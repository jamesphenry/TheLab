from __future__ import annotations

import math
from typing import Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from harness.learner.config import BabyLMConfig


class LayerNorm(nn.Module):
    """LayerNorm with optional bias, matching modern transformer implementations."""

    def __init__(self, dim: int, eps: float = 1e-5) -> None:
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))
        self.bias = nn.Parameter(torch.zeros(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.layer_norm(x, self.weight.shape, self.weight, self.bias, self.eps)


class CausalSelfAttention(nn.Module):
    def __init__(self, config: BabyLMConfig) -> None:
        super().__init__()
        assert config.dim % config.n_heads == 0, "dim must be divisible by n_heads"
        self.n_heads = config.n_heads
        self.d_k = config.dim // config.n_heads

        self.c_attn = nn.Linear(config.dim, 3 * config.dim, bias=False)
        self.c_proj = nn.Linear(config.dim, config.dim, bias=False)
        self.dropout = config.dropout

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.size()

        # Calculate query, key, values for all heads in batch and move head forward to the batch dim
        q, k, v = self.c_attn(x).split(C, dim=2)
        k = k.view(B, T, self.n_heads, self.d_k).transpose(1, 2)  # (B, nh, T, hs)
        q = q.view(B, T, self.n_heads, self.d_k).transpose(1, 2)  # (B, nh, T, hs)
        v = v.view(B, T, self.n_heads, self.d_k).transpose(1, 2)  # (B, nh, T, hs)

        # Efficient scaled dot product attention with causal masking
        y = F.scaled_dot_product_attention(
            q, k, v,
            attn_mask=None,
            dropout_p=self.dropout if self.training else 0.0,
            is_causal=True
        )
        y = y.transpose(1, 2).contiguous().view(B, T, C)  # Re-assemble head outputs side by side
        return self.c_proj(y)


class MLP(nn.Module):
    def __init__(self, config: BabyLMConfig) -> None:
        super().__init__()
        self.c_fc = nn.Linear(config.dim, config.d_ff, bias=False)
        self.gelu = nn.GELU()
        self.c_proj = nn.Linear(config.d_ff, config.dim, bias=False)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.c_fc(x)
        x = self.gelu(x)
        x = self.c_proj(x)
        x = self.dropout(x)
        return x


class TransformerBlock(nn.Module):
    def __init__(self, config: BabyLMConfig) -> None:
        super().__init__()
        self.ln_1 = LayerNorm(config.dim)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = LayerNorm(config.dim)
        self.mlp = MLP(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class BabyLM(nn.Module):
    """A compact ~25M parameter causal Transformer initialized from scratch (tabula rasa)."""

    def __init__(self, config: BabyLMConfig) -> None:
        super().__init__()
        self.config = config

        self.wte = nn.Embedding(config.vocab_size, config.dim)
        self.wpe = nn.Embedding(config.max_seq_len, config.dim)
        self.drop = nn.Dropout(config.dropout)
        self.blocks = nn.ModuleList([TransformerBlock(config) for _ in range(config.n_layers)])
        self.ln_f = LayerNorm(config.dim)
        self.lm_head = nn.Linear(config.dim, config.vocab_size, bias=False)

        # Weight tying
        self.lm_head.weight = self.wte.weight

        # Initialize weights with small normal distribution
        self.apply(self._init_weights)

    def _init_weights(self, module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def get_num_params(self, non_embedding: bool = False) -> int:
        """Return the number of parameters in the model."""
        n_params = sum(p.numel() for p in self.parameters())
        if non_embedding:
            n_params -= self.wpe.weight.numel()
        return n_params

    def forward(
        self,
        idx: torch.Tensor,
        targets: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        device = idx.device
        b, t = idx.size()
        assert t <= self.config.max_seq_len, f"Sequence length {t} exceeds maximum {self.config.max_seq_len}"

        pos = torch.arange(0, t, dtype=torch.long, device=device)

        # Forward the model
        tok_emb = self.wte(idx)
        pos_emb = self.wpe(pos)
        x = self.drop(tok_emb + pos_emb)

        for block in self.blocks:
            x = block(x)

        x = self.ln_f(x)

        if targets is not None:
            logits = self.lm_head(x)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=-1)
        else:
            # Inference optimization: only project the last position
            logits = self.lm_head(x[:, [-1], :])
            loss = None

        return logits, loss

    @torch.no_grad()
    def generate(
        self,
        idx: torch.Tensor,
        max_new_tokens: int,
        temperature: float = 1.0,
        top_k: Optional[int] = None
    ) -> torch.Tensor:
        """Autoregressively generate tokens given a prompt."""
        self.eval()
        for _ in range(max_new_tokens):
            idx_cond = idx if idx.size(1) <= self.config.max_seq_len else idx[:, -self.config.max_seq_len:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / max(temperature, 1e-5)

            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = -float("Inf")

            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, next_token), dim=1)

        return idx

    def train_step(
        self,
        idx: torch.Tensor,
        targets: torch.Tensor,
        optimizer: torch.optim.Optimizer,
        clip_grad: float = 1.0
    ) -> float:
        """Execute a single interactive training step and return the loss."""
        self.train()
        optimizer.zero_grad(set_to_none=True)
        _, loss = self(idx, targets)
        assert loss is not None, "Loss cannot be None during train_step"
        loss.backward()
        if clip_grad > 0.0:
            torch.nn.utils.clip_grad_norm_(self.parameters(), clip_grad)
        optimizer.step()
        return float(loss.item())
