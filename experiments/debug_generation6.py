#!/usr/bin/env python3
"""Try with the exact pattern from lesson"""
from __future__ import annotations

import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

torch.manual_seed(123)
config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
tokenizer = BabyTokenizer()
model = BabyLM(config)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

# Exact style from Lesson 1.1
exemplars = [
    "a b c d e f g ",
    "c d e f g h i ",
    "m n o p q r s ",
    "t u v w x y z ",
    "e f g h i j k ",
    "a b c  -> d",
    "f g h  -> i",
    "p q r  -> s", 
    "v w x  -> y",
]

print("Training with -> format...")
for iter in range(20):
    for text in exemplars:
        tokens = tokenizer.encode(text, add_special_tokens=False)
        if len(tokens) <= 1:
            continue
        input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
        target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
        loss = model.train_step(input_ids, target_ids, optimizer)
    if iter % 5 == 0:
        print(f"  Iter {iter}")

prompt = "g h i  -> "
target = "j"
prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
model.eval()
prompt_tensor = torch.tensor([prompt_tokens], dtype=torch.long)
generated_ids = model.generate(prompt_tensor, max_new_tokens=1, temperature=0.01)
generated_text = tokenizer.decode(generated_ids[0].tolist())
print(f"\nGenerated: '{generated_text}'")
if generated_text.startswith(prompt):
    completion = generated_text[len(prompt):]
    print(f"Completion: '{completion}'")
