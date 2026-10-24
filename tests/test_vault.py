import tempfile
import unittest
from pathlib import Path

from harness.vault.controller import VaultController, Role, PermissionDeniedError, VaultAccessError


class TestVaultController(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name)
        
        # Create standard layout
        (self.vault_path / "00-System").mkdir(parents=True)
        (self.vault_path / "01-Learner").mkdir(parents=True)
        (self.vault_path / "02-School" / "Programming" / "Lessons").mkdir(parents=True)
        (self.vault_path / "02-School" / "Programming" / "Assessments").mkdir(parents=True)
        (self.vault_path / "03-Experiences").mkdir(parents=True)
        (self.vault_path / "07-Reports").mkdir(parents=True)

        # Seed files
        (self.vault_path / "00-System" / "Harness-Rules.md").write_text("rules", encoding="utf-8")
        (self.vault_path / "01-Learner" / "Goals.md").write_text("goals", encoding="utf-8")
        (self.vault_path / "02-School" / "Programming" / "Lessons" / "Lesson-1.md").write_text("lesson 1", encoding="utf-8")
        (self.vault_path / "02-School" / "Programming" / "Assessments" / "Exam-1.md").write_text("exam secret", encoding="utf-8")
        (self.vault_path / "07-Reports" / "Grade-1.md").write_text("grade A", encoding="utf-8")

        self.vault = VaultController(self.vault_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_path_traversal_blocked(self):
        with self.assertRaises(PermissionDeniedError):
            self.vault.read_file("../../etc/passwd", role=Role.HUMAN)

        with self.assertRaises(PermissionDeniedError):
            self.vault.read_file("01-Learner/../../00-System/Harness-Rules.md", role=Role.LEARNER)

    def test_learner_permissions(self):
        # Learner can read own goals
        content = self.vault.read_file("01-Learner/Goals.md", role=Role.LEARNER)
        self.assertEqual(content, "goals")

        # Learner can read lesson
        lesson = self.vault.read_file("02-School/Programming/Lessons/Lesson-1.md", role=Role.LEARNER)
        self.assertEqual(lesson, "lesson 1")

        # Learner cannot read unassigned exam answers/assessments
        with self.assertRaises(PermissionDeniedError):
            self.vault.read_file("02-School/Programming/Assessments/Exam-1.md", role=Role.LEARNER)

        # Learner cannot read 00-System
        with self.assertRaises(PermissionDeniedError):
            self.vault.read_file("00-System/Harness-Rules.md", role=Role.LEARNER)

        # Learner can write to 01-Learner
        self.vault.write_file("01-Learner/MyNotes.md", "student note", role=Role.LEARNER)
        self.assertEqual((self.vault_path / "01-Learner" / "MyNotes.md").read_text(), "student note")

        # Learner CANNOT write to 02-School or 07-Reports or 00-System
        with self.assertRaises(PermissionDeniedError):
            self.vault.write_file("02-School/Programming/Lessons/Cheat.md", "hack", role=Role.LEARNER)

        with self.assertRaises(PermissionDeniedError):
            self.vault.write_file("07-Reports/FakeGrade.md", "A+", role=Role.LEARNER)

        with self.assertRaises(PermissionDeniedError):
            self.vault.write_file("00-System/Harness-Rules.md", "override", role=Role.LEARNER)

    def test_teacher_permissions(self):
        # Programming teacher can write lessons in Programming
        self.vault.write_file("02-School/Programming/Lessons/Lesson-2.md", "lesson 2", role=Role.TEACHER, subject="Programming")
        self.assertEqual((self.vault_path / "02-School" / "Programming" / "Lessons" / "Lesson-2.md").read_text(), "lesson 2")

        # Programming teacher cannot write to Mathematics
        with self.assertRaises(PermissionDeniedError):
            self.vault.write_file("02-School/Mathematics/Lessons/Lesson-1.md", "math", role=Role.TEACHER, subject="Programming")

        # Teacher cannot write to 00-System
        with self.assertRaises(PermissionDeniedError):
            self.vault.write_file("00-System/Harness-Rules.md", "new rules", role=Role.TEACHER, subject="Programming")

    def test_assessment_permissions(self):
        # Assessment can write grade report
        self.vault.write_file("07-Reports/Report-1.md", "Graded rubric", role=Role.ASSESSMENT)
        self.assertEqual((self.vault_path / "07-Reports" / "Report-1.md").read_text(), "Graded rubric")

        # Assessment cannot write to school curriculum
        with self.assertRaises(PermissionDeniedError):
            self.vault.write_file("02-School/Programming/Lessons/L1.md", "tamper", role=Role.ASSESSMENT)

    def test_human_unrestricted(self):
        # Human can read and write anywhere in the vault
        self.vault.write_file("00-System/Harness-Rules.md", "updated by human", role=Role.HUMAN)
        content = self.vault.read_file("00-System/Harness-Rules.md", role=Role.HUMAN)
        self.assertEqual(content, "updated by human")


if __name__ == "__main__":
    unittest.main()
