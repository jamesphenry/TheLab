---
title: "Experiment D — Inspect Tokenization"
type: experiment
status: completed
scripts:
  - experiments/run_experiment_d.py
tags:
  - ai-school
  - experiment
  - tokenization
  - tokenizer
  - verification
created: 2026-10-23
updated: 2026-10-25
---

# Experiment D — Inspect Tokenization

## Question

How does the `BabyTokenizer` actually represent individual letters, spaces, punctuation, and CVC words at the token level? The model config declares `vocab_size=4096` and the tokenizer class is described as "byte-level," but the actual vocabulary is only 260 tokens (4 special + 256 byte values). Does the model operate on true single-byte tokens, or is there a mismatch between the configured `vocab_size` and the tokenizer's actual vocabulary?

## Hypothesis

1. The `BabyTokenizer` operates at the byte level: each UTF-8 byte maps to exactly one token ID, and each character in the ASCII range (letters, digits, punctuation, space) is a single token. Round-trip encoding/decoding is lossless.
2. The tokenizer's actual vocabulary size is 260 (4 special tokens + 256 byte tokens), which is far smaller than the model's configured `vocab_size=4096`. The embedding table has 4,096 rows but only 260 are ever used — the remaining 3,836 embeddings are dead parameters.
3. CVC words like `cat` are encoded as exactly 3 tokens (one per byte), not as a single subword token. There is no BPE or merge operations.
4. The `latin1` decoding used in `__init__` correctly maps all 256 byte values to characters for the `token_to_id` dictionary, but the `encode` method operates on raw UTF-8 bytes, meaning multi-byte UTF-8 characters (e.g. accented letters, emoji) will produce multiple tokens.

## Variables and Conditions

- **Inspection targets:**
  - Individual lowercase letters: `a`, `b`, `c`, ..., `z`
  - Individual uppercase letters: `A`, `B`, `C`, ..., `Z`
  - Space character: `" "` (single space)
  - Punctuation: `.`, `,`, `!`, `?`, `'`, `"`
  - CVC words: `cat`, `bat`, `rat`, `mat`, `pen`, `dog`, `run`, `sun`, `hot`, `bed`
  - Multi-word exemplars: `"The cat sat on the mat."`, `"The sun is hot."`
  - Multi-byte UTF-8: `é`, `ñ`, `—` (em dash), `🎉`
  - Numbers: `0`, `1`, `42`
- **Measured outcomes:**
  - Token ID sequence for each input.
  - Token count vs. character count (to verify byte-level operation).
  - Decode round-trip fidelity.
  - Actual vocabulary size of `BabyTokenizer` instance.
  - Distribution of token IDs in the training exemplars (which IDs are used, which are not).
  - Number of dead embedding rows (vocab_size - actual_used_tokens).
- **Code reference:** `harness.learner.tokenizer.BabyTokenizer`, `harness.learner.config.BabyLMConfig`.

## Procedure

1. Instantiate `BabyTokenizer()` and record `tokenizer.vocab_size`.
2. For each inspection target:
   a. Encode the string via `tokenizer.encode(text, add_special_tokens=False)`.
   b. Record the token ID list.
   c. Verify `len(tokens) == len(text.encode("utf-8"))` (byte-level confirmation).
   d. Decode back via `tokenizer.decode(tokens)` and verify exact string recovery.
3. For the 5 training exemplars:
   a. Encode each.
   b. Record the full token ID sequence.
   c. Collect the set of unique token IDs used across all exemplars.
4. Compute:
   - Actual vocabulary size: `tokenizer.vocab_size` (expected: 260).
   - Configured model vocab: `BabyLMConfig.vocab_size` (expected: 4096).
   - Dead embedding rows: `4096 - 260 = 3836`.
   - Unique tokens used in training: count of distinct IDs in exemplar encodings.
5. For multi-byte UTF-8 characters:
   a. Encode `é` (2 bytes in UTF-8), `ñ` (2 bytes), `—` (3 bytes), `🎉` (4 bytes).
   b. Verify token count matches byte count, not character count.
6. Inspect the token ID mapping:
   a. Print `tokenizer.token_to_id` for a representative sample: `a`, `A`, ` `, `.`, `c`, `t`.
   b. Verify the offset: special tokens occupy IDs 0-3, byte values start at ID 4.
   c. Verify a space (byte 32) maps to ID `4 + 32 = 36`.

### Code Changes Required

