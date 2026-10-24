#!/usr/bin/env python3
"""Track expected token rank and probability over training"""
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

# Try different formats
formats = {
    "full_sequences": [
        "a b c d e f g",
        "b c d e f g h",
        "c d e f g h i",
        "d e f g h i j",
        "e f g h i j k",
    ],
    "prefix_only": [
        "a b c ",
        "b c d ",
        "c d e ",
        "f g h ",
        "m n o ",
    ],
    "mixed": [
        "a b c d e f g",
        "c d e f g h i",
        "a b c ",
        "f g h ",
    ]
}

for fmt_name, exemplars in formats.items():
    print(f"\n{'='*60}")
    print(f"Format: {fmt_name}")
    print(f"{'='*60}")
    
    # Fresh model
    torch.manual_seed(123)
    model = BabyLM(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    
    prompt = "a b c "
    expected = "d"
    prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
    expected_tokens = tokenizer.encode(expected, add_special_tokens=False)
    exp_token = expected_tokens[0] if expected_tokens else None
    
    for iter in range(0, 21, 5):
        if iter > 0:
            for _ in range(5):
                for text in exemplars:
                    tokens = tokenizer.encode(text, add_special_tokens=False)
                    if len(tokens) <= 1: continue
                    input_ids = torch.tensor([tokens[:-1]], dtype=torch.long)
                    target_ids = torch.tensor([tokens[1:]], dtype=torch.long)
                    loss = model.train_step(input_ids, target_ids, optimizer)
        
        # Check
        model.eval()
        with torch.no_grad():
            input_ids = torch.tensor([prompt_tokens], dtype=torch.long)
            logits, _ = model(input_ids, None)
            probs = torch.softmax(logits[0, -1, :], dim=-1)
            exp_prob = probs[exp_token].item() if exp_token else 0
            
            # Get rank
            sorted_probs, sorted_idx = torch.sort(probs, descending=True)
            rank = (sorted_idx == exp_token).nonzero(as_tuple=True)[0].item() + 1
            
        print(f"Iter {iter:2d}: exp_prob={exp_prob:.6f}, rank={rank}, top_token={repr(tokenizer.decode([sorted_idx[0].item()]))}")
