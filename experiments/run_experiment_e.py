#!/usr/bin/env python3
"""Experiment E — Reasoning.

Two conditions, both with seed=42:
  1. Condition 1 (Exemplars only): Train on original 5 Lesson 1.1 exemplars.
  2. Condition 2 (Exemplars + Rationale): Train on augmented exemplars with
     phonics pattern explanations appended.

Evaluates both conditions on:
  - Direct completion items (items 1-4): pattern application
  - Rationale generation items (items 5-8): pattern explanation
"""

from __future__ import annotations

import gc
import torch

from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

# ── Configuration ───────────────────────────────────────────────────────────

SEED = 42
ITERATIONS = 15
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

EXEMPLARS_PLAIN = [
    "The cat sat on the mat.",
    "The dog can run in the sun.",
    "The sun is hot.",
    "The red pen is on the bed.",
    "A cat can run.",
]

EXEMPLARS_RATIONALE = [
    "The cat sat on the mat. mat has the -at sound.",
    "The dog can run in the sun. run has the -un sound.",
    "The sun is hot. hot has the -ot sound.",
    "The red pen is on the bed. bed has the -ed sound.",
    "A cat can run. cat has the -at sound.",
]

DIRECT_ITEMS = [
    ("The cat sat on the ", "mat."),
    ("The sun is ", "hot."),
    ("The dog can ", "run."),
    ("The red pen is on the ", "bed."),
]

RATIONALE_ITEMS = [
    ("The cat sat on the mat. mat has the ", "-at sound."),
    ("The sun is hot. hot has the ", "-ot sound."),
    ("The dog can run. run has the ", "-un sound."),
    ("The red pen is on the bed. bed has the ", "-ed sound."),
]

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

        mask_len = len(prompt_tokens) - 1
        if mask_len > 0:
            target_ids[:, :mask_len] = -1

        with torch.no_grad():
            _, loss = model(input_ids, target_ids)
            loss_val = float(loss.item()) if loss is not None else 0.0

        prompt_tensor = torch.tensor([prompt_tokens], dtype=torch.long, device=device)
        generated_ids = model.generate(
            prompt_tensor,
            max_new_tokens=len(target) + 4,
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


def fresh_model_and_optimizer() -> tuple[BabyLM, torch.optim.Optimizer]:
    """Create a fresh model and optimizer with the global seed."""
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)

    config = BabyLMConfig(
        vocab_size=4096,
        max_seq_len=256,
        dim=512,
        n_layers=8,
        n_heads=8,
        device=DEVICE,
    )
    model = BabyLM(config).to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    return model, optimizer


def print_eval_table(label: str, items: list[dict]) -> None:
    """Print a formatted evaluation table."""
    print(f"\n{'─' * 80}")
    print(f"  {label}")
    print(f"{'─' * 80}")
    print(f"  {'Prompt':<40} {'Target':<14} {'Loss':>8}   {'Generated'}")
    print(f"  {'─' * 38} {'─' * 12} {'─' * 8}   {'─' * 30}")
    for it in items:
        gen_clean = it["generated"].replace("\n", "\\n")
        print(f"  {it['prompt']:<40} {it['target']:<14} {it['loss']:>8.4f}   {gen_clean}")
    avg = sum(it["loss"] for it in items) / max(len(items), 1)
    print(f"  {'':>40} {'AVG':>14} {avg:>8.4f}")


def run_condition(
    label: str,
    tokenizer: BabyTokenizer,
    exemplars: list[str],
) -> dict:
    """Run a single condition and return results dict."""
    model, optimizer = fresh_model_and_optimizer()
    print(f"\n{'=' * 80}")
    print(f"  CONDITION: {label}")
    print(f"{'=' * 80}")
    print(f"  Model params: {model.get_num_params():,}")

    pre_direct = evaluate_items(model, tokenizer, DIRECT_ITEMS, DEVICE)
    print_eval_table(f"{label} — Direct Completion (Pre)", pre_direct)

    pre_rationale = evaluate_items(model, tokenizer, RATIONALE_ITEMS, DEVICE)
    print_eval_table(f"{label} — Rationale Generation (Pre)", pre_rationale)

    losses = train_on_exemplars(model, tokenizer, optimizer, exemplars, ITERATIONS, DEVICE)
    print(f"\n  Training: {ITERATIONS} iterations")
    print(f"    Initial loss: {losses[0]:.4f}")
    print(f"    Final loss:   {losses[-1]:.4f}")

    post_direct = evaluate_items(model, tokenizer, DIRECT_ITEMS, DEVICE)
    print_eval_table(f"{label} — Direct Completion (Post)", post_direct)

    post_rationale = evaluate_items(model, tokenizer, RATIONALE_ITEMS, DEVICE)
    print_eval_table(f"{label} — Rationale Generation (Post)", post_rationale)

    pre_direct_avg = sum(it["loss"] for it in pre_direct) / len(pre_direct)
    post_direct_avg = sum(it["loss"] for it in post_direct) / len(post_direct)
    pre_rat_avg = sum(it["loss"] for it in pre_rationale) / len(pre_rationale)
    post_rat_avg = sum(it["loss"] for it in post_rationale) / len(post_rationale)

    del model, optimizer
    gc.collect()

    return {
        "label": label,
        "pre_direct": pre_direct,
        "post_direct": post_direct,
        "pre_rationale": pre_rationale,
        "post_rationale": post_rationale,
        "pre_direct_avg": pre_direct_avg,
        "post_direct_avg": post_direct_avg,
        "pre_rat_avg": pre_rat_avg,
        "post_rat_avg": post_rat_avg,
        "direct_delta": pre_direct_avg - post_direct_avg,
        "rationale_delta": pre_rat_avg - post_rat_avg,
        "train_initial": losses[0],
        "train_final": losses[-1],
    }


