#!/usr/bin/env python3
"""Comprehensive diagnostic addressing all points"""
from __future__ import annotations

import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

def comprehensive_diagnostic(seed=123):
    torch.manual_seed(seed)
    config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
    tokenizer = BabyTokenizer()
    model = BabyLM(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    
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
    
    # Expanded held-out set (12 examples)
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
    
    best_checkpoint = None
    best_held_acc = -1
    best_iter = 0
    
    print("=== COMPREHENSIVE DIAGNOSTIC ===")
    print(f"Seed: {seed}")
    print(f"Held-out set size: {len(held_out)}")
    print()
    
    for iter in range(0, 31):
        if iter > 0:
            for text in exemplars:
                tokens = tokenizer.encode(text, add_special_tokens=False)
                if len(tokens) <= 1: continue
                input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
                target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
                loss = model.train_step(input_ids, target_ids, optimizer)
        
        # Evaluate held-out loss
        model.eval()
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
        
        # Greedy accuracy - check all tokens
        correct = 0
        for prompt, target in held_out:
            prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
            current = torch.tensor([prompt_tokens], dtype=torch.long)
            # Generate exactly len(target) tokens
            for _ in range(len(target.strip())):
                with torch.no_grad():
                    logits, _ = model(current, None)
                    next_token = torch.argmax(logits[:, -1, :], dim=-1)
                    current = torch.cat([current, next_token.unsqueeze(0)], dim=1)
            generated = tokenizer.decode(current[0].tolist())
            completion = generated[len(prompt):].strip()
            if completion == target.strip():
                correct += 1
        held_acc = correct / len(held_out)
        
        if held_acc > best_held_acc:
            best_held_acc = held_acc
            best_iter = iter
            # Save checkpoint state
            best_checkpoint = {k: v.clone() for k, v in model.state_dict().items()}
        
        if iter % 5 == 0 or held_acc > 0:
            print(f"Iter {iter:2d}: held_loss={held_loss:.4f}, held_acc={held_acc:.2%} ({correct}/{len(held_out)})")
    
    print(f"\nBest checkpoint: iter {best_iter}, acc={best_held_acc:.2%}")
    print(f"Final checkpoint: acc={held_acc:.2%}")
    
    # Test best checkpoint
    if best_checkpoint is not None:
        model.load_state_dict(best_checkpoint)
        correct_best = 0
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
                correct_best += 1
        print(f"Best checkpoint tested: {correct_best}/{len(held_out)} = {correct_best/len(held_out):.2%}")
    
    # Detailed look at failures
    print(f"\n=== Detailed failures at best checkpoint ===")
    model.load_state_dict(best_checkpoint) if best_checkpoint else None
    for prompt, target in held_out:
        prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
        current = torch.tensor([prompt_tokens], dtype=torch.long)
        # Track each token
        tokens_generated = []
        for step in range(len(target.strip())):
            with torch.no_grad():
                logits, _ = model(current, None)
                probs = torch.softmax(logits[0, -1, :], dim=-1)
                next_token = torch.argmax(logits[:, -1, :], dim=-1)
                tokens_generated.append(next_token.item())
                # Check rank of expected
                expected_token = tokenizer.encode(target.strip()[step] if step < len(target.strip()) else '')[0] if target.strip() else None
                if expected_token and step == 0:  # just first token
                    sorted_probs, sorted_idx = torch.sort(probs, descending=True)
                    rank = (sorted_idx == expected_token).nonzero(as_tuple=True)[0].item() + 1
                current = torch.cat([current, next_token.unsqueeze(0)], dim=1)
        generated = tokenizer.decode(current[0].tolist())
        completion = generated[len(prompt):].strip()
        if completion != target.strip():
            print(f"  '{prompt}' exp='{target}' got='{completion}'")
        else:
            print(f"  '{prompt}' exp='{target}' got='{completion}' ✓")

if __name__ == "__main__":
    comprehensive_diagnostic(seed=123)
