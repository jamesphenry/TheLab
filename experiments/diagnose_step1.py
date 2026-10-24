#!/usr/bin/env python3
"""Step 1: Inspect next-token probabilities"""
from __future__ import annotations

import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

# Test with seed 123 like before
torch.manual_seed(123)
config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
tokenizer = BabyTokenizer()
model = BabyLM(config)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

# Use the format from our test
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
]

print("Training...")
for iter in range(15):
    for text in exemplars:
        tokens = tokenizer.encode(text, add_special_tokens=False)
        if len(tokens) <= 1:
            continue
        input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
        target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
        loss = model.train_step(input_ids, target_ids, optimizer)

prompt = "a b c "  # prefix
expected = "d"

print(f"\n=== Diagnostic for prefix '{prompt}' expecting '{expected}' ===")
prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
print(f"Tokenized prompt: {prompt_tokens}")
print(f"Decoded tokens: {[repr(tokenizer.decode([t])) for t in prompt_tokens]}")

expected_tokens = tokenizer.encode(expected, add_special_tokens=False)
print(f"Expected '{expected}' tokenized: {expected_tokens} -> {[repr(tokenizer.decode([t])) for t in expected_tokens]}")

model.eval()
with torch.no_grad():
    input_ids = torch.tensor([prompt_tokens], dtype=torch.long)
    logits, _ = model(input_ids, None)
    probs = torch.softmax(logits[0, -1, :], dim=-1)
    
    # Check expected token probability
    if expected_tokens:
        exp_token = expected_tokens[0]
        exp_prob = probs[exp_token].item()
        print(f"\nExpected token '{expected}' (id={exp_token}): probability = {exp_prob:.6f}")
    
    # Top 10
    topk = torch.topk(probs, k=10)
    print(f"\nTop 10 predictions:")
    for i, (prob, idx) in enumerate(zip(topk.values, topk.indices)):
        token_char = tokenizer.decode([idx.item()])
        marker = " <-- EXPECTED" if expected_tokens and idx.item() == expected_tokens[0] else ""
        print(f"  {i+1}. {repr(token_char)} (id={idx.item()}): {prob.item():.6f}{marker}")
