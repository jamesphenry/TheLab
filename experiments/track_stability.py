#!/usr/bin/env python3
"""Track stability across checkpoints on fixed probe set"""
from __future__ import annotations

import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

def track_stability(seed=123, iterations=30):
    torch.manual_seed(seed)
    config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
    tokenizer = BabyTokenizer()
    model = BabyLM(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    
    # Training exemplars (never include probes)
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
    
    # Fixed probe set
    probes = [
        ("a b c ", "d"),
        ("f g h ", "i"),
        ("h i j ", "k"),
        ("r s t ", "u"),
    ]
    
    # Held-out probes (different)
    held_probes = [
        ("g h i ", "j"),
        ("n o p ", "q"),
        ("s t u ", "v"),
        ("p q r ", "s"),
    ]
    
    results = []
    for iter in range(iterations + 1):
        if iter > 0:
            for text in exemplars:
                tokens = tokenizer.encode(text, add_special_tokens=False)
                if len(tokens) <= 1: continue
                input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
                target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
                loss = model.train_step(input_ids, target_ids, optimizer)
        
        # Evaluate probes
        model.eval()
        probe_stats = []
        for prompt, expected in probes:
            prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
            expected_tokens = tokenizer.encode(expected, add_special_tokens=False)
            exp_token = expected_tokens[0]
            
            with torch.no_grad():
                input_ids = torch.tensor([prompt_tokens], dtype=torch.long)
                logits, _ = model(input_ids, None)
                probs = torch.softmax(logits[0, -1, :], dim=-1)
                exp_prob = probs[exp_token].item()
                sorted_probs, sorted_idx = torch.sort(probs, descending=True)
                rank = (sorted_idx == exp_token).nonzero(as_tuple=True)[0].item() + 1
                top_token = tokenizer.decode([sorted_idx[0].item()])
            probe_stats.append({"prompt": prompt, "expected": expected, "prob": exp_prob, "rank": rank, "top": top_token})
        
        # Evaluate held-out
        held_correct = 0
        for prompt, expected in held_probes:
            prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
            current = torch.tensor([prompt_tokens], dtype=torch.long)
            for _ in range(1):
                with torch.no_grad():
                    logits, _ = model(current, None)
                    next_token = torch.argmax(logits[:, -1, :], dim=-1)
                    current = torch.cat([current, next_token.unsqueeze(0)], dim=1)
            generated = tokenizer.decode(current[0].tolist())
            completion = generated[len(prompt):].strip()
            if completion == expected.strip():
                held_correct += 1
        held_acc = held_correct / len(held_probes)
        
        # Training loss (on a sample)
        train_loss = 0
        for text in exemplars[:3]:
            tokens = tokenizer.encode(text, add_special_tokens=False)
            if len(tokens) <= 1: continue
            input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
            target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
            with torch.no_grad():
                _, loss = model(input_ids, target_ids)
                if loss is not None: train_loss += loss.item()
        train_loss /= 3
        
        print(f"Iter {iter:2d}: train_loss={train_loss:.4f}, held_acc={held_acc:.2%}, probes: " + 
              ", ".join([f"{p['prompt'].strip()}->{p['expected']} r{p['rank']}({p['prob']:.3f})" for p in probe_stats]))
        
        results.append({
            "iter": iter,
            "train_loss": train_loss,
            "held_acc": held_acc,
            "probes": probe_stats
        })
    
    return results

if __name__ == "__main__":
    for seed in [42, 123]:
        print(f"\n\n{'#'*60}")
        print(f"SEED {seed}")
        print(f"{'#'*60}")
        results = track_stability(seed=seed, iterations=25)
