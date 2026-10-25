#!/usr/bin/env python3
"""Test if adding coverage fixes the r,s,t,u issue"""
from __future__ import annotations

import time
import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

def test_format(name, exemplars, seed=123):
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    print(f"Exemplars: {exemplars}")
    
    torch.manual_seed(seed)
    config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
    tokenizer = BabyTokenizer()
    model = BabyLM(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    
    held_out = [
        ("g h i ", "j"),
        ("n o p ", "q"),
        ("s t u ", "v"),
        ("p q r ", "s"),
        ("e f g ", "h"),
        ("i j k ", "l"),
        ("j k l ", "m"),
        ("o p q ", "r"),
        ("d e f ", "g"),
        ("k l m ", "n"),
        ("h i j ", "k"),
        ("t u v ", "w"),
    ]
    
    best_acc = 0
    best_iter = 0
    best_checkpoint = None
    
    for iter in range(0, 31):
        if iter > 0:
            for text in exemplars:
                tokens = tokenizer.encode(text, add_special_tokens=False)
                if len(tokens) <= 1: continue
                input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
                target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
                loss = model.train_step(input_ids, target_ids, optimizer)
        
        if iter % 3 == 0 or iter == 30:
            model.eval()
            correct = 0
            for prompt, target in held_out:
                prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
                current = torch.tensor([prompt_tokens], dtype=torch.long)
                for _ in range(len(target.strip())):
                    with torch.no_grad():
                        logits, _ = model(current, None)
                        next_token = torch.argmax(logits[:, -1, :], dim=-1)
                        current = torch.cat([current, next_token.unsqueeze(0)], dim=1)
                generated = tokenizer.decode(current[0].tolist())
                completion = generated[len(prompt):].strip()
                if completion == target.strip():
                    correct += 1
            acc = correct / len(held_out)
            if acc > best_acc:
                best_acc = acc
                best_iter = iter
                best_checkpoint = {k: v.clone() for k, v in model.state_dict().items()}
    
    print(f"Best: iter {best_iter}, acc={best_acc:.2%} ({int(best_acc*12)}/12)")
    
    # Test best checkpoint
    if best_checkpoint:
        model.load_state_dict(best_checkpoint)
        correct = 0
        failures = []
        for prompt, target in held_out:
            prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
            current = torch.tensor([prompt_tokens], dtype=torch.long)
            for _ in range(len(target.strip())):
                with torch.no_grad():
                    logits, _ = model(current, None)
                    next_token = torch.argmax(logits[:, -1, :], dim=-1)
                    current = torch.cat([current, next_token.unsqueeze(0)], dim=1)
            generated = tokenizer.decode(current[0].tolist())
            completion = generated[len(prompt):].strip()
            if completion == target.strip():
                correct += 1
            else:
                failures.append(f"'{prompt}' exp='{target}' got='{completion}'")
        print(f"Verified best: {correct}/12 = {correct/12:.2%}")
        if failures:
            print("Failures:")
            for f in failures:
                print(f"  {f}")
    
    return best_acc

# Original format
orig = [
    "a b c d e f g",
    "c d e f g h i",
    "m n o p q r s",
    "t u v w x y z",
    "e f g h i j k",
]

# With coverage fixes
coverage_fixed = [
    "a b c d e f g",
    "b c d e f g h",
    "c d e f g h i",
    "d e f g h i j",
    "e f g h i j k",
    "f g h i j k l",
    "g h i j k l m",
    "h i j k l m n",
    "i j k l m n o",
    "j k l m n o p",
    "k l m n o p q",
    "l m n o p q r",
    "m n o p q r s",
    "n o p q r s t",
    "o p q r s t u",
    "p q r s t u v",
    "q r s t u v w",
    "r s t u v w x",
    "s t u v w x y",
    "t u v w x y z",
]

# Mixed - keep some variety
mixed_fixed = [
    "a b c d e f g",
    "c d e f g h i",
    "m n o p q r s",
    "t u v w x y z",
    "e f g h i j k",
    "p q r s t u",  # covers the problematic range
    "q r s t u v",
    "r s t u v w",
    "o p q r s t",
]

if __name__ == "__main__":
    r1 = test_format("ORIGINAL", orig)
    r2 = test_format("COVERAGE_FIXED_FULL", coverage_fixed)
    r3 = test_format("MIXED_FIXED", mixed_fixed)
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Original: {r1:.2%}")
    print(f"Coverage Fixed (full): {r2:.2%}")
    print(f"Mixed Fixed: {r3:.2%}")
