#!/usr/bin/env python3
"""Experiment B — Control Group.

Four conditions, all with seed=42:
  1. Treatment: 15 iterations on 5 Lesson 1.1 phonics exemplars.
  2. Control 1 (no-update): Zero gradient steps, evaluate twice.
  3. Control 2a (random bytes): 15 iterations on random byte sequences.
  4. Control 2b (unrelated English): 15 iterations on unrelated English sentences.

All conditions use the same 4 Lesson 1.1 test items for pre/post evaluation.
"""

from __future__ import annotations

import random
import torch

from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

# ── Configuration ───────────────────────────────────────────────────────────

SEED = 42
ITERATIONS = 15
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Original Lesson 1.1 training exemplars
TREATMENT_EXEMPLARS = [
    "The cat sat on the mat.",
    "The dog can run in the sun.",
    "The sun is hot.",
    "The red pen is on the bed.",
    "A cat can run.",
]

# Control corpus — unrelated English (no phonics/CVC overlap)
CONTROL_ENGLISH = [
    "The system processes data files.",
    "Network latency affects throughput.",
    "Database queries return results.",
    "The compiler optimizes register allocation.",
    "Memory allocation requires careful management.",
]


def make_random_byte_exemplars(seed: int) -> list[str]:
    """Generate random byte strings matching the token lengths of treatment exemplars."""
    rng = random.Random(seed)
    result = []
    for exemplar in TREATMENT_EXEMPLARS:
        length = len(exemplar.encode("utf-8"))
        raw = bytes(rng.randint(32, 126) for _ in range(length))  # printable ASCII
        result.append(raw.decode("latin1"))
    return result


# Test items (same as Lesson 1.1)
TEST_ITEMS = [
    ("The cat sat on the ", "mat."),
    ("The sun is ", "hot."),
    ("The dog can ", "run."),
    ("The red pen is on the ", "bed."),
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
    print(f"  {'Prompt':<28} {'Target':<8} {'Loss':>8}   {'Generated'}")
    print(f"  {'─' * 26} {'─' * 6} {'─' * 8}   {'─' * 30}")
    for it in items:
        gen_clean = it["generated"].replace("\n", "\\n")
        print(f"  {it['prompt']:<28} {it['target']:<8} {it['loss']:>8.4f}   {gen_clean}")
    avg = sum(it["loss"] for it in items) / max(len(items), 1)
    print(f"  {'':>28} {'AVG':>8} {avg:>8.4f}")


def run_condition(
    label: str,
    tokenizer: BabyTokenizer,
    train: bool,
    exemplars: list[str] | None = None,
) -> dict:
    """Run a single condition and return results dict."""
    model, optimizer = fresh_model_and_optimizer()
    print(f"\n{'=' * 80}")
    print(f"  CONDITION: {label}")
    print(f"{'=' * 80}")
    print(f"  Model params: {model.get_num_params():,}")

    # Pre-evaluation
    pre_eval = evaluate_items(model, tokenizer, TEST_ITEMS, DEVICE)
    print_eval_table(f"{label} — Pre-Evaluation", pre_eval)

    if train and exemplars:
        losses = train_on_exemplars(model, tokenizer, optimizer, exemplars, ITERATIONS, DEVICE)
        print(f"\n  Training: {ITERATIONS} iterations")
        print(f"    Initial loss: {losses[0]:.4f}")
        print(f"    Final loss:   {losses[-1]:.4f}")
    else:
        losses = []
        print(f"\n  No training (control condition)")

    # Post-evaluation
    post_eval = evaluate_items(model, tokenizer, TEST_ITEMS, DEVICE)
    print_eval_table(f"{label} — Post-Evaluation", post_eval)

    pre_avg = sum(it["loss"] for it in pre_eval) / len(pre_eval)
    post_avg = sum(it["loss"] for it in post_eval) / len(post_eval)
    delta = pre_avg - post_avg

    return {
        "label": label,
        "pre_eval": pre_eval,
        "post_eval": post_eval,
        "pre_avg": pre_avg,
        "post_avg": post_avg,
        "delta": delta,
        "train_losses": losses,
    }


# ── Main ───────────────────────────────────────────────────────────────────


def main() -> None:
    print(f"=== Experiment B — Control Group ===")
    print(f"Device: {DEVICE}")
    print(f"Seed: {SEED}")
    print(f"Iterations: {ITERATIONS}")

    tokenizer = BabyTokenizer()

    # Generate random byte control corpus
    random_bytes = make_random_byte_exemplars(SEED)

    all_results = []

    # ── Condition 1: Treatment (Lesson 1.1 exemplars) ───────────────────────
    all_results.append(run_condition(
        "Treatment (Lesson 1.1 Phonics)",
        tokenizer,
        train=True,
        exemplars=TREATMENT_EXEMPLARS,
    ))

    # ── Condition 2: Control 1 (no update) ─────────────────────────────────
    all_results.append(run_condition(
        "Control 1 (No Update)",
        tokenizer,
        train=False,
    ))

    # ── Condition 3: Control 2a (random bytes) ─────────────────────────────
    all_results.append(run_condition(
        "Control 2a (Random Bytes)",
        tokenizer,
        train=True,
        exemplars=random_bytes,
    ))

    # ── Condition 4: Control 2b (unrelated English) ─────────────────────────
    all_results.append(run_condition(
        "Control 2b (Unrelated English)",
        tokenizer,
        train=True,
        exemplars=CONTROL_ENGLISH,
    ))

    # ── Summary Comparison ─────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  SUMMARY — Loss Delta Comparison")
    print(f"{'=' * 80}")

    print(f"\n  {'Condition':<35} {'Pre-Avg':>8} {'Post-Avg':>8} {'Delta':>8}  {'Notes'}")
    print(f"  {'─' * 33} {'─' * 8} {'─' * 8} {'─' * 8}  {'─' * 25}")

    for r in all_results:
        notes = ""
        if "No Update" in r["label"]:
            notes = "Should be ~0 delta"
        elif "Random Bytes" in r["label"]:
            notes = "Tests any-text effect"
        elif "Unrelated English" in r["label"]:
            notes = "Tests generic English transfer"
        elif "Treatment" in r["label"]:
            notes = "Lesson-specific training"
        print(f"  {r['label']:<35} {r['pre_avg']:>8.4f} {r['post_avg']:>8.4f} {r['delta']:>+8.4f}  {notes}")

    # Per-item comparison across conditions
    print(f"\n{'=' * 80}")
    print("  PER-ITEM COMPARISON")
    print(f"{'=' * 80}")

    for i, (prompt, target) in enumerate(TEST_ITEMS):
        print(f"\n  Item {i+1}: `{prompt}` -> `{target}`")
        print(f"  {'Condition':<35} {'Pre-Loss':>8} {'Post-Loss':>8} {'Delta':>8}   {'Post-Gen'}")
        print(f"  {'─' * 33} {'─' * 8} {'─' * 8} {'─' * 8}   {'─' * 25}")
        for r in all_results:
            pre_it = r["pre_eval"][i]
            post_it = r["post_eval"][i]
            item_delta = pre_it["loss"] - post_it["loss"]
            gen_clean = post_it["generated"].replace("\n", "\\n")
            print(f"  {r['label']:<35} {pre_it['loss']:>8.4f} {post_it['loss']:>8.4f} {item_delta:>+8.4f}   {gen_clean}")

    print(f"\n{'=' * 80}")
    print("  Experiment B Complete")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
