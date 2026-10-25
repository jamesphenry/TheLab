#!/usr/bin/env python3
"""Test larger model size for comparison"""
from __future__ import annotations

import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

def test_model_size(seed=123, larger=False):
    torch.manual_seed(seed)
    if larger:
        # Double size - 16 layers, 1024 dim
        config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=1024, n_layers=16, n_heads=16)
    else:
        # Original - 8 layers, 512 dim
        config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
    
    tokenizer = BabyTokenizer()
    model = BabyLM(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    print(f"Model size: {model.get_num_params():,} params ({'LARGE' if larger else 'SMALL'})")
    
    exemplars = [
        "a b c d e f g",
        "b c d e f g h",
        "c d e f g h i",
        "d e f g h i j",
        "e f g h i j k",
        "f g h i j k l",
        "m n o p q r s",
        "n o p q r s t",
    ]
    
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
    
    for iter in range(0, 31):
        if iter > 0:
            for text in exemplars:
                tokens = tokenizer.encode(text, add_special_tokens=False)
                if len(tokens) <= 1: continue
                input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
                target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
                loss = model.train_step(input_ids, target_ids, optimizer)
        
        if iter % 5 == 0 or iter == 30:
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
            print(f"Iter {iter:2d}: acc={acc:.2%} ({correct}/12)")
    
    print(f"Best: iter {best_iter}, acc={best_acc:.2%}")
    return best_acc

if __name__ == "__main__":
    print("=== SMALL MODEL ===")
    small = test_model_size(seed=123, larger=False)
    print("\n=== LARGE MODEL (2x) ===")
    large = test_model_size(seed=123, larger=True)
    print(f"\nComparison: small={small:.2%}, large={large:.2%}, improvement={large-small:+.2%}")
