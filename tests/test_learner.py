import unittest
import torch

from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer


class TestBabyTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = BabyTokenizer()

    def test_encode_decode_roundtrip(self):
        sample = "The quick brown fox jumps over the lazy dog! 123."
        tokens = self.tokenizer.encode(sample)
        reconstructed = self.tokenizer.decode(tokens)
        self.assertEqual(sample, reconstructed)

    def test_special_tokens(self):
        sample = "Cat"
        tokens = self.tokenizer.encode(sample, add_special_tokens=True)
        self.assertEqual(tokens[0], self.tokenizer.bos_id)
        self.assertEqual(tokens[-1], self.tokenizer.eos_id)


class TestBabyLMModel(unittest.TestCase):
    def setUp(self):
        # Full 25M config
        self.config = BabyLMConfig(
            vocab_size=4096,
            max_seq_len=128,
            dim=512,
            n_layers=8,
            n_heads=8,
            device="cpu"
        )
        self.model = BabyLM(self.config)

    def test_parameter_count(self):
        num_params = self.model.get_num_params()
        # Should be between 24M and 30M parameters
        self.assertGreater(num_params, 24_000_000)
        self.assertLess(num_params, 30_000_000)

    def test_forward_and_loss(self):
        b, t = 2, 16
        idx = torch.randint(0, self.config.vocab_size, (b, t))
        targets = torch.randint(0, self.config.vocab_size, (b, t))

        logits, loss = self.model(idx, targets)
        self.assertEqual(logits.shape, (b, t, self.config.vocab_size))
        self.assertIsNotNone(loss)
        self.assertGreater(float(loss.item()), 0.0)

    def test_train_step_overfitting(self):
        """Verify the model can execute backpropagation and reduce loss on a toy batch."""
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-3)
        b, t = 1, 8
        idx = torch.randint(0, self.config.vocab_size, (b, t))
        targets = idx.clone()

        initial_loss = self.model.train_step(idx, targets, optimizer)
        for _ in range(5):
            latest_loss = self.model.train_step(idx, targets, optimizer)

        self.assertLess(latest_loss, initial_loss)

    def test_generate(self):
        prompt = torch.tensor([[10, 20, 30]], dtype=torch.long)
        out = self.model.generate(prompt, max_new_tokens=5, temperature=1.0)
        self.assertEqual(out.shape, (1, 8))


if __name__ == "__main__":
    unittest.main()
