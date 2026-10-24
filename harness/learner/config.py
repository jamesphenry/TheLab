from dataclasses import dataclass


@dataclass
class BabyLMConfig:
    vocab_size: int = 4096
    max_seq_len: int = 512
    dim: int = 512
    n_layers: int = 8
    n_heads: int = 8
    mlp_ratio: int = 4
    dropout: float = 0.0
    device: str = "cpu"

    @property
    def d_k(self) -> int:
        return self.dim // self.n_heads

    @property
    def d_ff(self) -> int:
        return self.dim * self.mlp_ratio
