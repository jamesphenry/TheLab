#!/usr/bin/env python3
"""Step 2: Use greedy decoding"""
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

prompt = "a b c "
target = "d"
print(f"\n=== Greedy decoding for '{prompt}' expecting '{target}' ===")

prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
model.eval()

# Greedy - manually pick highest prob
prompt_tensor = torch.tensor([prompt_tokens], dtype=torch.long)
generated_ids = []
current = prompt_tensor
for i in range(3):  # generate a few tokens
    with torch.no_grad():
        logits, _ = model(current, None)
        next_token = torch.argmax(logits[:, -1, :], dim=-1)
        generated_ids.append(next_token.item())
        current = torch.cat([current, next_token.unsqueeze(0)], dim=1)

full_text = tokenizer.decode(prompt_tokens + generated_ids)
print(f"Greedy generated: '{full_text}'")
if full_text.startswith(prompt):
    print(f"Completion: '{full_text[len(prompt):]}'")

# Compare with multinomial
generated_ids_multi = model.generate(prompt_tensor, max_new_tokens=3, temperature=0.8)
full_text_multi = tokenizer.decode(generated_ids_multi[0].tolist())
print(f"\nMultinomial generated: '{full_text_multi}'")
