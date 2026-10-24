import tempfile
import unittest
from pathlib import Path
import torch

from harness.vault.controller import VaultController
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer
from harness.school.classroom import ClassroomSession


class TestClassroomSession(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)

        # Create basic directory structure
        (self.vault_path / "00-System").mkdir(parents=True)
        (self.vault_path / "01-Learner").mkdir(parents=True)
        (self.vault_path / "02-School" / "Language" / "Lessons").mkdir(parents=True)
        (self.vault_path / "02-School" / "Language" / "Assessments").mkdir(parents=True)
        (self.vault_path / "03-Experiences").mkdir(parents=True)
        (self.vault_path / "07-Reports").mkdir(parents=True)

        self.vault = VaultController(self.vault_path)

        # Fast test configuration (2 layers, 128 dim)
        self.config = BabyLMConfig(
            vocab_size=4096,
            max_seq_len=64,
            dim=128,
            n_layers=2,
            n_heads=4,
            device="cpu"
        )
        self.model = BabyLM(self.config)
        self.tokenizer = BabyTokenizer()
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=5e-3)

        self.classroom = ClassroomSession(
            vault=self.vault,
            model=self.model,
            tokenizer=self.tokenizer,
            optimizer=self.optimizer,
            device="cpu"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_run_learning_cycle_end_to_end(self):
        exemplars = [
            "The cat sat on the mat.",
            "The dog can run in the sun."
        ]
        test_items = [
            ("The cat sat on the ", "mat."),
            ("The dog can ", "run")
        ]

        results = self.classroom.run_learning_cycle(
            subject="Language",
            lesson_rel_path="02-School/Language/Lessons/Lesson-1.1.md",
            assessment_rel_path="02-School/Language/Assessments/Assessment-1.1.md",
            exemplars=exemplars,
            test_items=test_items,
            iterations=10
        )

        # Check loss improvement
        self.assertGreater(results["delta_loss"], 0.0)

        # Check session log file creation
        session_file = self.vault_path / results["session_file"]
        self.assertTrue(session_file.exists())
        self.assertTrue(session_file.read_text(encoding="utf-8").startswith("---\n"))

        # Check report file creation
        report_file = self.vault_path / results["report_file"]
        self.assertTrue(report_file.exists())
        self.assertTrue(report_file.read_text(encoding="utf-8").startswith("---\n"))

        # Check self-assessment file update
        self_assess = self.vault_path / "01-Learner" / "Self-Assessment.md"
        self.assertTrue(self_assess.exists())
        self.assertIn("Language", self_assess.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
