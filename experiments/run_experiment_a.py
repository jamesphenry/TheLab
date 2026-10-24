#!/usr/bin/env python3
"""Experiment A — Held-Out Test.

Trains BabyLM on the original 5 Lesson 1.1 exemplars, then evaluates on:
  1. Training-adjacent test items (same as Lesson 1.1 experiment)
  2. Held-out items in 3 categories:
     - Category 1: Phonics-family transfer (seen letters, unseen CVC words)
     - Category 2: Sentence-context transfer (rearranged familiar words)
     - Category 3: Fully novel (no lexical overlap with training)

Records per-item cross-entropy before and after training, plus generated text.
"""

from __future__ import annotations

import torch

from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer
from harness.school.classroom import ClassroomSession
from harness.vault.controller import VaultController, Role

# ── Configuration ───────────────────────────────────────────────────────────

SEED = 42
ITERATIONS = 15
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Original Lesson 1.1 training exemplars
EXEMPLARS = [
    "The cat sat on the mat.",
    "The dog can run in the sun.",
    "The sun is hot.",
    "The red pen is on the bed.",
    "A cat can run.",
]

# Training-adjacent test items (same as Lesson 1.1 experiment)
TRAINING_ADJACENT_ITEMS = [
    ("The cat sat on the ", "mat."),
    ("The sun is ", "hot."),
    ("The dog can ", "run."),
    ("The red pen is on the ", "bed."),
]

# Held-out test items, grouped by category
HELD_OUT_ITEMS = {
    "Category 1 — Phonics-family transfer (seen letters, unseen CVC words)": [
        ("The cat sat on the ", "bat"),    # rhymes with mat, different word
        ("A dog can ", "log"),             # rhymes with dog, unseen as target
        ("The pen is ", "red"),           # seen in "red pen" but not as completion
    ],
    "Category 2 — Sentence-context transfer (rearranged familiar words)": [
        ("A dog sat on the ", "mat."),     # word transfer, new subject
        ("The cat is ", "hot."),           # word transfer, new subject
        ("The sun can ", "run."),          # word transfer, new subject
    ],
    "Category 3 — Fully novel (no lexical overlap with training)": [
        ("A pig can ", "dig."),            # unseen CVC pattern
        ("The bug is ", "big."),           # unseen CVC pattern
    ],
}


# ── Helpers ────────────────────────────────────────────────────────────────

def evaluate_items(
    model: BabyLM,
    tokenizer: BabyTokenizer,
    test_items: list[tuple[str, str]],
    device: str,
) -> list[dict]:
    """Evaluate cross-entropy loss and generation on prompt-target pairs."""
    model.eval()
    results = []

    for prompt, target in test_items:
        full_text = prompt + target
        tokens = tokenizer.encode(full_text, add_special_tokens=False)
        prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)

        if len(tokens) <= 1:
            continue

        input_ids = torch.tensor([tokens[:-1]], dtype=torch.long, device=device)
        target_ids = torch.tensor([tokens[1:]], dtype=torch.long, device=device)

        # Mask out prompt tokens so loss is only on target completion
        mask_len = len(prompt_tokens) - 1
        if mask_len > 0:
            target_ids[:, :mask_len] = -1

        with torch.no_grad():
            _, loss = model(input_ids, target_ids)
            loss_val = float(loss.item()) if loss is not None else 0.0

        # Generate sample completion
        prompt_tensor = torch.tensor([prompt_tokens], dtype=torch.long, device=device)
        generated_ids = model.generate(
            prompt_tensor,
            max_new_tokens=len(target) + 2,
            temperature=0.8,
        )
        generated_text = tokenizer.decode(generated_ids[0].tolist())

        results.append({
            "prompt": prompt,
            "target": target,
            "loss": loss_val,
            "generated": generated_text,
        })

    return results


def train_on_exemplars(
    model: BabyLM,
    tokenizer: BabyTokenizer,
    optimizer: torch.optim.Optimizer,
    exemplars: list[str],
    iterations: int,
    device: str,
) -> list[float]:
    """Train model for N iterations on exemplars, return per-iteration avg loss."""
    training_losses = []

    for _ in range(iterations):
        step_loss = 0.0
        for text in exemplars:
            tokens = tokenizer.encode(text, add_special_tokens=True)
            if len(tokens) <= 1:
                continue
            input_ids = torch.tensor([tokens[:-1]], dtype=torch.long, device=device)
            target_ids = torch.tensor([tokens[1:]], dtype=torch.long, device=device)
            loss = model.train_step(input_ids, target_ids, optimizer)
            step_loss += loss

        avg_step_loss = step_loss / max(len(exemplars), 1)
        training_losses.append(avg_step_loss)

    return training_losses


def print_eval_table(label: str, items: list[dict]) -> None:
    """Print a formatted evaluation table."""
    print(f"\n{'─' * 80}")
    print(f"  {label}")
    print(f"{'─' * 80}")
    print(f"  {'Prompt':<28} {'Target':<8} {'Loss':>8}   {'Generated'}")
    print(f"  {'─' * 26} {'─' * 6} {'─' * 8}   {'─' * 30}")
    for it in items:
        gen_clean = it["generated"].replace("\n", "\\n")
        print(f"  {it['prompt']:<28} {it['target']:<8} {it['loss']:>8.4f}   {gen_clean}")
    avg = sum(it["loss"] for it in items) / max(len(items), 1)
    print(f"  {'':>28} {'AVG':>8} {avg:>8.4f}")


# ── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"=== Experiment A — Held-Out Test ===")
    print(f"Device: {DEVICE}")
    print(f"Seed: {SEED}")
    print(f"Iterations: {ITERATIONS}")

    # Set seed for reproducibility
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)

    # Instantiate model
    config = BabyLMConfig(
        vocab_size=4096,
        max_seq_len=256,
        dim=512,
        n_layers=8,
        n_heads=8,
        device=DEVICE,
    )
    tokenizer = BabyTokenizer()
    model = BabyLM(config).to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    print(f"Model parameters: {model.get_num_params():,}")

    # Flatten all held-out items for evaluation
    all_held_out = []
    for items in HELD_OUT_ITEMS.values():
        all_held_out.extend(items)

    # ── 1. Pre-Training Evaluation ────────────────────────────────────────
    print("\n--- Pre-Training Evaluation ---")

    pre_training_adjacent = evaluate_items(model, tokenizer, TRAINING_ADJACENT_ITEMS, DEVICE)
    print_eval_table("Training-Adjacent Items (Pre)", pre_training_adjacent)

    pre_held_out_by_category: dict[str, list[dict]] = {}
    for cat_name, cat_items in HELD_OUT_ITEMS.items():
        pre_held_out_by_category[cat_name] = evaluate_items(model, tokenizer, cat_items, DEVICE)
        print_eval_table(f"Held-Out — {cat_name} (Pre)", pre_held_out_by_category[cat_name])

    # ── 2. Training ─────────────────────────────────────────────────────────
    print(f"\n--- Training ({ITERATIONS} iterations on 5 exemplars) ---")
    training_losses = train_on_exemplars(
        model, tokenizer, optimizer, EXEMPLARS, ITERATIONS, DEVICE
    )
    print(f"  Initial training loss: {training_losses[0]:.4f}")
    print(f"  Final training loss:   {training_losses[-1]:.4f}")

    # ── 3. Post-Training Evaluation ────────────────────────────────────────
    print("\n--- Post-Training Evaluation ---")

    post_training_adjacent = evaluate_items(model, tokenizer, TRAINING_ADJACENT_ITEMS, DEVICE)
    print_eval_table("Training-Adjacent Items (Post)", post_training_adjacent)

    post_held_out_by_category: dict[str, list[dict]] = {}
    for cat_name, cat_items in HELD_OUT_ITEMS.items():
        post_held_out_by_category[cat_name] = evaluate_items(model, tokenizer, cat_items, DEVICE)
        print_eval_table(f"Held-Out — {cat_name} (Post)", post_held_out_by_category[cat_name])

    # ── 4. Summary Comparison ─────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  SUMMARY — Loss Delta (Pre → Post)")
    print(f"{'=' * 80}")

    # Training-adjacent summary
    pre_adj_avg = sum(it["loss"] for it in pre_training_adjacent) / len(pre_training_adjacent)
    post_adj_avg = sum(it["loss"] for it in post_training_adjacent) / len(post_training_adjacent)
    adj_delta = pre_adj_avg - post_adj_avg
    print(f"\n  Training-Adjacent (n={len(pre_training_adjacent)}):")
    print(f"    Pre-avg:  {pre_adj_avg:.4f}")
    print(f"    Post-avg: {post_adj_avg:.4f}")
    print(f"    Delta:    {adj_delta:+.4f}")

    for cat_name in HELD_OUT_ITEMS:
        pre_items = pre_held_out_by_category[cat_name]
        post_items = post_held_out_by_category[cat_name]
        pre_avg = sum(it["loss"] for it in pre_items) / len(pre_items)
        post_avg = sum(it["loss"] for it in post_items) / len(post_items)
        delta = pre_avg - post_avg
        print(f"\n  {cat_name} (n={len(pre_items)}):")
        print(f"    Pre-avg:  {pre_avg:.4f}")
        print(f"    Post-avg: {post_avg:.4f}")
        print(f"    Delta:    {delta:+.4f}")

        # Per-item detail
        for pre_it, post_it in zip(pre_items, post_items):
            item_delta = pre_it["loss"] - post_it["loss"]
            print(f"      {pre_it['prompt']:<28} → {post_it['target']:<8}  "
                  f"pre={pre_it['loss']:.4f}  post={post_it['loss']:.4f}  Δ={item_delta:+.4f}  "
                  f"gen=\"{post_it['generated']}\"")

    # Overall held-out summary
    all_pre = [it for items in pre_held_out_by_category.values() for it in items]
    all_post = [it for items in post_held_out_by_category.values() for it in items]
    all_pre_avg = sum(it["loss"] for it in all_pre) / len(all_pre)
    all_post_avg = sum(it["loss"] for it in all_post) / len(all_post)
    all_delta = all_pre_avg - all_post_avg
    print(f"\n  All Held-Out Combined (n={len(all_pre)}):")
    print(f"    Pre-avg:  {all_pre_avg:.4f}")
    print(f"    Post-avg: {all_post_avg:.4f}")
    print(f"    Delta:    {all_delta:+.4f}")

    print(f"\n{'=' * 80}")
    print("  Experiment A Complete")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
