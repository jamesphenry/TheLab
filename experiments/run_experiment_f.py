#!/usr/bin/env python3
"""Experiment F — Multi-Seed Rationale Transfer.

Paired comparison across 10 seeds:
  Condition 1: train on plain exemplars, evaluate on held-out items.
  Condition 2: train on rationale exemplars, evaluate on same held-out items.

Both conditions use the same seed — only difference is the training set.
Measures whether rationale training produces a reproducible advantage on
tasks the model has never seen.
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

# Held-out direct completion (all novel — not in training exemplars)
HELD_OUT_DIRECT = [
    ("A dog sat on the ", "mat."),    # sentence-context transfer
    ("The cat is ", "hot."),          # sentence-context transfer
    ("The sun can ", "run."),         # sentence-context transfer
    ("A pig can ", "dig."),           # fully novel
    ("The bug is ", "big."),          # fully novel
]

# Held-out rationale generation (all novel — word not in rationale exemplars
# OR sentence context not seen)
HELD_OUT_RATIONALE = [
    ("A dog sat on the mat. mat has the ", "-at sound."),   # familiar word, new context
    ("The cat is hot. hot has the ", "-ot sound."),         # familiar word, new context
    ("A pig can dig. dig has the ", "-ig sound."),           # novel word
    ("The bug is big. big has the ", "-ig sound."),          # novel word
]

# ── Helpers ────────────────────────────────────────────────────────────────


def evaluate_items(model, tokenizer, test_items, device):
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
            prompt_tensor, max_new_tokens=len(target) + 4, temperature=0.8
        )
        generated_text = tokenizer.decode(generated_ids[0].tolist())
        results.append({
            "prompt": prompt, "target": target,
            "loss": loss_val, "generated": generated_text,
        })
    return results


def train_on_exemplars(model, tokenizer, optimizer, exemplars, iterations, device):
    losses = []
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
        losses.append(step_loss / max(len(exemplars), 1))
    return losses


def run_condition(seed, tokenizer, exemplars):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    config = BabyLMConfig(
        vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8, device=DEVICE
    )
    model = BabyLM(config).to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    pre_direct = evaluate_items(model, tokenizer, HELD_OUT_DIRECT, DEVICE)
    pre_rat = evaluate_items(model, tokenizer, HELD_OUT_RATIONALE, DEVICE)

    train_losses = train_on_exemplars(model, tokenizer, optimizer, exemplars, ITERATIONS, DEVICE)

    post_direct = evaluate_items(model, tokenizer, HELD_OUT_DIRECT, DEVICE)
    post_rat = evaluate_items(model, tokenizer, HELD_OUT_RATIONALE, DEVICE)

    # Extract data before cleanup
    pre_d_losses = [it["loss"] for it in pre_direct]
    post_d_losses = [it["loss"] for it in post_direct]
    post_d_gens = [it["generated"] for it in post_direct]
    pre_r_losses = [it["loss"] for it in pre_rat]
    post_r_losses = [it["loss"] for it in post_rat]
    post_r_gens = [it["generated"] for it in post_rat]

    del model, optimizer
    gc.collect()

    return {
        "pre_direct_avg": sum(pre_d_losses) / len(pre_d_losses),
        "post_direct_avg": sum(post_d_losses) / len(post_d_losses),
        "direct_delta": sum(pre_d_losses) / len(pre_d_losses) - sum(post_d_losses) / len(post_d_losses),
        "pre_rat_avg": sum(pre_r_losses) / len(pre_r_losses),
        "post_rat_avg": sum(post_r_losses) / len(post_r_losses),
        "rationale_delta": sum(pre_r_losses) / len(pre_r_losses) - sum(post_r_losses) / len(post_r_losses),
        "pre_d_losses": pre_d_losses,
        "post_d_losses": post_d_losses,
        "post_d_gens": post_d_gens,
        "pre_r_losses": pre_r_losses,
        "post_r_losses": post_r_losses,
        "post_r_gens": post_r_gens,
        "train_initial": train_losses[0],
        "train_final": train_losses[-1],
    }


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    print(f"=== Experiment F — Multi-Seed Rationale Transfer ===")
    print(f"Device: {DEVICE}")
    print(f"Iterations: {ITERATIONS}")
    print(f"Seeds: {SEEDS}")
    print(f"Held-out direct items: {len(HELD_OUT_DIRECT)}")
    print(f"Held-out rationale items: {len(HELD_OUT_RATIONALE)}")

    tokenizer = BabyTokenizer()
    all_results = []

    for i, seed in enumerate(SEEDS):
        print(f"\n{'=' * 80}")
        print(f"  Seed {seed} ({i+1}/{len(SEEDS)})")
        print(f"{'=' * 80}")

        cond1 = run_condition(seed, tokenizer, EXEMPLARS_PLAIN)
        print(f"  Cond 1 (Plain):  direct Δ={cond1['direct_delta']:+.4f}  "
              f"rationale Δ={cond1['rationale_delta']:+.4f}  "
              f"train {cond1['train_initial']:.2f}->{cond1['train_final']:.2f}")

        cond2 = run_condition(seed, tokenizer, EXEMPLARS_RATIONALE)
        print(f"  Cond 2 (Rationale): direct Δ={cond2['direct_delta']:+.4f}  "
              f"rationale Δ={cond2['rationale_delta']:+.4f}  "
              f"train {cond2['train_initial']:.2f}->{cond2['train_final']:.2f}")

        d_adv = cond2["direct_delta"] - cond1["direct_delta"]
        r_adv = cond2["rationale_delta"] - cond1["rationale_delta"]
        print(f"  Advantage:        direct={d_adv:+.4f}  rationale={r_adv:+.4f}")

        all_results.append({
            "seed": seed,
            "cond1": cond1,
            "cond2": cond2,
            "direct_advantage": d_adv,
            "rationale_advantage": r_adv,
        })

    # ── Summary ────────────────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  SUMMARY — Per-Seed Results")
    print(f"{'=' * 80}")

    print(f"\n  {'Seed':<8} {'C1 Dir Δ':>8} {'C2 Dir Δ':>8} {'Dir Adv':>8} "
          f"{'C1 Rat Δ':>8} {'C2 Rat Δ':>8} {'Rat Adv':>8}")
    print(f"  {'─' * 6} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8} {'─' * 8}")

    for r in all_results:
        c1 = r["cond1"]
        c2 = r["cond2"]
        print(f"  {r['seed']:<8} {c1['direct_delta']:>+8.4f} {c2['direct_delta']:>+8.4f} "
              f"{r['direct_advantage']:>+8.4f} "
              f"{c1['rationale_delta']:>+8.4f} {c2['rationale_delta']:>+8.4f} "
              f"{r['rationale_advantage']:>+8.4f}")

    # Aggregate stats
    d_advs = [r["direct_advantage"] for r in all_results]
    r_advs = [r["rationale_advantage"] for r in all_results]

    d_mean = sum(d_advs) / len(d_advs)
    d_std = (sum((x - d_mean) ** 2 for x in d_advs) / len(d_advs)) ** 0.5
    r_mean = sum(r_advs) / len(r_advs)
    r_std = (sum((x - r_mean) ** 2 for x in r_advs) / len(r_advs)) ** 0.5

    print(f"\n  {'Statistic':<16} {'Direct Advantage':>16} {'Rationale Advantage':>20}")
    print(f"  {'─' * 14} {'─' * 16} {'─' * 20}")
    print(f"  {'Mean':<16} {d_mean:>+16.4f} {r_mean:>+20.4f}")
    print(f"  {'Std Dev':<16} {d_std:>16.4f} {r_std:>20.4f}")
    print(f"  {'Min':<16} {min(d_advs):>+16.4f} {min(r_advs):>+20.4f}")
    print(f"  {'Max':<16} {max(d_advs):>+16.4f} {max(r_advs):>+20.4f}")
    print(f"  {'Seeds positive':<16} {sum(1 for x in d_advs if x > 0):>16} {sum(1 for x in r_advs if x > 0):>20}")

    # ── Per-Item Analysis ─────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  PER-ITEM — Held-Out Direct Completion")
    print(f"{'=' * 80}")

    for idx, (prompt, target) in enumerate(HELD_OUT_DIRECT):
        c1_deltas = [r["cond1"]["pre_d_losses"][idx] - r["cond1"]["post_d_losses"][idx]
                     for r in all_results]
        c2_deltas = [r["cond2"]["pre_d_losses"][idx] - r["cond2"]["post_d_losses"][idx]
                     for r in all_results]
        advs = [c2 - c1 for c1, c2 in zip(c1_deltas, c2_deltas)]
        mean_adv = sum(advs) / len(advs)
        pos_count = sum(1 for a in advs if a > 0)

        print(f"\n  Item {idx+1}: `{prompt}` -> `{target}`")
        print(f"    Cond1 mean Δ: {sum(c1_deltas)/len(c1_deltas):+.4f}  "
              f"Cond2 mean Δ: {sum(c2_deltas)/len(c2_deltas):+.4f}  "
              f"Advantage: {mean_adv:+.4f}  ({pos_count}/{len(advs)} seeds positive)")
        print(f"    Per-seed advantage: {' '.join(f'{a:+.2f}' for a in advs)}")

    print(f"\n{'=' * 80}")
    print("  PER-ITEM — Held-Out Rationale Generation")
    print(f"{'=' * 80}")

    for idx, (prompt, target) in enumerate(HELD_OUT_RATIONALE):
        c1_deltas = [r["cond1"]["pre_r_losses"][idx] - r["cond1"]["post_r_losses"][idx]
                     for r in all_results]
        c2_deltas = [r["cond2"]["pre_r_losses"][idx] - r["cond2"]["post_r_losses"][idx]
                     for r in all_results]
        advs = [c2 - c1 for c1, c2 in zip(c1_deltas, c2_deltas)]
        mean_adv = sum(advs) / len(advs)
        pos_count = sum(1 for a in advs if a > 0)

        print(f"\n  Item {idx+5}: `{prompt}` -> `{target}`")
        print(f"    Cond1 mean Δ: {sum(c1_deltas)/len(c1_deltas):+.4f}  "
              f"Cond2 mean Δ: {sum(c2_deltas)/len(c2_deltas):+.4f}  "
              f"Advantage: {mean_adv:+.4f}  ({pos_count}/{len(advs)} seeds positive)")
        print(f"    Per-seed advantage: {' '.join(f'{a:+.2f}' for a in advs)}")

    # ── Qualitative Sample ────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  QUALITATIVE — Sample Generated Rationale (Seed 42)")
    print(f"{'=' * 80}")

    sample = all_results[0]
    for idx, (prompt, target) in enumerate(HELD_OUT_RATIONALE):
        gen1 = sample["cond1"]["post_r_gens"][idx]
        gen2 = sample["cond2"]["post_r_gens"][idx]
        print(f"\n  {prompt} -> `{target}`")
        print(f"    Cond1: `{gen1}`")
        print(f"    Cond2: `{gen2}`")

    print(f"\n{'=' * 80}")
    print("  Experiment F Complete")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
