#!/usr/bin/env python3
"""Debug generation issue - trace one example end to end"""
from __future__ import annotations

import torch
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer

# Setup
torch.manual_seed(123)
config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8)
tokenizer = BabyTokenizer()
model = BabyLM(config)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

# Train on Lesson 1.1 exemplars
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
        tokens = tokenizer.encode(text, add_special_tokens=True)
        if len(tokens) <= 1:
            continue
        input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
        target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
        loss = model.train_step(input_ids, target_ids, optimizer)
    if iter % 5 == 0:
        print(f"  Iter {iter}")

# Test on held-out
prompt = "g h i "
target = "j"
print(f"\n=== Testing prompt='{prompt}' target='{target}' ===")

# Check tokens
prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
target_tokens = tokenizer.encode(target, add_special_tokens=False)
print(f"Prompt tokens: {prompt_tokens}")
print(f"Prompt bytes: {[tokenizer.decode([t]) for t in prompt_tokens]}")
print(f"Target tokens: {target_tokens}")
print(f"Target bytes: {[tokenizer.decode([t]) for t in target_tokens]}")

# Generation
model.eval()
prompt_tensor = torch.tensor([prompt_tokens], dtype=torch.long)
generated_ids = model.generate(prompt_tensor, max_new_tokens=5, temperature=0.8)
generated_text = tokenizer.decode(generated_ids[0].tolist())
print(f"\nGenerated (full): '{generated_text}'")
if generated_text.startswith(prompt):
    completion = generated_text[len(prompt):]
    print(f"Completion: '{completion}'")

# Also try greedy
generated_ids_greedy = model.generate(prompt_tensor, max_new_tokens=5, temperature=0.1)
generated_text_greedy = tokenizer.decode(generated_ids_greedy[0].tolist())
print(f"\nGenerated (greedy, temp=0.1): '{generated_text_greedy}'")
if generated_text_greedy.startswith(prompt):
    completion_g = generated_text_greedy[len(prompt):]
    print(f"Completion (greedy): '{completion_g}'")

# Check probabilities
with torch.no_grad():
    input_ids = prompt_tensor
    logits, _ = model(input_ids, None)
    # Get probs for next token
    probs = torch.softmax(logits[0, -1, :], dim=-1)
    topk = torch.topk(probs, k=10)
    print(f"\nTop 10 next token probabilities:")
    for i, (prob, idx) in enumerate(zip(topk.values, topk.indices)):
        token_char = tokenizer.decode([idx.item()])
        print(f"  {i+1}. '{token_char}' (id={idx.item()}): {prob.item():.4f}")
