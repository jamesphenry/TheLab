#!/usr/bin/env python3
"""
Throwaway harness to test the preschool curriculum plan.

Distinguishes:
- training loss (per-step)
- held-out loss (cross-entropy on completions, prompt-masked)
- generated-answer accuracy (does the generated completion match the target pattern?)
"""
from __future__ import annotations

import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

import torch

from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer
from harness.vault.controller import VaultController, Role


class PreschoolTester:
    def __init__(self, vault_root: str = "vault", device: str = None):
        self.vault = VaultController(vault_root)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BabyTokenizer()
    
    def init_fresh_student(self, seed: int, config: BabyLMConfig = None):
        """Initialize a fresh student (model + optimizer) with given seed."""
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        random.seed(seed)
        
        if config is None:
            config = BabyLMConfig(
                vocab_size=4096,
                max_seq_len=256,
                dim=512,
                n_layers=8,
                n_heads=8,
                device=self.device,
            )
        model = BabyLM(config).to(self.device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
        return model, optimizer
    
    def compute_training_loss(self, model: BabyLM, optimizer: torch.optim.Optimizer, 
                             exemplars: List[str]) -> float:
        """Compute average training loss on exemplars (one pass)."""
        model.train()
        total_loss = 0.0
        count = 0
        for text in exemplars:
            tokens = self.tokenizer.encode(text, add_special_tokens=True)
            if len(tokens) <= 1:
                continue
            input_ids = torch.tensor([tokens[:-1]], dtype=torch.long, device=self.device)
            target_ids = torch.tensor([tokens[1:]], dtype=torch.long, device=self.device)
            loss = model.train_step(input_ids, target_ids, optimizer)
            total_loss += loss
            count += 1
        return total_loss / max(count, 1)
    
    def train_on_exemplars(self, model: BabyLM, optimizer: torch.optim.Optimizer,
                          exemplars: List[str], iterations: int = 15) -> List[float]:
        """Train for multiple iterations, return per-iteration training losses."""
        training_losses = []
        for _ in range(iterations):
            loss = self.compute_training_loss(model, optimizer, exemplars)
            training_losses.append(loss)
        return training_losses
    
    def evaluate_loss(self, model: BabyLM, test_items: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Evaluate held-out/training-adjacent loss with prompt masking."""
        model.eval()
        item_results = []
        total_loss = 0.0
        for prompt, target in test_items:
            full_text = prompt + target
            tokens = self.tokenizer.encode(full_text, add_special_tokens=False)
            prompt_tokens = self.tokenizer.encode(prompt, add_special_tokens=False)
            if len(tokens) <= 1:
                continue
            input_ids = torch.tensor([tokens[:-1]], dtype=torch.long, device=self.device)
            target_ids = torch.tensor([tokens[1:]], dtype=torch.long, device=self.device)
            mask_len = len(prompt_tokens) - 1
            if mask_len > 0:
                target_ids[:, :mask_len] = -1
            with torch.no_grad():
                _, loss = model(input_ids, target_ids)
                loss_val = float(loss.item()) if loss is not None else float('inf')
                total_loss += loss_val
            item_results.append({
                "prompt": prompt,
                "target": target,
                "loss": loss_val,
            })
        avg_loss = total_loss / max(len(item_results), 1)
        return {"avg_loss": avg_loss, "items": item_results}
    
    def evaluate_generation_accuracy(self, model: BabyLM, test_items: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Evaluate generated answer accuracy."""
        model.eval()
        item_results = []
        correct = 0
        total = 0
        for prompt, target in test_items:
            prompt_tokens = self.tokenizer.encode(prompt, add_special_tokens=False)
            prompt_tensor = torch.tensor([prompt_tokens], dtype=torch.long, device=self.device)
            generated_ids = model.generate(
                prompt_tensor,
                max_new_tokens=len(target) + 3,
                temperature=0.8
            )
            generated_text = self.tokenizer.decode(generated_ids[0].tolist())
            # Extract completion after prompt
            if generated_text.startswith(prompt):
                completion = generated_text[len(prompt):]
            else:
                completion = generated_text
            # Check for exact match or startswith target (accounting for punctuation)
            is_correct = (completion.strip() == target.strip()) or completion.strip().startswith(target.strip()) or target.strip() in completion.strip()
            if is_correct:
                correct += 1
            total += 1
            item_results.append({
                "prompt": prompt,
                "target": target,
                "generated": generated_text,
                "completion": completion,
                "correct": is_correct,
            })
        accuracy = correct / max(total, 1)
        return {"accuracy": accuracy, "correct": correct, "total": total, "items": item_results}
    
    def test_lesson_1_1(self, seeds: List[int] = [42, 123, 7], iterations: int = 15) -> Dict[str, Any]:
        """Test Lesson 1.1: Alphabet Sequences from beginning to end."""
        results_all = []
        
        # Define exemplars from Lesson 1.1
        exemplars = [
            "a b c d e f g",
            "c d e f g h i",
            "m n o p q r s",
            "t u v w x y z",
            "e f g h i j k",
            "a b c " + "->" + " d",  # pattern form
        ]
        # Better format - space separated
        exemplars = [
            "a b c d e f g ",
            "c d e f g h i ",
            "m n o p q r s ",
            "t u v w x y z ",
            "e f g h i j k ",
            "a b c  d",  # space separation style
        ]
        # Use the actual style from lesson - space separated sequences
        exemplars = [
            "a b c d e f g",
            "c d e f g h i",
            "m n o p q r s",
            "t u v w x y z",
            "e f g h i j k",
            "a b c ",  # prefix for completion
            "f g h ",
            "p q r ",
            "v w x ",
        ]
        
        # Training-adjacent test items (similar to seen patterns)
        training_adj = [
            ("h i j ", "k"),
            ("r s t ", "u"),
            ("d e f ", "g"),
        ]
        
        # Held-out test items
        held_out = [
            ("g h i ", "j"),
            ("n o p ", "q"),
            ("s t u ", "v"),
        ]
        
        all_test = training_adj + held_out
        
        for seed in seeds:
            print(f"\n{'='*60}")
            print(f"Testing Lesson 1.1 with seed={seed}")
            print(f"{'='*60}")
            
            model, optimizer = self.init_fresh_student(seed)
            print(f"Initialized fresh student with {model.get_num_params():,} params")
            
            # 1. Baseline performance
            print("\n1. Baseline performance...")
            baseline_loss = self.evaluate_loss(model, all_test)
            baseline_acc = self.evaluate_generation_accuracy(model, all_test)
            print(f"   Baseline loss (all test): {baseline_loss['avg_loss']:.4f}")
            print(f"   Baseline accuracy: {baseline_acc['accuracy']:.2%} ({baseline_acc['correct']}/{baseline_acc['total']})")
            
            # 2. Train on alphabet exemplars
            print(f"\n2. Training on {len(exemplars)} exemplars for {iterations} iterations...")
            training_losses = self.train_on_exemplars(model, optimizer, exemplars, iterations)
            print(f"   Training loss: {training_losses[0]:.4f} -> {training_losses[-1]:.4f}")
            
            # 3. Evaluate
            print("\n3. Post-training evaluation...")
            post_loss_all = self.evaluate_loss(model, all_test)
            post_acc_all = self.evaluate_generation_accuracy(model, all_test)
            
            post_loss_trainadj = self.evaluate_loss(model, training_adj)
            post_acc_trainadj = self.evaluate_generation_accuracy(model, training_adj)
            
            post_loss_heldout = self.evaluate_loss(model, held_out)
            post_acc_heldout = self.evaluate_generation_accuracy(model, held_out)
            
            print(f"   All test - Loss: {baseline_loss['avg_loss']:.4f} -> {post_loss_all['avg_loss']:.4f} (Δ={baseline_loss['avg_loss']-post_loss_all['avg_loss']:+.4f})")
            print(f"             Acc:  {baseline_acc['accuracy']:.2%} -> {post_acc_all['accuracy']:.2%}")
            print(f"   Training-adj - Loss: {post_loss_trainadj['avg_loss']:.4f}, Acc: {post_acc_trainadj['accuracy']:.2%}")
            print(f"   Held-out      - Loss: {post_loss_heldout['avg_loss']:.4f}, Acc: {post_acc_heldout['accuracy']:.2%}")
            
            # Show details
            print("\n   Detailed results:")
            for item in post_acc_all['items']:
                print(f"     '{item['prompt']}' -> target='{item['target']}', gen='{item['completion'][:10]}', correct={item['correct']}")
            
            # 4. Determine pass/fail
            loss_improved = (baseline_loss['avg_loss'] - post_loss_all['avg_loss']) > 0.1  # small threshold
            passed = loss_improved and post_loss_heldout['avg_loss'] < baseline_loss['avg_loss']  # any improvement on held-out
            
            print(f"\n4. Lesson 1.1 {'PASSED' if passed else 'FAILED'} (loss improved: {loss_improved}, held-out improved: {post_loss_heldout['avg_loss'] < baseline_loss['avg_loss']})")
            
            results_all.append({
                "seed": seed,
                "baseline_loss": baseline_loss['avg_loss'],
                "baseline_acc": baseline_acc['accuracy'],
                "post_loss_all": post_loss_all['avg_loss'],
                "post_acc_all": post_acc_all['accuracy'],
                "post_loss_trainadj": post_loss_trainadj['avg_loss'],
                "post_acc_trainadj": post_acc_trainadj['accuracy'],
                "post_loss_heldout": post_loss_heldout['avg_loss'],
                "post_acc_heldout": post_acc_heldout['accuracy'],
                "delta_loss_all": baseline_loss['avg_loss'] - post_loss_all['avg_loss'],
                "delta_loss_heldout": baseline_loss['avg_loss'] - post_loss_heldout['avg_loss'],  # baseline vs held-out
                "passed": passed,
                "training_losses": training_losses,
            })
        
        return results_all

    def test_lesson_1_2(self, seeds: List[int] = [42], iterations: int = 15) -> Dict[str, Any]:
        """Test Lesson 1.2: Counting Sequences without changing harness."""
        results_all = []
        
        exemplars = [
            "1 2 3 4 5 6",
            "3 4 5 6 7 8",
            "7 8 9 10 11 12",
            "10 11 12 13 14 15",
            "1 2 3 ",
            "4 5 6 ",
            "8 9 10 ",
        ]
        
        training_adj = [
            ("6 7 8 ", "9"),
            ("14 15 16 ", "17"),
        ]
        
        held_out = [
            ("2 3 4 ", "5"),
            ("9 10 11 ", "12"),
            ("15 16 17 ", "18"),
        ]
        
        all_test = training_adj + held_out
        
        for seed in seeds:
            print(f"\n{'='*60}")
            print(f"Testing Lesson 1.2 with seed={seed}")
            print(f"{'='*60}")
            
            model, optimizer = self.init_fresh_student(seed)
            print(f"Initialized fresh student with {model.get_num_params():,} params")
            
            print("\n1. Baseline performance...")
            baseline_loss = self.evaluate_loss(model, all_test)
            baseline_acc = self.evaluate_generation_accuracy(model, all_test)
            print(f"   Baseline loss: {baseline_loss['avg_loss']:.4f}, Acc: {baseline_acc['accuracy']:.2%}")
            
            print(f"\n2. Training on {len(exemplars)} exemplars for {iterations} iterations...")
            training_losses = self.train_on_exemplars(model, optimizer, exemplars, iterations)
            print(f"   Training loss: {training_losses[0]:.4f} -> {training_losses[-1]:.4f}")
            
            print("\n3. Post-training evaluation...")
            post_loss_all = self.evaluate_loss(model, all_test)
            post_acc_all = self.evaluate_generation_accuracy(model, all_test)
            post_loss_heldout = self.evaluate_loss(model, held_out)
            post_acc_heldout = self.evaluate_generation_accuracy(model, held_out)
            
            print(f"   All test - Loss: {baseline_loss['avg_loss']:.4f} -> {post_loss_all['avg_loss']:.4f} (Δ={baseline_loss['avg_loss']-post_loss_all['avg_loss']:+.4f})")
            print(f"   Held-out - Loss: {post_loss_heldout['avg_loss']:.4f}, Acc: {post_acc_heldout['accuracy']:.2%}")
            
            for item in post_acc_all['items']:
                print(f"     '{item['prompt']}' -> target='{item['target']}', gen='{item['completion'][:10]}', correct={item['correct']}")
            
            loss_improved = (baseline_loss['avg_loss'] - post_loss_all['avg_loss']) > 0.1
            passed = loss_improved and post_loss_heldout['avg_loss'] < baseline_loss['avg_loss']
            print(f"\n4. Lesson 1.2 {'PASSED' if passed else 'FAILED'}")
            
            results_all.append({
                "seed": seed,
                "baseline_loss": baseline_loss['avg_loss'],
                "post_loss_heldout": post_loss_heldout['avg_loss'],
                "delta_loss_heldout": baseline_loss['avg_loss'] - post_loss_heldout['avg_loss'],
                "post_acc_heldout": post_acc_heldout['accuracy'],
                "passed": passed,
            })
        return results_all


def main():
    tester = PreschoolTester(vault_root="vault")
    print("=== Preschool Throwaway Harness Test ===")
    print(f"Device: {tester.device}")
    
    # Test Lesson 1.1
    print("\n\n### TESTING LESSON 1.1 ###")
    results_11 = tester.test_lesson_1_1(seeds=[42, 123], iterations=15)
    
    # Summary for Lesson 1.1
    print(f"\n\n{'='*60}")
    print("LESSON 1.1 SUMMARY")
    print(f"{'='*60}")
    for r in results_11:
        print(f"Seed {r['seed']}: Held-out loss Δ={r['delta_loss_heldout']:+.4f}, Acc={r['post_acc_heldout']:.2%}, Passed={r['passed']}")
    
    # Test Lesson 1.2
    print("\n\n### TESTING LESSON 1.2 ###")
    results_12 = tester.test_lesson_1_2(seeds=[42], iterations=15)
    print(f"\n\n{'='*60}")
    print("LESSON 1.2 SUMMARY")
    print(f"{'='*60}")
    for r in results_12:
        print(f"Seed {r['seed']}: Held-out loss Δ={r['delta_loss_heldout']:+.4f}, Acc={r['post_acc_heldout']:.2%}, Passed={r['passed']}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = Path("experiments/preschool_test") / f"results_{timestamp}.json"
    all_results = {
        "lesson_1_1": results_11,
        "lesson_1_2": results_12,
        "timestamp": timestamp,
    }
    with open(results_file, 'w') as f:
        # Convert numpy/torch types if any
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n\nResults saved to {results_file}")


if __name__ == "__main__":
    main()
