#!/usr/bin/env python3
"""Investigate persistent r s t -> u failure"""
from __future__ import annotations

import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

torch.manual_seed(42)
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

# Train
for iter in range(25):
    for text in exemplars:
        tokens = tokenizer.encode(text, add_special_tokens=False)
        if len(tokens) <= 1: continue
        input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
        target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
        loss = model.train_step(input_ids, target_ids, optimizer)

# Investigate r s t
prompt = "r s t "
expected = "u"
print(f"=== Investigating '{prompt}' -> '{expected}' ===")
prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
expected_tokens = tokenizer.encode(expected, add_special_tokens=False)
exp_token = expected_tokens[0]

print(f"Prompt tokens: {prompt_tokens} -> {[repr(tokenizer.decode([t])) for t in prompt_tokens]}")
print(f"Expected token: {exp_token} -> {repr(tokenizer.decode([exp_token]))}")

model.eval()
with torch.no_grad():
    input_ids = torch.tensor([prompt_tokens], dtype=torch.long)
    logits, _ = model(input_ids, None)
    probs = torch.softmax(logits[0, -1, :], dim=-1)
    exp_prob = probs[exp_token].item()
    sorted_probs, sorted_idx = torch.sort(probs, descending=True)
    rank = (sorted_idx == exp_token).nonzero(as_tuple=True)[0].item() + 1

    print(f"\nExpected '{expected}' rank: {rank}, prob: {exp_prob:.6f}")
    print(f"\nTop 15 predictions:")
    for i in range(15):
        token_char = tokenizer.decode([sorted_idx[i].item()])
        marker = " <-- EXPECTED" if sorted_idx[i].item() == exp_token else ""
        print(f"  {i+1}. {repr(token_char)} (id={sorted_idx[i].item()}): {sorted_probs[i].item():.6f}{marker}")

# Check what training examples teach
print(f"\n=== Training coverage ===")
for ex in exemplars:
    if 'r' in ex or 's' in ex or 't' in ex or 'u' in ex:
        print(f"  '{ex}'")