# ── Main ───────────────────────────────────────────────────────────────────


def main() -> None:
    print(f"=== Experiment E — Reasoning ===")
    print(f"Device: {DEVICE}")
    print(f"Seed: {SEED}")
    print(f"Iterations: {ITERATIONS}")

    tokenizer = BabyTokenizer()

    cond1 = run_condition("Condition 1 (Exemplars Only)", tokenizer, EXEMPLARS_PLAIN)
    cond2 = run_condition("Condition 2 (Exemplars + Rationale)", tokenizer, EXEMPLARS_RATIONALE)

    # ── Summary ─────────────────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  SUMMARY — Loss Delta Comparison")
    print(f"{'=' * 80}")

    print(f"\n  {'Condition':<40} {'Direct Δ':>10} {'Rationale Δ':>12}")
    print(f"  {'─' * 38} {'─' * 10} {'─' * 12}")
    for r in [cond1, cond2]:
        print(f"  {r['label']:<40} {r['direct_delta']:>+10.4f} {r['rationale_delta']:>+12.4f}")

    print(f"\n  {'Condition':<40} {'Dir Pre':>8} {'Dir Post':>9} {'Rat Pre':>8} {'Rat Post':>9}")
    print(f"  {'─' * 38} {'─' * 8} {'─' * 9} {'─' * 8} {'─' * 9}")
    for r in [cond1, cond2]:
        print(f"  {r['label']:<40} {r['pre_direct_avg']:>8.4f} {r['post_direct_avg']:>9.4f} "
              f"{r['pre_rat_avg']:>8.4f} {r['post_rat_avg']:>9.4f}")

    # ── Per-Item: Direct Completion ────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  PER-ITEM — Direct Completion (Pattern Application)")
    print(f"{'=' * 80}")

    for i, (prompt, target) in enumerate(DIRECT_ITEMS):
        print(f"\n  Item {i+1}: `{prompt}` -> `{target}`")
        print(f"  {'Condition':<40} {'Pre':>8} {'Post':>8} {'Delta':>8}   {'Post-Gen'}")
        print(f"  {'─' * 38} {'─' * 8} {'─' * 8} {'─' * 8}   {'─' * 25}")
        for r in [cond1, cond2]:
            pre_it = r["pre_direct"][i]
            post_it = r["post_direct"][i]
            item_delta = pre_it["loss"] - post_it["loss"]
            gen_clean = post_it["generated"].replace("\n", "\\n")
            print(f"  {r['label']:<40} {pre_it['loss']:>8.4f} {post_it['loss']:>8.4f} {item_delta:>+8.4f}   {gen_clean}")

    # ── Per-Item: Rationale Generation ─────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  PER-ITEM — Rationale Generation (Pattern Explanation)")
    print(f"{'=' * 80}")

    for i, (prompt, target) in enumerate(RATIONALE_ITEMS):
        print(f"\n  Item {i+4}: `{prompt}` -> `{target}`")
        print(f"  {'Condition':<40} {'Pre':>8} {'Post':>8} {'Delta':>8}   {'Post-Gen'}")
        print(f"  {'─' * 38} {'─' * 8} {'─' * 8} {'─' * 8}   {'─' * 25}")
        for r in [cond1, cond2]:
            pre_it = r["pre_rationale"][i]
            post_it = r["post_rationale"][i]
            item_delta = pre_it["loss"] - post_it["loss"]
            gen_clean = post_it["generated"].replace("\n", "\\n")
            print(f"  {r['label']:<40} {pre_it['loss']:>8.4f} {post_it['loss']:>8.4f} {item_delta:>+8.4f}   {gen_clean}")

    print(f"\n{'=' * 80}")
    print("  Experiment E Complete")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
