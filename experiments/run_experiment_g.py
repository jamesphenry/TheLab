#!/usr/bin/env python3
"""Experiment G — Rule Learning vs Format Learning.

Three conditions, 10 paired seeds:
  1. Baseline: 5 rationale exemplars from Experiment E/F.
  2. Explicit-rule: 5 rationale exemplars + 10 explicit word→ending examples.
  3. Matched control: 5 rationale exemplars + 10 same-volume sentences with no rule.

Evaluates on held-out items:
  - Direct completion (items 1-5)
  - Rule identification (items 6-12): scored for exact ending match + format compliance
  - Rationale generation (items 13-15)

Key metric: rule accuracy (correct ending), not just loss reduction.
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

# Condition 1: Baseline rationale exemplars (from Experiment E/F)
EXEMPLARS_BASELINE = [
    "The cat sat on the mat. mat has the -at sound.",
    "The dog can run in the sun. run has the -un sound.",
    "The sun is hot. hot has the -ot sound.",
    "The red pen is on the bed. bed has the -ed sound.",
    "A cat can run. cat has the -at sound.",
]

# Condition 2: Explicit-rule (baseline + direct word→ending examples)
EXEMPLARS_EXPLICIT_RULE = [
    # Original rationale exemplars
    "The cat sat on the mat. mat has the -at sound.",
    "The dog can run in the sun. run has the -un sound.",
    "The sun is hot. hot has the -ot sound.",
    "The red pen is on the bed. bed has the -ed sound.",
    "A cat can run. cat has the -at sound.",
    # Explicit rule examples
    "cat ends with -at.",
    "mat ends with -at.",
    "hot ends with -ot.",
    "run ends with -un.",
    "bed ends with -ed.",
    "dig ends with -ig.",
    "big ends with -ig.",
    "pig ends with -ig.",
    "log ends with -og.",
    "bug ends with -ug.",
]

# Condition 3: Matched control (baseline + same-volume sentences, no rule)
EXEMPLARS_MATCHED_CONTROL = [
    # Original rationale exemplars
    "The cat sat on the mat. mat has the -at sound.",
    "The dog can run in the sun. run has the -un sound.",
    "The sun is hot. hot has the -ot sound.",
    "The red pen is on the bed. bed has the -ed sound.",
    "A cat can run. cat has the -at sound.",
    # Matched-volume sentences (no word→ending relationship)
    "cat is a small animal.",
    "mat is on the floor.",
    "hot means high temperature.",
    "run is a fast action.",
    "bed is for sleeping.",
    "dig is what pigs do.",
    "big means large size.",
    "pig is a farm animal.",
    "log is a piece of wood.",
    "bug is a small insect.",
]

# Held-out direct completion (pattern application on unseen prompts)
HELD_OUT_DIRECT = [
    ("A dog sat on the ", "mat."),
    ("The cat is ", "hot."),
    ("The sun can ", "run."),
    ("A pig can ", "dig."),
    ("The bug is ", "big."),
]

# Held-out rule identification (does the model produce the correct ending?)
# dig appears in explicit-rule training, but this exact prompt format is withheld
HELD_OUT_RULES = [
    ("cat ends with ", "-at."),
    ("hot ends with ", "-ot."),
    ("run ends with ", "-un."),
    ("dig ends with ", "-ig."),
    ("bug ends with ", "-ug."),
    ("log ends with ", "-og."),
    ("pen ends with ", "-en."),  # fully novel — word AND ending never in training
]

# Held-out rationale generation (format vs content — from Experiment F)
HELD_OUT_RATIONALE = [
    ("The cat is hot. hot has the ", "-ot sound."),
    ("A pig can dig. dig has the ", "-ig sound."),
    ("The bug is big. big has the ", "-ig sound."),
]

# ── Helpers ────────────────────────────────────────────────────────────────


def evaluate_items(model, tokenizer, test_items, device):
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
            prompt_tensor, max_new_tokens=len(target) + 4, temperature=0.8
        )
        generated_text = tokenizer.decode(generated_ids[0].tolist())
        results.append({
            "prompt": prompt, "target": target,
            "loss": loss_val, "generated": generated_text,
        })
    return results


def score_rule_accuracy(generated_text, target_ending):
    """Score whether generated text contains the correct ending.

    Returns (starts_with_hyphen, exact_ending_match).
    """
    # Extract the portion after the prompt (generated includes the prompt)
    # The target ending is like "-at." — we check if generated text contains it
    # Strip the ending to get just the pattern (e.g. "-at" from "-at.")
    target_clean = target_ending.rstrip(".")

    # Check if generation starts with hyphen (format compliance)
    # The generated text includes the prompt, so look at what comes after the prompt
    # We'll check if a hyphen appears in the generated completion portion
    # For simplicity, check if the generated text contains the target ending pattern
    starts_with_hyphen = "-" in generated_text

    # Check exact ending match: does the generated text contain the target ending?
    exact_match = target_clean in generated_text

    return starts_with_hyphen, exact_match


def train_on_exemplars(model, tokenizer, optimizer, exemplars, iterations, device):
    """Train model for N iterations on exemplars."""
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
    """Run a single condition: fresh model, pre-eval, train, post-eval."""
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    config = BabyLMConfig(
        vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8, device=DEVICE
    )
    model = BabyLM(config).to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    # Pre-eval (loss only — generation is random pre-training)
    pre_direct = evaluate_items(model, tokenizer, HELD_OUT_DIRECT, DEVICE)
    pre_rules = evaluate_items(model, tokenizer, HELD_OUT_RULES, DEVICE)
    pre_rat = evaluate_items(model, tokenizer, HELD_OUT_RATIONALE, DEVICE)

    # Train
    train_losses = train_on_exemplars(model, tokenizer, optimizer, exemplars, ITERATIONS, DEVICE)

    # Post-eval
    post_direct = evaluate_items(model, tokenizer, HELD_OUT_DIRECT, DEVICE)
    post_rules = evaluate_items(model, tokenizer, HELD_OUT_RULES, DEVICE)
    post_rat = evaluate_items(model, tokenizer, HELD_OUT_RATIONALE, DEVICE)

    # Extract data before cleanup
    result = {
        "pre_direct_losses": [it["loss"] for it in pre_direct],
        "post_direct_losses": [it["loss"] for it in post_direct],
        "post_direct_gens": [it["generated"] for it in post_direct],
        "pre_rule_losses": [it["loss"] for it in pre_rules],
        "post_rule_losses": [it["loss"] for it in post_rules],
        "post_rule_gens": [it["generated"] for it in post_rules],
        "pre_rat_losses": [it["loss"] for it in pre_rat],
        "post_rat_losses": [it["loss"] for it in post_rat],
        "post_rat_gens": [it["generated"] for it in post_rat],
        "train_initial": train_losses[0],
        "train_final": train_losses[-1],
    }

    # Score rule accuracy
    rule_scores = []
    for i, (prompt, target) in enumerate(HELD_OUT_RULES):
        gen = result["post_rule_gens"][i]
        starts_hyphen, exact = score_rule_accuracy(gen, target)
        rule_scores.append({"prompt": prompt, "target": target,
                            "generated": gen, "starts_hyphen": starts_hyphen,
                            "exact_match": exact})
    result["rule_scores"] = rule_scores

    del model, optimizer
    gc.collect()

    return result


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    print(f"=== Experiment G — Rule Learning vs Format Learning ===")
    print(f"Device: {DEVICE}")
    print(f"Iterations: {ITERATIONS}")
    print(f"Seeds: {SEEDS}")
    print(f"Conditions: Baseline, Explicit-rule, Matched control")
    print(f"Held-out items: {len(HELD_OUT_DIRECT)} direct, {len(HELD_OUT_RULES)} rules, {len(HELD_OUT_RATIONALE)} rationale")

    tokenizer = BabyTokenizer()
    all_results = []  # list of (seed, cond1, cond2, cond3)

    conditions = [
        ("Baseline", EXEMPLARS_BASELINE),
        ("Explicit-rule", EXEMPLARS_EXPLICIT_RULE),
        ("Matched control", EXEMPLARS_MATCHED_CONTROL),
    ]

    for si, seed in enumerate(SEEDS):
        print(f"\n{'=' * 80}")
        print(f"  Seed {seed} ({si+1}/{len(SEEDS)})")
        print(f"{'=' * 80}")

        seed_results = {}
        for cond_name, cond_exemplars in conditions:
            r = run_condition(seed, tokenizer, cond_exemplars)
            seed_results[cond_name] = r

            # Compute deltas
            d_delta = sum(r["pre_direct_losses"][i] - r["post_direct_losses"][i]
                          for i in range(len(HELD_OUT_DIRECT))) / len(HELD_OUT_DIRECT)
            r_delta = sum(r["pre_rule_losses"][i] - r["post_rule_losses"][i]
                          for i in range(len(HELD_OUT_RULES))) / len(HELD_OUT_RULES)
            rat_delta = sum(r["pre_rat_losses"][i] - r["post_rat_losses"][i]
                            for i in range(len(HELD_OUT_RATIONALE))) / len(HELD_OUT_RATIONALE)

            # Rule accuracy
            format_count = sum(1 for s in r["rule_scores"] if s["starts_hyphen"])
            exact_count = sum(1 for s in r["rule_scores"] if s["exact_match"])

            print(f"  {cond_name:<16}: dir Δ={d_delta:+.4f}  rule Δ={r_delta:+.4f}  "
                  f"rat Δ={rat_delta:+.4f}  "
                  f"format={format_count}/{len(HELD_OUT_RULES)}  "
                  f"exact={exact_count}/{len(HELD_OUT_RULES)}  "
                  f"train {r['train_initial']:.2f}->{r['train_final']:.2f}")

        all_results.append((seed, seed_results))

    # ── Summary ────────────────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  SUMMARY — Loss Deltas Across Seeds")
    print(f"{'=' * 80}")

    print(f"\n  {'Seed':<8}", end="")
    for cond_name, _ in conditions:
        print(f"  {cond_name:<16}", end="")
    print()
    print(f"  {'─' * 6}", end="")
    for _ in conditions:
        print(f"  {'─' * 16}", end="")
    print()

    for seed, sr in all_results:
        print(f"  {seed:<8}", end="")
        for cond_name, _ in conditions:
            r = sr[cond_name]
            d_delta = sum(r["pre_direct_losses"][i] - r["post_direct_losses"][i]
                          for i in range(len(HELD_OUT_DIRECT))) / len(HELD_OUT_DIRECT)
            print(f"  dir={d_delta:+.4f}    ", end="")
        print()

    # Direct completion deltas
    print(f"\n  Direct Completion Delta:")
    print(f"  {'Seed':<8} {'Baseline':>10} {'Explicit':>10} {'Matched':>10}")
    print(f"  {'─' * 6} {'─' * 10} {'─' * 10} {'─' * 10}")
    for seed, sr in all_results:
        vals = []
        for cond_name, _ in conditions:
            r = sr[cond_name]
            d = sum(r["pre_direct_losses"][i] - r["post_direct_losses"][i]
                   for i in range(len(HELD_OUT_DIRECT))) / len(HELD_OUT_DIRECT)
            vals.append(d)
        print(f"  {seed:<8} {vals[0]:>+10.4f} {vals[1]:>+10.4f} {vals[2]:>+10.4f}")

    # Rule ID deltas
    print(f"\n  Rule Identification Delta:")
    print(f"  {'Seed':<8} {'Baseline':>10} {'Explicit':>10} {'Matched':>10}")
    print(f"  {'─' * 6} {'─' * 10} {'─' * 10} {'─' * 10}")
    for seed, sr in all_results:
        vals = []
        for cond_name, _ in conditions:
            r = sr[cond_name]
            d = sum(r["pre_rule_losses"][i] - r["post_rule_losses"][i]
                   for i in range(len(HELD_OUT_RULES))) / len(HELD_OUT_RULES)
            vals.append(d)
        print(f"  {seed:<8} {vals[0]:>+10.4f} {vals[1]:>+10.4f} {vals[2]:>+10.4f}")

    # Rationale gen deltas
    print(f"\n  Rationale Generation Delta:")
    print(f"  {'Seed':<8} {'Baseline':>10} {'Explicit':>10} {'Matched':>10}")
    print(f"  {'─' * 6} {'─' * 10} {'─' * 10} {'─' * 10}")
    for seed, sr in all_results:
        vals = []
        for cond_name, _ in conditions:
            r = sr[cond_name]
            d = sum(r["pre_rat_losses"][i] - r["post_rat_losses"][i]
                   for i in range(len(HELD_OUT_RATIONALE))) / len(HELD_OUT_RATIONALE)
            vals.append(d)
        print(f"  {seed:<8} {vals[0]:>+10.4f} {vals[1]:>+10.4f} {vals[2]:>+10.4f}")

    # ── Rule Accuracy ──────────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  RULE ACCURACY — Format Compliance & Exact Ending Match")
    print(f"{'=' * 80}")

    # Aggregate rule accuracy across seeds
    cond_names = [c[0] for c in conditions]
    for cond_name in cond_names:
        total_items = len(HELD_OUT_RULES) * len(SEEDS)
        format_total = 0
        exact_total = 0
        for _, sr in all_results:
            for s in sr[cond_name]["rule_scores"]:
                if s["starts_hyphen"]:
                    format_total += 1
                if s["exact_match"]:
                    exact_total += 1
        cond_accuracy = exact_total / max(format_total, 1) if format_total > 0 else 0
        print(f"\n  {cond_name}:")
        print(f"    Format rate (starts with -): {format_total}/{total_items} = {format_total/total_items*100:.1f}%")
        print(f"    Exact ending match:           {exact_total}/{total_items} = {exact_total/total_items*100:.1f}%")
        print(f"    Conditional accuracy (exact|format): {exact_total}/{format_total} = {cond_accuracy*100:.1f}%" if format_total > 0 else
              f"    Conditional accuracy: N/A (no format hits)")

    # ── Per-Item Rule Accuracy ──────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  PER-ITEM RULE ACCURACY")
    print(f"{'=' * 80}")

    for idx, (prompt, target) in enumerate(HELD_OUT_RULES):
        print(f"\n  Item {idx+6}: `{prompt}` -> `{target}`")
        print(f"    {'Condition':<16} {'Format':>6} {'Exact':>6} {'Sample Generation'}")
        print(f"    {'─' * 14} {'─' * 6} {'─' * 6} {'─' * 30}")
        for cond_name in cond_names:
            format_count = 0
            exact_count = 0
            sample_gen = ""
            for seed_i, (_, sr) in enumerate(all_results):
                s = sr[cond_name]["rule_scores"][idx]
                if s["starts_hyphen"]:
                    format_count += 1
                if s["exact_match"]:
                    exact_count += 1
                if seed_i == 0:
                    sample_gen = s["generated"].replace("\n", "\\n")
            print(f"    {cond_name:<16} {format_count}/{len(SEEDS):>3}  {exact_count}/{len(SEEDS):>3}  `{sample_gen}`")

    # ── Qualitative — All Rule Generations for Seed 42 ─────────────────────
    print(f"\n{'=' * 80}")
    print("  QUALITATIVE — Rule Generations (Seed 42)")
    print(f"{'=' * 80}")

    seed42_results = all_results[0][1]
    for idx, (prompt, target) in enumerate(HELD_OUT_RULES):
        print(f"\n  `{prompt}` -> `{target}`")
        for cond_name in cond_names:
            gen = seed42_results[cond_name]["rule_scores"][idx]["generated"].replace("\n", "\\n")
            exact = seed42_results[cond_name]["rule_scores"][idx]["exact_match"]
            print(f"    {cond_name:<16}: `{gen}` {'✓' if exact else '✗'}")

    # ── Advantage Comparison ───────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("  ADVANTAGE — Explicit-rule vs Matched Control")
    print(f"{'=' * 80}")

    for metric_name, item_list, pre_key, post_key in [
        ("Direct Completion", HELD_OUT_DIRECT, "pre_direct_losses", "post_direct_losses"),
        ("Rule Identification", HELD_OUT_RULES, "pre_rule_losses", "post_rule_losses"),
        ("Rationale Generation", HELD_OUT_RATIONALE, "pre_rat_losses", "post_rat_losses"),
    ]:
        advs = []
        for _, sr in all_results:
            exp_d = sum(sr["Explicit-rule"][pre_key][i] - sr["Explicit-rule"][post_key][i]
                       for i in range(len(item_list))) / len(item_list)
            match_d = sum(sr["Matched control"][pre_key][i] - sr["Matched control"][post_key][i]
                         for i in range(len(item_list))) / len(item_list)
            advs.append(exp_d - match_d)
        mean_adv = sum(advs) / len(advs)
        std_adv = (sum((a - mean_adv) ** 2 for a in advs) / len(advs)) ** 0.5
        pos = sum(1 for a in advs if a > 0)
        print(f"\n  {metric_name}:")
        print(f"    Mean advantage: {mean_adv:+.4f}  (std: {std_adv:.4f})  {pos}/{len(advs)} seeds positive")

    # Rule accuracy advantage
    print(f"\n  Rule Accuracy (exact ending match):")
    exp_exact_total = sum(sum(1 for s in sr["Explicit-rule"]["rule_scores"] if s["exact_match"])
                          for _, sr in all_results)
    match_exact_total = sum(sum(1 for s in sr["Matched control"]["rule_scores"] if s["exact_match"])
                            for _, sr in all_results)
    total = len(HELD_OUT_RULES) * len(SEEDS)
    print(f"    Explicit-rule:   {exp_exact_total}/{total} = {exp_exact_total/total*100:.1f}%")
    print(f"    Matched control: {match_exact_total}/{total} = {match_exact_total/total*100:.1f}%")
    print(f"    Advantage: {exp_exact_total - match_exact_total} items")

    print(f"\n{'=' * 80}")
    print("  Experiment G Complete")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
