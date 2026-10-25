#!/usr/bin/env python3
"""Controlled, leakage-checked CVC transfer runner.

This script has an explicit ``--preflight-only`` mode. The normal mode trains
the three preregistered conditions; do not invoke it until the protocol, code,
data, and execution revision have been approved.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import io
import json
import math
import os
import platform
import random
import re
import signal
import statistics
import subprocess
import sys
import tempfile
import traceback
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "experiments" / "data" / "cvc_transfer_v2.json"
RESULTS_DIR = ROOT / "experiments" / "results" / "cvc_transfer_v2"
sys.path.insert(0, str(ROOT))

CONDITION_NAMES = ("phonics", "shuffled", "unrelated_english")
LETTER_BYTES = tuple(range(ord("a"), ord("z") + 1))
RUN_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}\Z")


class NonFiniteLossError(RuntimeError):
    """Raised when a training update returns a non-finite loss."""


class RunInterrupted(Exception):
    """Raised from SIGTERM so the partial bundle can be closed cleanly."""


class ByteTokenizerContract:
    """Tiny standard-library-only tokenizer contract for preflight checks."""

    special_tokens = ("<pad>", "<bos>", "<eos>", "<unk>")
    vocab_size = len(special_tokens) + 256

    @staticmethod
    def encode(text: str, add_special_tokens: bool = False) -> list[int]:
        ids = [len(ByteTokenizerContract.special_tokens) + byte for byte in text.encode("utf-8")]
        if add_special_tokens:
            return [1, *ids, 2]
        return ids


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_provenance() -> dict[str, Any]:
    def git(*args: str) -> str | None:
        try:
            return subprocess.run(
                ["git", *args], cwd=ROOT, check=True, capture_output=True,
                text=True,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return None

    status = git("status", "--porcelain", "--untracked-files=all")
    return {
        "commit": git("rev-parse", "HEAD"),
        "working_tree_clean": status == "" if status is not None else None,
        "working_tree_status_porcelain": status,
    }


def whole_words(text: str) -> set[str]:
    return set(re.findall(r"[a-z]+", text.lower()))


def overlapping_count(text: str, needle: str) -> int:
    text = text.lower()
    needle = needle.lower()
    return sum(text[index:index + len(needle)] == needle
               for index in range(max(0, len(text) - len(needle) + 1)))


def preflight(protocol: dict[str, Any], tokenizer: ByteTokenizerContract) -> dict[str, Any]:
    """Validate frozen inputs without importing Torch or constructing a model."""
    errors: list[str] = []
    conditions = protocol.get("conditions", {})
    development = protocol.get("development", [])
    final_test = protocol.get("final_test", [])

    if protocol.get("protocol_id") != "cvc_transfer_v2":
        errors.append("protocol_id must be cvc_transfer_v2")
    if protocol.get("protocol_version") != 2:
        errors.append("protocol_version must be 2")
    if protocol.get("passes") != 15:
        errors.append("training must use exactly 15 passes")
    seeds = protocol.get("seeds", [])
    if len(seeds) != 10 or len(set(seeds)) != 10:
        errors.append("expected ten unique, predeclared seeds")
    if tuple(conditions) != CONDITION_NAMES:
        errors.append(f"condition order/names must be {CONDITION_NAMES}")
    for name in CONDITION_NAMES:
        strings = conditions.get(name, [])
        if len(strings) != 5 or not all(isinstance(item, str) for item in strings):
            errors.append(f"{name} must contain exactly five strings")

    phonics = conditions.get("phonics", [])
    shuffled = conditions.get("shuffled", [])
    shuffle_checks = []
    if len(phonics) == len(shuffled):
        for index, (source, control) in enumerate(zip(phonics, shuffled)):
            same = (len(source.encode("utf-8")) == len(control.encode("utf-8"))
                    and Counter(source.encode("utf-8")) == Counter(control.encode("utf-8")))
            shuffle_checks.append({"example": index, "byte_multiset_and_length_match": same})
            if not same:
                errors.append(f"shuffled example {index} does not preserve byte inventory/length")

    actual_suffix_exposures: dict[str, dict[str, int]] = {}
    for item in development + final_test:
        suffix = str(item.get("word", ""))[-2:].lower()
        if len(suffix) == 2:
            actual_suffix_exposures.setdefault(suffix, {})
    for suffix in actual_suffix_exposures:
        for condition in CONDITION_NAMES:
            actual_suffix_exposures[suffix][condition] = sum(
                overlapping_count(sentence, suffix)
                for sentence in conditions.get(condition, [])
            )

    expected_suffixes = protocol.get("expected_suffix_exposures", {})
    expected_only = {
        suffix: {condition: int(counts.get(condition, -1)) for condition in CONDITION_NAMES}
        for suffix, counts in expected_suffixes.items()
    }
    final_suffixes = {str(item.get("word", ""))[-2:].lower() for item in final_test}
    actual_final_suffix_exposures = {
        suffix: actual_suffix_exposures[suffix]
        for suffix in final_suffixes
        if suffix in actual_suffix_exposures
    }
    if actual_final_suffix_exposures != expected_only:
        errors.append("computed suffix exposure matrix differs from the frozen expected matrix")

    phonics_words = set().union(*(whole_words(text) for text in phonics)) if phonics else set()
    target_letters = {str(item.get("target", "")) for item in development + final_test}
    phonics_letters = set("".join(phonics).lower())
    if not target_letters.issubset(phonics_letters):
        errors.append("one or more evaluation target letters are absent from phonics training")

    development_words = {str(item.get("word", "")) for item in development}
    test_words = {str(item.get("word", "")) for item in final_test}
    development_prompts = {str(item.get("prompt", "")) for item in development}
    test_prompts = {str(item.get("prompt", "")) for item in final_test}
    if development_words & test_words:
        errors.append("development and final-test words overlap")
    if development_prompts & test_prompts:
        errors.append("development and final-test prompts overlap")
    if len(development) != 4:
        errors.append("expected exactly four development items")
    if len(final_test) != 13:
        errors.append("expected exactly thirteen final-test items")

    evaluation_exposure: list[dict[str, Any]] = []
    for split_name, items in (("development", development), ("final_test", final_test)):
        for item in items:
            word = str(item.get("word", ""))
            prompt = str(item.get("prompt", ""))
            target = str(item.get("target", ""))
            item_errors: list[str] = []
            if len(word) != 3 or prompt != word[:2] or target != word[2:]:
                item_errors.append("item must be a CVC word split into a two-byte prompt and one-byte target")
            if not (word.isascii() and word.islower() and word.isalpha()):
                item_errors.append("word must contain lowercase ASCII letters only")
            if target not in "abcdefghijklmnopqrstuvwxyz":
                item_errors.append("target must be one lowercase ASCII letter")
            suffix = word[-2:].lower()
            actual_stratum = (
                "near" if actual_suffix_exposures.get(suffix, {}).get("phonics", 0) > 0 else "far"
            )
            declared_stratum = item.get("stratum", actual_stratum)
            if split_name == "final_test" and declared_stratum != actual_stratum:
                item_errors.append(f"declared stratum {declared_stratum} differs from computed {actual_stratum}")
            overlaps = {
                condition: sorted(whole_words(" ".join(strings)) & {word})
                for condition, strings in conditions.items()
            }
            if any(overlaps.values()):
                item_errors.append("complete evaluation word occurs in a training condition")
            encoded_prompt = tokenizer.encode(prompt, add_special_tokens=False)
            encoded_target = tokenizer.encode(target, add_special_tokens=False)
            byte_ids_valid = all(0 <= token_id < tokenizer.vocab_size
                                 for token_id in encoded_prompt + encoded_target)
            if not byte_ids_valid:
                item_errors.append("prompt/target encodes outside tokenizer byte vocabulary")
            if item_errors:
                errors.extend(f"{split_name} item {word}: {message}" for message in item_errors)
            byte_ngrams = [word[index:index + 2] for index in range(max(0, len(word) - 1))]
            evaluation_exposure.append({
                "split": split_name,
                "word": word,
                "prompt": prompt,
                "target": target,
                "stratum": actual_stratum if split_name == "final_test" else "development",
                "word_byte_bigrams": {
                    ngram: {
                        condition: sum(overlapping_count(sentence, ngram) for sentence in strings)
                        for condition, strings in conditions.items()
                    }
                    for ngram in byte_ngrams
                },
                "suffix_exposures": actual_suffix_exposures.get(suffix, {}),
                "whole_word_overlap_by_condition": overlaps,
                "byte_ids_valid": byte_ids_valid,
            })

    # Verify all frozen text is ASCII and can be represented by BabyTokenizer.
    training_byte_audit: dict[str, Any] = {}
    for condition, strings in conditions.items():
        ascii_only = all(text.isascii() for text in strings)
        valid_ids = all(
            token_id < tokenizer.vocab_size
            for text in strings
            for token_id in tokenizer.encode(text, add_special_tokens=True)
        )
        training_byte_audit[condition] = {
            "example_count": len(strings),
            "utf8_byte_count": sum(len(text.encode("utf-8")) for text in strings),
            "ascii_only": ascii_only,
            "tokenizer_ids_valid": valid_ids,
        }
        if not ascii_only or not valid_ids:
            errors.append(f"{condition} training strings contain invalid/non-ASCII byte IDs")

    # Verify the expected near/far split from treatment data, not only metadata.
    stratum_counts = Counter(str(item.get("stratum")) for item in final_test)
    if stratum_counts != Counter({"far": 8, "near": 5}):
        errors.append("final-test strata must contain five near and eight far items")

    return {
        "passed": not errors,
        "errors": errors,
        "checks": {
            "condition_examples": {name: len(conditions.get(name, [])) for name in CONDITION_NAMES},
            "shuffled_byte_inventory": shuffle_checks,
            "development_test_word_disjoint": not bool(development_words & test_words),
            "development_test_prompt_disjoint": not bool(development_prompts & test_prompts),
            "all_target_letters_in_phonics_training": target_letters.issubset(phonics_letters),
            "suffix_exposure_matches_frozen_matrix": actual_final_suffix_exposures == expected_only,
        },
        "suffix_exposure_counts_per_corpus_before_passes": actual_suffix_exposures,
        "final_test_suffix_exposure_counts_per_corpus_before_passes": actual_final_suffix_exposures,
        "training_byte_audit": training_byte_audit,
        "evaluation_item_exposure": evaluation_exposure,
        "pass_count": protocol.get("passes"),
        "updates_per_condition": protocol.get("passes", 0) * 5,
        "planned_trained_fits": len(seeds) * len(CONDITION_NAMES),
    }


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent,
        prefix=f".{path.name}.", suffix=".tmp", delete=False,
    ) as handle:
        temp_path = Path(handle.name)
        json.dump(value, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    os.replace(temp_path, path)


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return float("nan")
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def digest_state_dict(state: dict[str, Any]) -> str:
    import torch

    digest = hashlib.sha256()
    for name, tensor in sorted(state.items()):
        cpu_tensor = tensor.detach().to("cpu").contiguous()
        fields = (name, str(cpu_tensor.dtype), json.dumps(list(cpu_tensor.shape), separators=(",", ":")))
        for field in fields:
            digest.update(field.encode("utf-8"))
            digest.update(b"\0")
        # Torch writes raw storage bytes in C++; Python-level iteration over
        # UntypedStorage is prohibitively slow. Hash only data/0, excluding
        # archive metadata that can differ for equal tensors.
        tensor_buffer = io.BytesIO()
        torch.save(cpu_tensor, tensor_buffer)
        with zipfile.ZipFile(tensor_buffer) as archive:
            data_members = [name for name in archive.namelist() if name.endswith("/data/0")]
            if len(data_members) != 1:
                raise RuntimeError(f"expected one raw tensor payload in Torch archive for {name}")
            digest.update(archive.read(data_members[0]))
        digest.update(b"\0")
    return digest.hexdigest()


def snapshot_state_dict(state: dict[str, Any]) -> dict[str, Any]:
    return {name: tensor.detach().to("cpu").clone() for name, tensor in state.items()}


def states_equal(model_state: dict[str, Any], reference: dict[str, Any]) -> bool:
    import torch

    if model_state.keys() != reference.keys():
        return False
    return all(torch.equal(model_state[name].detach().to("cpu"), reference[name])
               for name in reference)


def set_seed(torch: Any, seed: int) -> None:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def readable_prediction(token_id: int, tokenizer: BabyTokenizer) -> tuple[str, str | None]:
    if token_id >= tokenizer.vocab_size:
        return f"<invalid-id:{token_id}>", None
    if token_id < len(tokenizer.special_tokens):
        return tokenizer.id_to_token.get(token_id, f"<special-id:{token_id}>"), None
    byte_value = token_id - len(tokenizer.special_tokens)
    decoded = bytes([byte_value]).decode("utf-8", errors="replace")
    return decoded, f"{byte_value:02x}"


def evaluate_items(
    model: Any,
    tokenizer: BabyTokenizer,
    items: list[dict[str, Any]],
    device: str,
) -> list[dict[str, Any]]:
    import torch

    model.eval()
    letter_ids = [len(tokenizer.special_tokens) + value for value in LETTER_BYTES]
    results = []
    for item in items:
        prompt_ids = tokenizer.encode(item["prompt"], add_special_tokens=False)
        target_id = tokenizer.encode(item["target"], add_special_tokens=False)[0]
        input_ids = torch.tensor([prompt_ids], dtype=torch.long, device=device)
        with torch.no_grad():
            logits, _ = model(input_ids, None)
        vector = logits[0, -1, :].float()
        log_probabilities = torch.log_softmax(vector, dim=0)
        letter_logits = vector[letter_ids]
        letter_log_probabilities = torch.log_softmax(letter_logits, dim=0)

        full_prediction = int(torch.argmax(vector).item())
        letter_offset = int(torch.argmax(letter_logits).item())
        letter_prediction = letter_ids[letter_offset]
        full_text, full_byte_hex = readable_prediction(full_prediction, tokenizer)
        letter_text, letter_byte_hex = readable_prediction(letter_prediction, tokenizer)
        impossible_mass = float(torch.softmax(vector, dim=0)[tokenizer.vocab_size:].sum().item())
        item_result = {
            "word": item["word"],
            "prompt": item["prompt"],
            "target": item["target"],
            "stratum": item.get("stratum", "development"),
            "target_token_id": target_id,
            "target_byte_hex": f"{ord(item['target']):02x}",
            "full_head_target_nll": float((-log_probabilities[target_id]).item()),
            "lowercase_letter_normalized_target_nll": float((-letter_log_probabilities[ord(item["target"]) - ord("a")]).item()),
            "target_probability_full_head": float(torch.exp(log_probabilities[target_id]).item()),
            "target_probability_lowercase_letters": float(torch.exp(letter_log_probabilities[ord(item["target"]) - ord("a")]).item()),
            "target_rank_full_head": int((vector > vector[target_id]).sum().item()) + 1,
            "target_rank_lowercase_letters": int((letter_logits > vector[target_id]).sum().item()) + 1,
            "impossible_output_id_probability_mass": impossible_mass,
            "full_head_argmax_id": full_prediction,
            "full_head_argmax_token": full_text,
            "full_head_argmax_byte_hex": full_byte_hex,
            "full_head_argmax_is_impossible_id": full_prediction >= tokenizer.vocab_size,
            "full_head_exact_letter": full_prediction == target_id,
            "letter_restricted_argmax_id": letter_prediction,
            "letter_restricted_argmax_token": letter_text,
            "letter_restricted_argmax_byte_hex": letter_byte_hex,
            "letter_restricted_exact_letter": letter_prediction == target_id,
        }
        results.append(item_result)
    return results


def mean_metric(items: list[dict[str, Any]], key: str) -> float:
    return statistics.mean(float(item[key]) for item in items) if items else float("nan")


def distribution_summary(values: list[float]) -> dict[str, Any]:
    return {
        "n_seeds": len(values),
        "seed_level_values": values,
        "mean": statistics.mean(values) if values else None,
        "median": statistics.median(values) if values else None,
        "sample_standard_deviation": statistics.stdev(values) if len(values) > 1 else 0.0,
    }


def condition_seed_summary(
    baseline_items: list[dict[str, Any]],
    final_items: list[dict[str, Any]],
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for stratum in ("near", "far"):
        base = [item for item in baseline_items if item["stratum"] == stratum]
        final = [item for item in final_items if item["stratum"] == stratum]
        output[stratum] = {
            "item_count": len(final),
            "baseline_mean_full_head_nll": mean_metric(base, "full_head_target_nll"),
            "final_mean_full_head_nll": mean_metric(final, "full_head_target_nll"),
            "full_head_nll_improvement": mean_metric(base, "full_head_target_nll") - mean_metric(final, "full_head_target_nll"),
            "baseline_mean_letter_normalized_nll": mean_metric(base, "lowercase_letter_normalized_target_nll"),
            "final_mean_letter_normalized_nll": mean_metric(final, "lowercase_letter_normalized_target_nll"),
            "letter_normalized_nll_improvement": mean_metric(base, "lowercase_letter_normalized_target_nll") - mean_metric(final, "lowercase_letter_normalized_target_nll"),
            "full_head_exact_accuracy": statistics.mean(bool(item["full_head_exact_letter"]) for item in final) if final else 0.0,
            "letter_restricted_exact_accuracy": statistics.mean(bool(item["letter_restricted_exact_letter"]) for item in final) if final else 0.0,
            "impossible_argmax_rate": statistics.mean(bool(item["full_head_argmax_is_impossible_id"]) for item in final) if final else 0.0,
        }
    return output


def summarize_run(protocol: dict[str, Any], seed_records: list[dict[str, Any]]) -> dict[str, Any]:
    per_seed: dict[str, dict[str, Any]] = {}
    paired_far_contrasts: list[float] = []
    for seed_record in seed_records:
        seed = str(seed_record["seed"])
        baseline = seed_record["baseline"]["final_test"]
        per_seed[seed] = {}
        for condition_name, condition in seed_record["conditions"].items():
            per_seed[seed][condition_name] = condition_seed_summary(
                baseline, condition["final"]["final_test"]
            )
        phonics_gain = per_seed[seed]["phonics"]["far"]["full_head_nll_improvement"]
        shuffled_gain = per_seed[seed]["shuffled"]["far"]["full_head_nll_improvement"]
        paired_far_contrasts.append(phonics_gain - shuffled_gain)

    aggregate_by_condition: dict[str, Any] = {}
    aggregate_metrics = (
        "full_head_nll_improvement",
        "letter_normalized_nll_improvement",
        "full_head_exact_accuracy",
        "letter_restricted_exact_accuracy",
        "impossible_argmax_rate",
    )
    for condition_name in CONDITION_NAMES:
        aggregate_by_condition[condition_name] = {}
        for stratum in ("near", "far"):
            aggregate_by_condition[condition_name][stratum] = {
                metric: distribution_summary([
                    float(per_seed[str(seed_record["seed"])][condition_name][stratum][metric])
                    for seed_record in seed_records
                ])
                for metric in aggregate_metrics
            }

    boot = protocol["bootstrap"]
    rng = random.Random(int(boot["seed"]))
    estimates = []
    for _ in range(int(boot["resamples"])):
        sample = [rng.choice(paired_far_contrasts) for _ in paired_far_contrasts]
        estimates.append(statistics.mean(sample))
    alpha = 1.0 - float(boot["confidence_level"])
    return {
        "per_seed_by_condition_and_stratum": per_seed,
        "aggregate_by_condition_and_stratum": aggregate_by_condition,
        "primary_far_paired_improvement_contrast_phonics_minus_shuffled": {
            "n_seeds": len(paired_far_contrasts),
            "n_fixed_far_items": 8,
            "seed_level_values": paired_far_contrasts,
            "mean": statistics.mean(paired_far_contrasts),
            "median": statistics.median(paired_far_contrasts),
            "sample_standard_deviation": statistics.stdev(paired_far_contrasts) if len(paired_far_contrasts) > 1 else 0.0,
            "bootstrap_method": "percentile interval over paired seeds",
            "bootstrap_resamples": int(boot["resamples"]),
            "bootstrap_seed": int(boot["seed"]),
            "confidence_level": float(boot["confidence_level"]),
            "bootstrap_interval": [percentile(estimates, alpha / 2), percentile(estimates, 1 - alpha / 2)],
            "interpretation_unit": "seed-level initialization sensitivity; the eight words remain eight fixed items",
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True, help="Unique label; output files are never overwritten")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--preflight-only", action="store_true", help="Write the data audit without importing Torch or training")
    return parser.parse_args()


def signal_handler(signum: int, _frame: Any) -> None:
    raise RunInterrupted(f"received signal {signum}")


def main() -> int:
    args = parse_args()
    if not RUN_ID_PATTERN.fullmatch(args.run_id):
        print("ERROR: --run-id must be 1-80 filename-safe ASCII letters, digits, dots, underscores, or hyphens", file=sys.stderr)
        return 2

    try:
        protocol_bytes = DATA_PATH.read_bytes()
        protocol = json.loads(protocol_bytes)
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: cannot load frozen protocol data: {error}", file=sys.stderr)
        return 2

    tokenizer = ByteTokenizerContract()
    audit = preflight(protocol, tokenizer)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    bundle_path = RESULTS_DIR / f"{args.run_id}.json"
    log_path = RESULTS_DIR / f"{args.run_id}.log"
    if bundle_path.exists() or log_path.exists():
        print(f"ERROR: run ID already has output; refusing to overwrite {args.run_id}", file=sys.stderr)
        return 2

    try:
        log_handle = log_path.open("x", encoding="utf-8")
    except FileExistsError:
        print(f"ERROR: log already exists; refusing to overwrite {log_path}", file=sys.stderr)
        return 2

    run_bundle: dict[str, Any] = {
        "bundle_schema_version": 1,
        "protocol_id": protocol["protocol_id"],
        "protocol_version": protocol["protocol_version"],
        "run_id": args.run_id,
        "status": "running",
        "started_at_utc": utc_now(),
        "finished_at_utc": None,
        "command": ["python3", "experiments/run_cvc_transfer_v2.py", *sys.argv[1:]],
        "source_path": "experiments/run_cvc_transfer_v2.py",
        "data_path": "experiments/data/cvc_transfer_v2.json",
        "output_paths": {
            "bundle": f"experiments/results/cvc_transfer_v2/{args.run_id}.json",
            "log": f"experiments/results/cvc_transfer_v2/{args.run_id}.log",
        },
        "source_sha256": sha256_file(Path(__file__).resolve()),
        "protocol_data_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
        "git_provenance_before_output_creation": git_provenance(),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "pytorch_package_version": importlib.metadata.version("torch") if importlib.metadata.packages_distributions().get("torch") else None,
            "requested_device": args.device,
        },
        "protocol_configuration": protocol,
        "preflight": audit,
        "progress": None,
        "seed_runs": [],
        "summary": None,
    }

    def log(message: str) -> None:
        line = f"[{utc_now()}] {message}"
        print(line, flush=True)
        log_handle.write(line + "\n")
        log_handle.flush()

    def save_bundle() -> None:
        atomic_write_json(bundle_path, run_bundle)

    try:
        save_bundle()  # Persist the leakage/exposure audit before any model/optimizer exists.
        log(f"run_id={args.run_id}; preflight={'PASS' if audit['passed'] else 'FAIL'}")
        log(f"bundle={run_bundle['output_paths']['bundle']}")
        if not audit["passed"]:
            run_bundle["status"] = "preflight_failed"
            run_bundle["finished_at_utc"] = utc_now()
            log("preflight failed; no model or optimizer was constructed")
            save_bundle()
            return 2
        if args.preflight_only:
            run_bundle["status"] = "preflight_only"
            run_bundle["finished_at_utc"] = utc_now()
            log("preflight-only mode; no Torch import, model construction, or training")
            save_bundle()
            return 0

        signal.signal(signal.SIGTERM, signal_handler)
        run_training(protocol, run_bundle, log, save_bundle, args.device)
        run_bundle["summary"] = summarize_run(protocol, run_bundle["seed_runs"])
        run_bundle["status"] = "completed"
        run_bundle["finished_at_utc"] = utc_now()
        run_bundle["progress"] = None
        log("run completed all declared seeds and conditions")
        save_bundle()
        return 0
    except (KeyboardInterrupt, RunInterrupted) as error:
        run_bundle["status"] = "interrupted"
        run_bundle["finished_at_utc"] = utc_now()
        run_bundle["interruption"] = str(error) or "KeyboardInterrupt"
        log(f"run interrupted; preserving partial bundle: {run_bundle['interruption']}")
        save_bundle()
        return 130
    except Exception as error:
        run_bundle["status"] = "failed"
        run_bundle["finished_at_utc"] = utc_now()
        run_bundle["failure"] = {
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
        }
        log(f"run failed; preserving partial bundle: {type(error).__name__}: {error}")
        log(traceback.format_exc())
        save_bundle()
        return 1
    finally:
        log_handle.close()


def run_training(
    protocol: dict[str, Any],
    bundle: dict[str, Any],
    log: Any,
    save_bundle: Any,
    requested_device: str,
) -> None:
    import torch

    from harness.learner.config import BabyLMConfig
    from harness.learner.model import BabyLM
    from harness.learner.tokenizer import BabyTokenizer

    if requested_device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was explicitly requested but is unavailable")
    device = ("cuda" if torch.cuda.is_available() else "cpu") if requested_device == "auto" else requested_device
    model_config = protocol["model"]
    config = BabyLMConfig(**model_config, device=device)
    tokenizer = BabyTokenizer()
    torch_version = torch.__version__
    device_name = torch.cuda.get_device_name(0) if device == "cuda" else platform.processor() or "CPU"
    bundle["environment"].update({
        "pytorch_version": str(torch_version),
        "device": device,
        "device_name": device_name,
        "cuda_version": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
    })
    bundle["optimizer_configuration"] = protocol["optimizer"]
    bundle["training_schedule"] = {
        "passes_per_condition": protocol["passes"],
        "examples_per_condition": 5,
        "updates_per_condition": protocol["passes"] * 5,
        "planned_total_optimizer_updates": len(protocol["seeds"]) * len(CONDITION_NAMES) * protocol["passes"] * 5,
        "checkpoint_selection": "none; final weights after fixed schedule",
        "training_texts_by_condition": protocol["conditions"],
        "raw_training_utf8_bytes_by_condition": {
            name: sum(len(text.encode("utf-8")) for text in texts)
            for name, texts in protocol["conditions"].items()
        },
        "training_target_tokens_per_pass_by_condition": {
            name: sum(len(tokenizer.encode(text, add_special_tokens=True)) - 1 for text in texts)
            for name, texts in protocol["conditions"].items()
        },
    }
    save_bundle()

    all_updates = 0
    for seed in protocol["seeds"]:
        seed = int(seed)
        set_seed(torch, seed)
        reference_model = BabyLM(config).to(device)
        initial_state = snapshot_state_dict(reference_model.state_dict())
        initial_digest = digest_state_dict(initial_state)
        baseline_development = evaluate_items(reference_model, tokenizer, protocol["development"], device)
        baseline_final = evaluate_items(reference_model, tokenizer, protocol["final_test"], device)
        seed_record: dict[str, Any] = {
            "seed": seed,
            "initial_state_sha256": initial_digest,
            "baseline": {
                "development": baseline_development,
                "final_test": baseline_final,
            },
            "conditions": {},
        }
        bundle["seed_runs"].append(seed_record)
        del reference_model
        log(f"seed={seed} paired_initial_state_sha256={initial_digest}")
        save_bundle()

        for condition_name in CONDITION_NAMES:
            set_seed(torch, seed)
            model = BabyLM(config).to(device)
            model.load_state_dict(initial_state, strict=True)
            state_equal = states_equal(model.state_dict(), initial_state)
            arm_digest = digest_state_dict(model.state_dict())
            if not state_equal or arm_digest != initial_digest:
                raise RuntimeError(f"initial-state mismatch for seed={seed}, condition={condition_name}")

            optimizer_cfg = protocol["optimizer"]
            optimizer = torch.optim.AdamW(
                model.parameters(),
                lr=float(optimizer_cfg["learning_rate"]),
                betas=tuple(float(value) for value in optimizer_cfg["betas"]),
                eps=float(optimizer_cfg["eps"]),
                weight_decay=float(optimizer_cfg["weight_decay"]),
                amsgrad=bool(optimizer_cfg["amsgrad"]),
            )
            condition_record: dict[str, Any] = {
                "initial_state_sha256": arm_digest,
                "tensor_equal_to_paired_reference": state_equal,
                "passes_completed": 0,
                "updates_completed": 0,
                "training_loss_by_pass": [],
                "final": None,
            }
            seed_record["conditions"][condition_name] = condition_record
            log(f"seed={seed} condition={condition_name} verified_identical_initial_weights=true")

            for pass_index in range(1, int(protocol["passes"]) + 1):
                pass_losses: list[float] = []
                for example_index, text in enumerate(protocol["conditions"][condition_name], start=1):
                    token_ids = tokenizer.encode(text, add_special_tokens=True)
                    input_ids = torch.tensor([token_ids[:-1]], dtype=torch.long, device=device)
                    target_ids = torch.tensor([token_ids[1:]], dtype=torch.long, device=device)
                    loss_value = model.train_step(
                        input_ids,
                        target_ids,
                        optimizer,
                        clip_grad=float(optimizer_cfg["gradient_clip_norm"]),
                    )
                    if not math.isfinite(loss_value):
                        raise NonFiniteLossError(
                            f"non-finite loss at seed={seed}, condition={condition_name}, "
                            f"pass={pass_index}, example={example_index}"
                        )
                    pass_losses.append(loss_value)
                    all_updates += 1
                    condition_record["updates_completed"] += 1
                    bundle["progress"] = {
                        "seed": seed,
                        "condition": condition_name,
                        "pass": pass_index,
                        "last_completed_update_in_condition": condition_record["updates_completed"],
                        "last_completed_global_update": all_updates,
                    }
                mean_loss = statistics.mean(pass_losses)
                condition_record["passes_completed"] = pass_index
                condition_record["training_loss_by_pass"].append(mean_loss)
                log(f"seed={seed} condition={condition_name} pass={pass_index}/{protocol['passes']} mean_loss={mean_loss:.6f}")
                save_bundle()

            condition_record["final"] = {
                "development": evaluate_items(model, tokenizer, protocol["development"], device),
                "final_test": evaluate_items(model, tokenizer, protocol["final_test"], device),
            }
            if condition_record["updates_completed"] != int(protocol["passes"]) * 5:
                raise RuntimeError(f"unexpected update count for seed={seed}, condition={condition_name}")
            log(f"seed={seed} condition={condition_name} final_evaluation_saved")
            save_bundle()
            del optimizer, model
            if device == "cuda":
                torch.cuda.empty_cache()

    expected_runs = len(protocol["seeds"]) * len(CONDITION_NAMES)
    if sum(len(seed_record["conditions"]) for seed_record in bundle["seed_runs"]) != expected_runs:
        raise RuntimeError("run ended without all planned seed-condition arms")
    bundle["training_schedule"]["completed_optimizer_updates"] = all_updates


if __name__ == "__main__":
    raise SystemExit(main())