- **No code changes needed** — this is a pure inspection/analysis experiment. The existing `BabyTokenizer` API (`encode`, `decode`, `token_to_id`, `id_to_token`, `vocab_size`) provides everything required.
- **Suggested approach:** Write a standalone inspection script (e.g. `experiments/run_experiment_d.py`) that:
  1. Instantiates the tokenizer.
  2. Runs the encoding/decoding checks described above.
  3. Prints a formatted report of all findings.
  4. Optionally writes results to a vault note in `07-Reports/`.
- **Consider adding a test:** Add a unit test to `tests/test_learner.py` that asserts `tokenizer.vocab_size == 260` and that the model's embedding table has `4096` rows, documenting the intentional mismatch.

## Results

### Tokenizer Vocabulary

| Property | Value |
| --- | --- |
| Special tokens | 4 (`<pad>`, `<bos>`, `<eos>`, `<unk>`) |
| Byte tokens | 256 |
| Actual vocab size | **260** |
| Model config vocab_size | **4096** |
| Dead embedding rows | **3836** (1,964,032 params, **1.96M**) |

### Single Character Encoding

| Input | UTF-8 Bytes | Token Count | Token IDs | Round-Trip OK |
| --- | :---: | :---: | :--- | :---: |
| `a` | 1 | 1 | [101] | OK |
| `A` | 1 | 1 | [69] | OK |
| `z` | 1 | 1 | [126] | OK |
| ` ` (space) | 1 | 1 | [36] | OK |
| `.` | 1 | 1 | [50] | OK |
| `c` | 1 | 1 | [103] | OK |
| `t` | 1 | 1 | [120] | OK |

All 19 tested characters (letters, digits, punctuation, space): **1 byte = 1 token, all round-trips lossless.**

### CVC Word Encoding

| Word | Characters | UTF-8 Bytes | Token Count | Token IDs | Round-Trip OK |
| --- | :---: | :---: | :---: | :--- | :---: |
| `cat` | 3 | 3 | **3** | [103, 101, 120] | OK |
| `mat` | 3 | 3 | **3** | [113, 101, 120] | OK |
| `run` | 3 | 3 | **3** | [118, 121, 114] | OK |
| `hot` | 3 | 3 | **3** | [108, 115, 120] | OK |
| `bed` | 3 | 3 | **3** | [102, 105, 104] | OK |

All 12 tested CVC words: **3 tokens each (one per byte), all round-trips lossless.**

### Multi-Byte UTF-8 Encoding

| Input | Characters | UTF-8 Bytes | Token Count | Round-Trip OK |
| --- | :---: | :---: | :---: | :---: |
| `é` | 1 | 2 | **2** | OK |
| `ñ` | 1 | 2 | **2** | OK |
| `—` | 1 | 3 | **3** | OK |
| `🎉` | 1 | 4 | **4** | OK |

Token count always equals byte count, not character count. Multi-byte UTF-8 characters produce multiple tokens.

### Training Exemplar Token Usage

| Exemplar | Token Count | Unique Tokens |
| --- | :---: | :---: |
| `"The cat sat on the mat."` | 23 | 12 |
| `"The dog can run in the sun."` | 27 | 16 |
| `"The sun is hot."` | 15 | 11 |
| `"The red pen is on the bed."` | 26 | 14 |
| `"A cat can run."` | 14 | 9 |
| **Total unique tokens across all exemplars** | | **20** |

The 5 training exemplars use only **20 out of 260** available tokenizer tokens (7.7% utilization). The 20 tokens correspond to: space, period, uppercase `A` and `T`, and lowercase letters `a`, `b`, `c`, `d`, `e`, `g`, `h`, `i`, `m`, `n`, `o`, `p`, `r`, `s`, `t`, `u`.

### Token ID Formula

```
token_id = 4 + byte_value (for byte tokens)
Special tokens: pad=0, bos=1, eos=2, unk=3
```

Verified for all tested characters: `a` (byte 97 → ID 101), `A` (byte 65 → ID 69), space (byte 32 → ID 36), etc.

## Interpretation

### 1. The tokenizer is truly byte-level

Confirmed across all test categories: every token corresponds to exactly one byte. ASCII characters (letters, digits, punctuation, space) each map to a single token. CVC words are 3 tokens. Multi-byte UTF-8 characters produce multiple tokens (one per byte, not one per character). Round-trip encode/decode is lossless in all cases. There is no BPE, no subword merging, no character-level abstraction — pure byte-level operation.

