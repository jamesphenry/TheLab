#!/usr/bin/env python3
"""Investigate with full lesson exemplars"""
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

# Full lesson exemplars
exemplars = [
    "a b c d e f g",
    "c d e f g h i",
    "m n o p q r s",
    "t u v w x y z",
    "e f g h i j k",
]

# Train
for iter in range(25):
    for text in exemplars:
        tokens = tokenizer.encode(text, add_special_tokens=False)
        if len(tokens) <= 1: continue
        input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
        target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
        loss = model.train_step(input_ids, target_ids, optimizer)

# Investigate
prompt = "r s t "
expected = "u"
prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
expected_tokens = tokenizer.encode(expected, add_special_tokens=False)
exp_token = expected_tokens[0]

model.eval()
with torch.no_grad():
    input_ids = torch.tensor([prompt_tokens], dtype=torch.long)
    logits, _ = model(input_ids, None)
    probs = torch.softmax(logits[0, -1, :], dim=-1)
    exp_prob = probs[exp_token].item()
    sorted_probs, sorted_idx = torch.sort(probs, descending=True)
    rank = (sorted_idx == exp_token).nonzero(as_tuple=True)[0].item() + 1

    print(f"Expected '{expected}' rank: {rank}, prob: {exp_prob:.6f}")
    print(f"Top 5: ", end="")
    for i in range(5):
        print(f"{repr(tokenizer.decode([sorted_idx[i].item()]))}({sorted_probs[i].item():.3f}) ", end="")
    print()
