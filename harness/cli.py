import argparse
from pathlib import Path
import torch

from harness.vault.controller import VaultController
from harness.learner.config import BabyLMConfig
from harness.learner.model import BabyLM
from harness.learner.tokenizer import BabyTokenizer
from harness.school.classroom import ClassroomSession


def run_lesson_1(iterations: int = 10, compact: bool = False) -> None:
    vault_root = Path("vault")
    vault = VaultController(vault_root)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Initializing AI School Classroom on device: {device}")

    # Use compact config if requested, else full 25M config
    if compact:
        config = BabyLMConfig(vocab_size=4096, max_seq_len=128, dim=128, n_layers=4, n_heads=4, device=device)
    else:
        config = BabyLMConfig(vocab_size=4096, max_seq_len=256, dim=512, n_layers=8, n_heads=8, device=device)

    tokenizer = BabyTokenizer()
    model = BabyLM(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    print(f"Model initialized: {model.get_num_params():,} parameters (tabula rasa)")

    classroom = ClassroomSession(
        vault=vault,
        model=model,
        tokenizer=tokenizer,
        optimizer=optimizer,
        device=device
    )

    exemplars = [
        "The cat sat on the mat.",
        "The dog can run in the sun.",
        "The sun is hot.",
        "The red pen is on the bed.",
        "A cat can run."
    ]

    test_items = [
        ("The cat sat on the ", "mat."),
        ("The sun is ", "hot."),
        ("The dog can ", "run."),
        ("The red pen is on the ", "bed.")
    ]

    print("\n--- Running Pre-Lesson Assessment ---")
    results = classroom.run_learning_cycle(
        subject="Language",
        lesson_rel_path="02-School/Language/Lessons/Lesson-1.1-Alphabet-and-Phonics.md",
        assessment_rel_path="02-School/Language/Assessments/Assessment-1.1.md",
        exemplars=exemplars,
        test_items=test_items,
        iterations=iterations
    )

    print("\n=== Lesson 1.1 Complete ===")
    print(f"Pre-Lesson Evaluation Loss:  {results['pre_eval']['avg_loss']:.4f}")
    print(f"Post-Lesson Evaluation Loss: {results['post_eval']['avg_loss']:.4f}")
    print(f"Net Improvement (Delta):     {results['delta_loss']:+.4f}")
    print(f"Session Transcript Logged:   {results['session_file']}")
    print(f"Assessment Report Logged:    {results['report_file']}")
    print("Self-Assessment Updated:     vault/01-Learner/Self-Assessment.md")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Learner Laboratory CLI")
    parser.add_argument("--run-lesson-1", action="store_true", help="Execute Lesson 1.1 learning cycle")
    parser.add_argument("--iterations", type=int, default=10, help="Number of training iterations")
    parser.add_argument("--compact", action="store_true", help="Use compact model for rapid testing")
    args = parser.parse_args()

    if args.run_lesson_1:
        run_lesson_1(iterations=args.iterations, compact=args.compact)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
