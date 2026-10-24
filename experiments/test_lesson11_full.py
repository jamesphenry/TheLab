#!/usr/bin/env python3
"""Test Lesson 1.1 with full lesson format"""
from __future__ import annotations

import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

def test_lesson(seeds=[42, 123, 7], iterations=20):
    # Full format from lesson
    exemplars = [
        "a b c d e f g",
        "c d e f g h i",
        "m n o p q r s",
        "t u v w x y z",
        "e f g h i j k",
        "a b c ",
        "f g h ",
        "p q r ",
        "v w x ",
        "z y x w v u",
        "z y x ",
        "m l k ",
    ]
    
    training_adj = [
        ("h i j ", "k"),
        ("r s t ", "u"),
        ("d e f ", "g"),
    ]
    held_out = [
        ("g h i ", "j"),
        ("n o p ", "q"),
        ("s t u ", "v"),
    ]
    all_test = training_adj + held_out
    
    results = []
    for seed in seeds:
        print(f"\n=== Seed {seed} ===")
        torch.manual_seed(seed)
        config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
        tokenizer = BabyTokenizer()
        model = BabyLM(config)
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
        
        # Baseline
        model.eval()
        baseline_loss = 0
        for prompt, target in all_test:
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
        baseline_loss /= len(all_test)
        
        # Train
        for iter in range(iterations):
            for text in exemplars:
                tokens = tokenizer.encode(text, add_special_tokens=False)
                if len(tokens) <= 1: continue
                input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
                target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
                loss = model.train_step(input_ids, target_ids, optimizer)
        
        # Post
        model.eval()
        post_loss_held = 0
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
                if loss is not None: post_loss_held += loss.item()
        post_loss_held /= len(held_out)
        
        # Greedy
        correct_held = 0
        for prompt, target in held_out:
            prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
            current = torch.tensor([prompt_tokens], dtype=torch.long)
            for _ in range(1):
                with torch.no_grad():
                    logits, _ = model(current, None)
                    next_token = torch.argmax(logits[:, -1, :], dim=-1)
                    current = torch.cat([current, next_token.unsqueeze(0)], dim=1)
            generated = tokenizer.decode(current[0].tolist())
            completion = generated[len(prompt):].strip()
            is_correct = (completion == target.strip())
            if is_correct: correct_held += 1
            print(f"  '{prompt}' -> '{completion}' (exp '{target}'): {is_correct}")
        
        acc_held = correct_held / len(held_out)
        delta_held = baseline_loss - post_loss_held  # rough
        print(f"Greedy acc held: {acc_held:.2%}")
        results.append({"seed": seed, "acc_held": acc_held})
    
    avg_acc = sum(r['acc_held'] for r in results)/len(results)
    print(f"\nAVG greedy acc held: {avg_acc:.2%}")

if __name__ == "__main__":
    test_lesson()
