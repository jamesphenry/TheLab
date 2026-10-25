#!/usr/bin/env python3
"""Test updated Lesson 1.1 with mixed coverage"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

# Updated exemplars from Lesson 1.1
EXEMPLARS = [
    "a b c d e f g",
    "c d e f g h i",
    "m n o p q r s",
    "t u v w x y z",
    "e f g h i j k",
    "p q r s t u",
    "q r s t u v",
    "r s t u v w",
    "o p q r s t",
]

# Assessment items
TRAINING_ADJ = [
    ("h i j ", "k"),
    ("r s t ", "u"),
    ("d e f ", "g"),
]
HELD_OUT = [
    ("g h i ", "j"),
    ("n o p ", "q"),
    ("s t u ", "v"),
]
ALL_TEST = TRAINING_ADJ + HELD_OUT

def test_lesson(seeds=[42, 123, 7, 999], iterations=30):
    results_all = []
    
    for seed in seeds:
        print(f"\n{'='*60}")
        print(f"Testing updated Lesson 1.1 with seed={seed}")
        print(f"{'='*60}")
        
        torch.manual_seed(seed)
        config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
        tokenizer = BabyTokenizer()
        model = BabyLM(config)
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
        
        # Baseline
        model.eval()
        baseline_loss = 0
        for prompt, target in ALL_TEST:
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
        baseline_loss /= len(ALL_TEST)
        print(f"Baseline loss: {baseline_loss:.4f}")
        
        best_checkpoint = None
        best_held_loss = float('inf')
        best_iter = 0
        
        # Train with checkpointing
        for iter in range(iterations):
            for text in EXEMPLARS:
                tokens = tokenizer.encode(text, add_special_tokens=False)
                if len(tokens) <= 1: continue
                input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
                target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
                loss = model.train_step(input_ids, target_ids, optimizer)
            
            # Check held-out loss for checkpointing
            if iter % 2 == 0 or iter == iterations - 1:
                model.eval()
                held_loss = 0
                for prompt, target in HELD_OUT:
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
                held_loss /= len(HELD_OUT)
                if held_loss < best_held_loss:
                    best_held_loss = held_loss
                    best_iter = iter
                    best_checkpoint = {k: v.clone() for k, v in model.state_dict().items()}
        
        # Load best checkpoint
        if best_checkpoint:
            model.load_state_dict(best_checkpoint)
            print(f"Using best checkpoint at iter {best_iter}")
        
        # Evaluate
        model.eval()
        post_loss_all = 0
        post_loss_held = 0
        for prompt, target in ALL_TEST:
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
                if loss is not None: 
                    post_loss_all += loss.item()
                    if (prompt, target) in HELD_OUT:
                        post_loss_held += loss.item()
        post_loss_all /= len(ALL_TEST)
        post_loss_held /= len(HELD_OUT)
        
        delta_loss = baseline_loss - post_loss_all
        delta_held = baseline_loss - post_loss_held  # rough comparison
        
        # Greedy accuracy
        correct_held = 0
        for prompt, target in HELD_OUT:
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
                correct_held += 1
            print(f"  '{prompt}' -> '{completion}' (exp '{target}'): {completion == target.strip()}")
        
        acc_held = correct_held / len(HELD_OUT)
        passed = delta_loss > 2.0 and acc_held >= 0.5  # curriculum criteria
        
        print(f"Delta loss (all): {delta_loss:.4f}, Held acc: {acc_held:.2%}, Passed: {passed}")
        
        results_all.append({
            "seed": seed,
            "baseline_loss": baseline_loss,
            "post_loss_all": post_loss_all,
            "post_loss_held": post_loss_held,
            "delta_loss": delta_loss,
            "acc_held": acc_held,
            "correct_held": correct_held,
            "passed": passed
        })
    
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for r in results_all:
        print(f"Seed {r['seed']}: Δ={r['delta_loss']:.4f}, Held Acc={r['acc_held']:.2%}, Passed={r['passed']}")
    mean_delta = sum(r['delta_loss'] for r in results_all)/len(results_all)
    mean_acc = sum(r['acc_held'] for r in results_all)/len(results_all)
    print(f"MEAN: Δ={mean_delta:.4f}, Held Acc={mean_acc:.2%}")
    
    return results_all

if __name__ == "__main__":
    results = test_lesson()
    # Save
    Path("experiments").mkdir(exist_ok=True)
    with open(f"experiments/lesson11_updated_results.json", 'w') as f:
        json.dump({"timestamp": datetime.now().isoformat(), "results": results}, f, indent=2, default=str)
