#!/usr/bin/env python3
"""Compare training formats"""
from __future__ import annotations

import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

def test_format(name, exemplars, seeds=[42, 123, 7], iterations=15):
    print(f"\n{'='*60}")
    print(f"EXPERIMENT {name}: {exemplars}")
    print(f"{'='*60}")

    held_out_prompts = [
        ("g h i ", "j"),
        ("n o p ", "q"),
        ("s t u ", "v"),
    ]

    results = []
    for seed in seeds:
        torch.manual_seed(seed)
        config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
        tokenizer = BabyTokenizer()
        model = BabyLM(config)
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

        # Baseline
        model.eval()
        baseline_loss = 0
        for prompt, target in held_out_prompts:
            full_text = prompt + target
            tokens = tokenizer.encode(full_text, add_special_tokens=False)
            prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
            if len(tokens) <= 1: continue
            input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
            target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
            mask_len = len(prompt_tokens) - 1
            if mask_len > 0: target_ids[:, :mask_len] = -1
            with torch.no_grad():
                _, loss = model(input_ids, target_ids)
                if loss is not None: baseline_loss += loss.item()
        baseline_loss /= len(held_out_prompts)

        # Train
        for iter in range(iterations):
            for text in exemplars:
                tokens = tokenizer.encode(text, add_special_tokens=False)
                if len(tokens) <= 1: continue
                input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
                target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
                loss = model.train_step(input_ids, target_ids, optimizer)

        # Post eval - loss
        model.eval()
        post_loss = 0
        for prompt, target in held_out_prompts:
            full_text = prompt + target
            tokens = tokenizer.encode(full_text, add_special_tokens=False)
            prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
            if len(tokens) <= 1: continue
            input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
            target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
            mask_len = len(prompt_tokens) - 1
            if mask_len > 0: target_ids[:, :mask_len] = -1
            with torch.no_grad():
                _, loss = model(input_ids, target_ids)
                if loss is not None: post_loss += loss.item()
        post_loss /= len(held_out_prompts)

        # Greedy accuracy
        correct = 0
        for prompt, target in held_out_prompts:
            prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
            current = torch.tensor([prompt_tokens], dtype=torch.long)
            for _ in range(1):
                with torch.no_grad():
                    logits, _ = model(current, None)
                    next_token = torch.argmax(logits[:, -1, :], dim=-1)
                    current = torch.cat([current, next_token.unsqueeze(0)], dim=1)
            generated = tokenizer.decode(current[0].tolist())
            completion = generated[len(prompt):].strip()
            if completion == target.strip() or completion.startswith(target.strip()):
                correct += 1

        delta = baseline_loss - post_loss
        acc = correct / len(held_out_prompts)
        print(f"  Seed {seed}: baseline={baseline_loss:.4f}, post={post_loss:.4f}, Δ={delta:+.4f}, greedy_acc={acc:.2%}")
        results.append({"seed": seed, "delta": delta, "acc": acc})

    avg_delta = sum(r["delta"] for r in results) / len(results)
    avg_acc = sum(r["acc"] for r in results) / len(results)
    print(f"  AVG: Δ={avg_delta:+.4f}, greedy_acc={avg_acc:.2%}")
    return results

# Run experiments
A = test_format("A - Full sequences", [
    "a b c d e f g",
    "b c d e f g h",
    "c d e f g h i",
    "d e f g h i j",
    "e f g h i j k",
    "f g h i j k l",
    "m n o p q r s",
    "n o p q r s t",
])

B = test_format("B - Explicit prefix-completion", [
    "a b c  -> d",
    "b c d  -> e",
    "c d e  -> f",
    "f g h  -> i",
    "m n o  -> p",
    "r s t  -> u",
    "x y z  -> ",
    "a b c  d",  # space separated
    "f g h  i",
])

C = test_format("C - Mixed", [
    "a b c d e f g",
    "c d e f g h i",
    "m n o p q r s",
    "a b c  -> d",
    "f g h  -> i",
    "n o p  -> q",
])
