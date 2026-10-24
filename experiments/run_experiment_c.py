#!/usr/bin/env python3
"""Experiment C — Multiple Random Seeds.

Repeats the Lesson 1.1 learning cycle across 10 independently initialized
models. Reports mean, std, min, max of loss delta to assess reproducibility
of the single-run result from the original experiment (delta=3.7655).
"""

from __future__ import annotations

import gc
import torch

from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

# ── Configuration ───────────────────────────────────────────────────────────

SEEDS = [42, 123, 7, 2026, 99, 314, 256, 13, 555, 8]
ITERATIONS = 15
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

EXEMPLARS = [
    "The cat sat on the mat.",
    "The dog can run in the sun.",
    "The sun is hot.",
    "The red pen is on the bed.",
    "A cat can run.",
]

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


def run_seed(seed: int, tokenizer: BabyTokenizer) -> dict:
    """Run a single seed: fresh model, pre-eval, train, post-eval."""
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

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

    # Pre-evaluation
    pre_eval = evaluate_items(model, tokenizer, TEST_ITEMS, DEVICE)
    pre_avg = sum(it["loss"] for it in pre_eval) / len(pre_eval)

    # Training
    train_losses = train_on_exemplars(model, tokenizer, optimizer, EXEMPLARS, ITERATIONS, DEVICE)

    # Post-evaluation
    post_eval = evaluate_items(model, tokenizer, TEST_ITEMS, DEVICE)
    post_avg = sum(it["loss"] for it in post_eval) / len(post_eval)

    delta = pre_avg - post_avg

    # Extract per-item data before cleanup
    pre_item_losses = [it["loss"] for it in pre_eval]
    post_item_losses = [it["loss"] for it in post_eval]
    post_item_gens = [it["generated"] for it in post_eval]

    # Cleanup to free memory
    del model, optimizer, pre_eval, post_eval
    gc.collect()

    return {
        "seed": seed,
        "pre_avg": pre_avg,
        "post_avg": post_avg,
        "delta": delta,
        "initial_train_loss": train_losses[0],
        "final_train_loss": train_losses[-1],
        "pre_item_losses": pre_item_losses,
        "post_item_losses": post_item_losses,
        "post_item_gens": post_item_gens,
        "train_losses": train_losses,
    }


# ── Main ───────────────────────────────────────────────────────────────────


def main() -> None:
    print(f"=== Experiment C — Multiple Random Seeds ===")
    print(f"Device: {DEVICE}")
    print(f"Iterations: {ITERATIONS}")
    print(f"Seeds: {SEEDS}")

    tokenizer = BabyTokenizer()
    all_results = []

    for i, seed in enumerate(SEEDS):
        print(f"\n{'=' * 80}")
        print(f"  Seed {seed} ({i+1}/{len(SEEDS)})")
        print(f"{'=' * 80}")

        result = run_seed(seed, tokenizer)
        all_results.append(result)

        print(f"  Pre-eval avg:   {result['pre_avg']:.4f}")
        print(f"  Post-eval avg:  {result['post_avg']:.4f}")
        print(f"  Delta:          {result['delta']:+.4f}")
        print(f"  Train loss:     {result['initial_train_loss']:.4f} -> {result['final_train_loss']:.4f}")

        # Per-item post-eval
        for i, gen in enumerate(result["post_item_gens"]):
            gen_clean = gen.replace("\n", "\\n")
            print(f"    {TEST_ITEMS[i][0]:<28} -> {TEST_ITEMS[i][1]:<8}  post={result['post_item_losses'][i]:.4f}  gen=\"{gen_clean}\"")

    # ── Summary Statistics ─────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  SUMMARY — All Seeds")
    print(f"{'=' * 80}")

    print(f"\n  {'Seed':<8} {'Pre-Avg':>8} {'Post-Avg':>8} {'Delta':>8} {'Init Train':>10} {'Final Train':>10}")
    print(f"  {'─' * 6} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 10} {'─' * 10}")

    for r in all_results:
        print(f"  {r['seed']:<8} {r['pre_avg']:>8.4f} {r['post_avg']:>8.4f} {r['delta']:>+8.4f} "
              f"{r['initial_train_loss']:>10.4f} {r['final_train_loss']:>10.4f}")

    # Aggregate stats
    deltas = [r["delta"] for r in all_results]
    pre_avgs = [r["pre_avg"] for r in all_results]
    post_avgs = [r["post_avg"] for r in all_results]
    final_trains = [r["final_train_loss"] for r in all_results]

    mean_delta = sum(deltas) / len(deltas)
    std_delta = (sum((d - mean_delta) ** 2 for d in deltas) / len(deltas)) ** 0.5

    print(f"\n  {'Statistic':<16} {'Pre-Avg':>8} {'Post-Avg':>8} {'Delta':>8} {'Final Train':>10}")
    print(f"  {'─' * 14} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 10}")
    print(f"  {'Mean':<16} {sum(pre_avgs)/len(pre_avgs):>8.4f} {sum(post_avgs)/len(post_avgs):>8.4f} "
          f"{mean_delta:>+8.4f} {sum(final_trains)/len(final_trains):>10.4f}")
    print(f"  {'Std Dev':<16} {''} {''} {std_delta:>8.4f}")
    print(f"  {'Min':<16} {min(pre_avgs):>8.4f} {min(post_avgs):>8.4f} {min(deltas):>+8.4f} {min(final_trains):>10.4f}")
    print(f"  {'Max':<16} {max(pre_avgs):>8.4f} {max(post_avgs):>8.4f} {max(deltas):>+8.4f} {max(final_trains):>10.4f}")

    # Coefficient of variation
    cv = std_delta / mean_delta if mean_delta != 0 else float("inf")
    print(f"  {'CV (σ/μ)':<16} {cv:>8.4f}")

    # Compare with original single-run result
    original_delta = 3.7655
    print(f"\n  Original single-run delta (Lesson 1.1 experiment): {original_delta:+.4f}")
    print(f"  Mean delta across {len(SEEDS)} seeds:                {mean_delta:+.4f}")
    print(f"  Std dev:                                         {std_delta:.4f}")
    print(f"  Range: [{min(deltas):+.4f}, {max(deltas):+.4f}]")

    # Per-item analysis across seeds
    print(f"\n{'=' * 80}")
    print("  PER-ITEM ANALYSIS ACROSS SEEDS")
    print(f"{'=' * 80}")

    for i, (prompt, target) in enumerate(TEST_ITEMS):
        item_improvements = [r["pre_item_losses"][i] - r["post_item_losses"][i] for r in all_results]
        mean_imp = sum(item_improvements) / len(item_improvements)
        std_imp = (sum((x - mean_imp) ** 2 for x in item_improvements) / len(item_improvements)) ** 0.5

        print(f"\n  Item {i+1}: `{prompt}` -> `{target}`")
        print(f"    Mean improvement: {mean_imp:+.4f}  (std: {std_imp:.4f})")
        print(f"    Range: [{min(item_improvements):+.4f}, {max(item_improvements):+.4f}]")
        print(f"    Per-seed: {' '.join(f'{x:+.2f}' for x in item_improvements)}")

    print(f"\n{'=' * 80}")
    print("  Experiment C Complete")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
