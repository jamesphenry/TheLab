#!/usr/bin/env python3
"""Test larger model size for comparison"""
from __future__ import annotations

import time
import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

def test_model_size(seed=123, larger=False):
    start_time = time.time()
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
    params = model.get_num_params()
    print(f"Model size: {params:,} params ({'LARGE' if larger else 'SMALL'})")
    
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
    best_loss = float('inf')
    final_acc = 0
    final_loss = 0
    
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
            # Compute held-out loss
            held_loss = 0
            for prompt, target in held_out:
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
                    if loss is not None: held_loss += loss.item()
            held_loss /= len(held_out)
            
            # Greedy accuracy
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
                best_loss = held_loss
            if iter == 30:
                final_acc = acc
                final_loss = held_loss
            print(f"Iter {iter:2d}: held_loss={held_loss:.4f}, acc={acc:.2%} ({correct}/12)")
    
    elapsed = time.time() - start_time
    print(f"Elapsed: {elapsed:.1f}s, Best: iter {best_iter}, acc={best_acc:.2%}, Final: acc={final_acc:.2%}, Gap: {best_acc-final_acc:.2%}")
    return {
        "params": params,
        "best_acc": best_acc,
        "best_iter": best_iter,
        "final_acc": final_acc,
        "final_loss": final_loss,
        "gap": best_acc - final_acc,
        "elapsed": elapsed
    }

if __name__ == "__main__":
    print("=== SMALL MODEL (27M) ===")
    small = test_model_size(seed=123, larger=False)
    print("\n=== LARGE MODEL (~109M) ===")
    large = test_model_size(seed=123, larger=True)
    print(f"\n=== COMPARISON ===")
    print(f"Small: {small['params']:,} params, best={small['best_acc']:.2%} (iter {small['best_iter']}), final={small['final_acc']:.2%}, gap={small['gap']:.2%}, time={small['elapsed']:.1f}s")
    print(f"Large: {large['params']:,} params, best={large['best_acc']:.2%} (iter {large['best_iter']}), final={large['final_acc']:.2%}, gap={large['gap']:.2%}, time={large['elapsed']:.1f}s")
    print(f"Improvement in best acc: {large['best_acc']-small['best_acc']:+.2%}")
