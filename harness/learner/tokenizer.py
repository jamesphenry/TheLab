from typing import List, Dict


class BabyTokenizer:
    """Byte-level tokenizer for early-stage language acquisition.
    
    Guarantees 100% vocabulary coverage without out-of-vocabulary (OOV) tokens,
    treating ASCII/UTF-8 bytes directly with reserved control tokens.
    """

    PAD_TOKEN = "<pad>"
    BOS_TOKEN = "<bos>"
    EOS_TOKEN = "<eos>"
    UNK_TOKEN = "<unk>"

    def __init__(self, max_vocab: int = 4096) -> None:
        self.special_tokens = [self.PAD_TOKEN, self.BOS_TOKEN, self.EOS_TOKEN, self.UNK_TOKEN]
        self.pad_id = 0
        self.bos_id = 1
        self.eos_id = 2
        self.unk_id = 3

        # Map special tokens first
        self.token_to_id: Dict[str, int] = {tok: idx for idx, tok in enumerate(self.special_tokens)}
        self.id_to_token: Dict[int, str] = {idx: tok for idx, tok in enumerate(self.special_tokens)}

        # Map all 256 byte values directly to token IDs
        offset = len(self.special_tokens)
        for b in range(256):
            tok_id = offset + b
            char_repr = bytes([b]).decode("latin1")
            self.token_to_id[char_repr] = tok_id
            self.id_to_token[tok_id] = char_repr

        self.vocab_size = offset + 256

    def encode(self, text: str, add_special_tokens: bool = False) -> List[int]:
        """Convert string to a list of token IDs."""
        byte_data = text.encode("utf-8")
        tokens: List[int] = []
        if add_special_tokens:
            tokens.append(self.bos_id)

        offset = len(self.special_tokens)
        for b in byte_data:
            tokens.append(offset + b)

        if add_special_tokens:
            tokens.append(self.eos_id)

        return tokens

    def decode(self, token_ids: List[int], skip_special_tokens: bool = True) -> str:
        """Convert token IDs back to a decoded string."""
        raw_bytes = bytearray()
        offset = len(self.special_tokens)

        for tid in token_ids:
            if tid < offset:
                if not skip_special_tokens:
                    tok = self.id_to_token.get(tid, "")
                    raw_bytes.extend(tok.encode("utf-8"))
                continue
            b = tid - offset
            if 0 <= b < 256:
                raw_bytes.append(b)

        return raw_bytes.decode("utf-8", errors="replace")
