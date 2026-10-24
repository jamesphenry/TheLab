---
title: "2026-10-23 BabyLM 25M Baseline Initialization & Gradient Step"
type: experiment
status: completed
tags:
  - ai-school
  - experiment
  - babylm
  - baseline
created: 2026-10-23
updated: 2026-10-23
---

# 2026-10-23 BabyLM 25M Baseline Initialization & Gradient Step

## Question
Can a ~25M parameter causal Transformer initialized with random weights ($\mathcal{N}(0, 0.02)$) successfully execute end-to-end forward passes, compute causal cross-entropy loss, backpropagate gradients, and demonstrate deterministic loss reduction on an interactive training sequence within CPU/P4 memory boundaries?

## Hypothesis
1. The ~25M model architecture ($n_{layers}=8, d_{model}=512, n_{heads}=8, \text{vocab}=4096$) will allocate approximately $27\text{M}$ total parameters.
2. The model will initialize in a state of maximum entropy (uniform token probability), producing initial cross-entropy loss $\approx \ln(\text{vocab\_size}) = \ln(4096) \approx 8.31$.
3. Interactive backward passes via AdamW will measurably decrease cross-entropy loss over 5 gradient steps on a sample sequence without NaN gradients or divergence.

## Variables and Conditions
- **Independent Variable:** Number of AdamW gradient steps ($t \in [0, 5]$) on a fixed sequence.
- **Measured Outcomes:**
  - Parameter count ($N_{params}$).
  - Initial forward cross-entropy loss ($\mathcal{L}_0$).
  - Post-step cross-entropy loss ($\mathcal{L}_5$).
  - Autoregressive generation shape integrity.
- **Controls:** Fixed random seed, learning rate $\eta = 10^{-3}$, weight tying between embedding and LM head.
- **Environment / Architecture:** Debian Linux x86_64, Python 3.13.5, PyTorch 2.14.1+cpu (CPU development mode).
- **Code Reference:** `harness.learner.model.BabyLM`, `harness.learner.tokenizer.BabyTokenizer`.

## Procedure
1. Initialize `BabyLMConfig` with $V=4096, d=512, L=8, H=8, T=128$.
2. Instantiate `BabyLM` and record total parameter count.
3. Generate synthetic token sequence and evaluate initial forward loss $\mathcal{L}_0$.
4. Apply 5 iterations of `model.train_step()` using AdamW optimizer ($\text{lr}=10^{-3}$).
5. Verify $\mathcal{L}_5 < \mathcal{L}_0$.
6. Sample 5 autoregressive tokens via `model.generate()`.

## Results

| Run | Conditions | Observation | Evidence |
| :--- | :--- | :--- | :--- |
| **Param Count** | $L=8, d=512, V=4096$ | $27,330,560$ parameters total | `test_parameter_count: PASSED` |
| **Initial Loss** | Random weights | $\mathcal{L}_0 \approx 8.32$ (matches theoretical $\ln(4096) = 8.317$) | `test_forward_and_loss: PASSED` |
| **Gradient Step** | 5 steps AdamW | Loss drops consistently ($\mathcal{L}_5 < \mathcal{L}_0$) | `test_train_step_overfitting: PASSED` |
| **Generation** | Autoregressive sampling | Output tensor shaped `(1, prompt_len + 5)` | `test_generate: PASSED` |
| **Tokenizer** | Byte-level UTF-8 roundtrip | Exact string reconstruction | `test_encode_decode_roundtrip: PASSED` |

## Interpretation
The results verify that the 25M BabyLM architecture is mathematically sound and structurally ready for live interactive learning:
- The parameter count ($27.3\text{M}$) sits precisely in the targeted 25M range.
- The initial baseline loss closely tracks theoretical uniform entropy, proving clean weight initialization without exploding or dead layers.
- The training step executes cleanly on CPU, confirming that live backpropagation during teacher interaction works as designed.

## Limitations
- This baseline experiment tests structural and computational viability on synthetic tokens; it does not evaluate convergence speed on real phonics or natural language corpora.

## Conclusion
- **Supported:** The 25M BabyLM model initializes cleanly, backpropagates gradients, and reduces loss deterministically.
- **Next Experiment:** Stage 0 Phonics curriculum — testing rate of loss decay and word-boundary acquisition on letter and phoneme lessons.

## Related
- Model Architecture: [[Development/Architecture|Harness Architecture]]
- Decision Record: [[Development/Decisions/ADR-0001 BabyLM 25M Tabula Rasa Architecture|ADR-0001]]
- Tests: `tests/test_learner.py`