### 2. The vocab_size mismatch wastes ~2M parameters

The tokenizer has 260 tokens (4 special + 256 bytes), but `BabyLMConfig.vocab_size` is set to 4096. This means the embedding table has 4,096 rows but only 260 are ever used — 3,836 rows are dead. At `dim=512`, that's **1,964,032 wasted parameters (~1.96M)**, which is **7.1% of the model's 27.5M total parameters**.

This is not a bug per se — the dead rows never receive gradients (they're never indexed), so they don't affect training. But they inflate the model's reported parameter count and waste memory. Reducing `vocab_size` to 260 would shrink the model to ~25.5M parameters with no loss in capability. Alternatively, the extra capacity could be used for a future BPE tokenizer with merge operations.

### 3. Training exemplars use only 20 of 260 tokens

The 5 phonics exemplars use just 20 distinct byte tokens: space, period, uppercase `A`/`T`, and 16 lowercase letters (`a`, `b`, `c`, `d`, `e`, `g`, `h`, `i`, `m`, `n`, `o`, `p`, `r`, `s`, `t`, `u`). The remaining 240 tokens in the tokenizer (including all digits, most punctuation, and all non-ASCII bytes) are unused. This is expected for a phonics lesson — the curriculum simply doesn't need more character coverage at this stage.

### 4. The token ID mapping is clean and predictable

The formula `token_id = 4 + byte_value` holds for all tested characters. The offset of 4 accounts for the 4 special tokens. This makes the tokenizer fully transparent — given any byte value, the token ID is deterministic, and vice versa.

### Key Questions Addressed

1. **Is the tokenizer truly byte-level?** Yes — every token is one byte, confirmed across ASCII, CVC words, and multi-byte UTF-8.
2. **What is the vocab_size mismatch impact?** 3,836 dead embedding rows = 1.96M wasted parameters (7.1% of total). No training impact, but inflates reported model size.
3. **Should `BabyLMConfig.vocab_size` be reduced to 260?** Recommended. This would eliminate dead embeddings with no capability loss. Alternatively, document the larger vocab as intentional for future BPE expansion.
4. **Are there any encoding surprises?** No — `latin1` decoding in the tokenizer's `__init__` correctly maps all 256 byte values, and the `encode` method operates on raw UTF-8 bytes as expected.

## Limitations

- This experiment inspects the tokenizer in isolation. It does not test how the model actually uses the tokens (e.g. attention patterns over byte sequences).
- The token usage analysis covers only the 5 training exemplars — a broader corpus would reveal more about vocabulary utilization.
- Does not investigate whether a BPE or character-level tokenizer would be more efficient for this task.

## Conclusion

- **Supported:**
  1. The `BabyTokenizer` operates at the byte level — every token is one byte, confirmed across ASCII characters, CVC words, and multi-byte UTF-8. (Hypothesis 1 confirmed.)
  2. The tokenizer's actual vocabulary is 260 (4 special + 256 bytes), and the model config's `vocab_size=4096` leaves 3,836 dead embedding rows (~1.96M wasted parameters, 7.1% of total). (Hypothesis 2 confirmed.)
  3. CVC words are encoded as exactly 3 tokens (one per byte) with no BPE or merge operations. (Hypothesis 3 confirmed.)
  4. Multi-byte UTF-8 characters produce multiple tokens equal to their byte count, and `latin1` decoding in `__init__` correctly maps all 256 byte values. (Hypothesis 4 confirmed.)
- **Not established:**
  1. Whether reducing `vocab_size` to 260 would improve training speed (fewer parameters to load, but dead rows don't receive gradients anyway).
  2. Whether a BPE tokenizer would be more efficient for this task — the byte-level approach works but requires the model to learn byte-to-character mappings from scratch.
- **Next experiment:** If vocab_size mismatch is confirmed, consider an ADR for reducing `BabyLMConfig.vocab_size` to 260 or implementing a proper BPE tokenizer.

## Related

- Code: `harness/learner/tokenizer.py`, `harness/learner/config.py`
- Tests: `tests/test_learner.py` (`TestBabyTokenizer`)
- Related experiments: [[2026-10-23 Experiment A — Held-Out Test|Experiment A]], [[2026-10-23 Experiment B — Control Group|Experiment B]], [[2026-10-23 Experiment C — Multiple Random Seeds|Experiment C]]
- Architecture: [[Development/Architecture|Harness Architecture]]
