#!/usr/bin/env python3
"""Manage deterministic state for drill-syntax-bioinformatics."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
STATE_DIRNAME = ".drill-syntax-bioinformatics"
DEFAULT_TRACK = "python"
TRACKS = {
    "python": {
        "bank_path": SKILL_DIR / "references" / "python_question_bank.json",
        "state_filename": "python_progress.json",
        "mistakes_filename": "python_mistakes.jsonl",
        "question_count": 180,
    },
    "statistics": {
        "bank_path": SKILL_DIR / "references" / "statistics_question_bank.json",
        "state_filename": "statistics_progress.json",
        "mistakes_filename": "statistics_mistakes.jsonl",
        "question_count": 180,
    },
    "r": {
        "bank_path": SKILL_DIR / "references" / "r_question_bank.json",
        "state_filename": "r_progress.json",
        "mistakes_filename": "r_mistakes.jsonl",
        "question_count": 180,
    },
}
REVIEW_GAP = 10
STATE_SCHEMA_VERSION = 2


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    temporary.replace(path)


def append_json_line(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, ensure_ascii=False))
        handle.write("\n")


def load_json_lines(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            entry = json.loads(line)
            if not isinstance(entry, dict):
                raise ValueError(
                    f"Mistakes log line {line_number} must contain a JSON object."
                )
            entries.append(entry)
    return entries


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def find_repo_root(start: Path) -> Path:
    resolved = start.resolve()
    for candidate in (resolved, *resolved.parents):
        if (candidate / ".agents" / "skills" / "drill-syntax-bioinformatics").is_dir():
            return candidate
    raise SystemExit(
        "Could not locate the repository containing "
        ".agents/skills/drill-syntax-bioinformatics."
    )


def track_config(track: str) -> dict[str, Any]:
    try:
        return TRACKS[track]
    except KeyError as error:
        raise ValueError(f"Unknown drill track: {track!r}.") from error


def bank_data(track: str) -> dict[str, Any]:
    bank = load_json(track_config(track)["bank_path"])
    validate_bank(bank, track)
    return bank


def state_path(repo_root: Path, track: str) -> Path:
    return repo_root / STATE_DIRNAME / track_config(track)["state_filename"]


def mistakes_path(repo_root: Path, track: str) -> Path:
    return repo_root / STATE_DIRNAME / track_config(track)["mistakes_filename"]


def category_map(bank: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {category["id"]: category for category in bank["categories"]}


def questions_by_id(bank: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {question["id"]: question for question in bank["questions"]}


def validate_bank(bank: dict[str, Any], track: str) -> None:
    required_top = {"schema_version", "language", "categories", "questions"}
    if not required_top.issubset(bank):
        raise ValueError(f"Question bank is missing: {sorted(required_top - set(bank))}")
    if bank["language"] != track:
        raise ValueError(
            f"The {track!r} question bank must have language={track!r}."
        )

    categories = bank["categories"]
    questions = bank["questions"]
    category_ids = [category["id"] for category in categories]
    if len(category_ids) != len(set(category_ids)):
        raise ValueError("Category IDs must be unique.")
    expected_question_count = track_config(track)["question_count"]
    if len(questions) != expected_question_count:
        raise ValueError(
            f"Expected {expected_question_count} questions, found {len(questions)}."
        )

    question_ids = [question["id"] for question in questions]
    if len(question_ids) != len(set(question_ids)):
        raise ValueError("Question IDs must be unique.")

    actual_counts = {category_id: 0 for category_id in category_ids}
    for question in questions:
        required = {"id", "category", "prompt", "answer", "explanation"}
        if not required.issubset(question):
            raise ValueError(
                f"{question.get('id', '<unknown>')} is missing "
                f"{sorted(required - set(question))}."
            )
        if question["category"] not in actual_counts:
            raise ValueError(
                f"{question['id']} references unknown category {question['category']}."
            )
        actual_counts[question["category"]] += 1

    expected_total = 0
    for category in categories:
        expected = category["question_bank_size"]
        actual = actual_counts[category["id"]]
        expected_total += expected
        if expected != actual:
            raise ValueError(
                f"{category['id']} expects {expected} questions but contains {actual}."
            )
    if expected_total != expected_question_count:
        raise ValueError(
            f"Category sizes total {expected_total}, not {expected_question_count}."
        )


def new_state(bank: dict[str, Any], track: str) -> dict[str, Any]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "language": track,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "sequence_number": 0,
        "active_question": None,
        "categories": {
            category["id"]: {
                "label": category["label"],
                "question_bank_size": category["question_bank_size"],
                "questions_given": 0,
                "correct": 0,
                "percent_correct": None,
            }
            for category in bank["categories"]
        },
        "questions": {
            question["id"]: {
                "times_asked": 0,
                "times_correct": 0,
                "last_asked_sequence": None,
                "last_result": None,
            }
            for question in bank["questions"]
        },
    }


def migrate_state(state: dict[str, Any]) -> bool:
    version = state.get("schema_version", 1)
    if version == STATE_SCHEMA_VERSION:
        return False
    if version != 1:
        raise ValueError(f"Unsupported progress schema version: {version}.")

    for question_state in state.get("questions", {}).values():
        asked = question_state.get("times_asked", 0)
        correct = question_state.get("times_correct", 0)
        if asked == 0:
            question_state["last_result"] = None
        elif correct == asked:
            question_state["last_result"] = "correct"
        else:
            question_state["last_result"] = "incorrect"
    state["schema_version"] = STATE_SCHEMA_VERSION
    return True


def synchronize_state_to_bank(
    state: dict[str, Any],
    bank: dict[str, Any],
    track: str,
) -> bool:
    """Import matching question history after an explicitly declared bank revision."""
    bank_categories = category_map(bank)
    bank_questions = questions_by_id(bank)
    state_categories = state.get("categories", {})
    state_questions = state.get("questions", {})

    shape_matches = (
        set(state_categories) == set(bank_categories)
        and set(state_questions) == set(bank_questions)
        and all(
            state_categories[category_id].get("label") == category["label"]
            and state_categories[category_id].get("question_bank_size")
            == category["question_bank_size"]
            for category_id, category in bank_categories.items()
        )
    )
    if shape_matches:
        return False

    migration = bank.get("progress_migration", {})
    if migration.get("strategy") != "preserve_matching_question_ids":
        return False

    replacement = new_state(bank, track)
    replacement["created_at"] = state.get("created_at", replacement["created_at"])
    replacement["sequence_number"] = state.get("sequence_number", 0)

    for question_id in set(state_questions).intersection(bank_questions):
        replacement["questions"][question_id] = state_questions[question_id]

    retired = dict(state.get("retired_questions", {}))
    for question_id, question_state in state_questions.items():
        if question_id not in bank_questions and question_state.get("times_asked", 0) > 0:
            retired[question_id] = question_state
    if retired:
        replacement["retired_questions"] = retired

    active_question = state.get("active_question")
    if active_question in bank_questions:
        replacement["active_question"] = active_question

    for question_id, question_state in replacement["questions"].items():
        category_id = bank_questions[question_id]["category"]
        metrics = replacement["categories"][category_id]
        metrics["questions_given"] += question_state["times_asked"]
        metrics["correct"] += question_state["times_correct"]

    for metrics in replacement["categories"].values():
        given = metrics["questions_given"]
        metrics["percent_correct"] = (
            None if given == 0 else round(100 * metrics["correct"] / given, 1)
        )

    replacement["updated_at"] = utc_now()
    replacement["bank_revision"] = migration.get("revision")
    state.clear()
    state.update(replacement)
    return True


def ensure_state(
    repo_root: Path,
    bank: dict[str, Any],
    track: str,
) -> tuple[Path, dict[str, Any]]:
    path = state_path(repo_root, track)
    if not path.exists():
        state = new_state(bank, track)
        write_json(path, state)
        return path, state
    state = load_json(path)
    changed = migrate_state(state)
    if synchronize_state_to_bank(state, bank, track):
        changed = True
    if changed:
        state["updated_at"] = utc_now()
        write_json(path, state)
    validate_state(state, bank, track)
    return path, state


def validate_state(
    state: dict[str, Any],
    bank: dict[str, Any],
    track: str,
) -> None:
    if state.get("schema_version") != STATE_SCHEMA_VERSION:
        raise ValueError(
            f"Progress state must use schema version {STATE_SCHEMA_VERSION}."
        )
    if state.get("language") != track:
        raise ValueError(f"Progress state must have language={track!r}.")
    bank_categories = category_map(bank)
    if set(state.get("categories", {})) != set(bank_categories):
        raise ValueError("Progress categories do not match the question bank.")
    bank_questions = questions_by_id(bank)
    if set(state.get("questions", {})) != set(bank_questions):
        raise ValueError("Progress question IDs do not match the question bank.")
    active_question = state.get("active_question")
    if active_question is not None and active_question not in bank_questions:
        raise ValueError("The active question does not exist in the question bank.")

    category_totals = {
        category_id: {"questions_given": 0, "correct": 0}
        for category_id in bank_categories
    }
    for question_id, question_state in state["questions"].items():
        asked = question_state["times_asked"]
        correct = question_state["times_correct"]
        last_sequence = question_state["last_asked_sequence"]
        last_result = question_state.get("last_result")
        if not isinstance(asked, int) or not isinstance(correct, int):
            raise ValueError(f"Question counters must be integers for {question_id}.")
        if asked < 0 or correct < 0 or correct > asked:
            raise ValueError(f"Invalid question counters for {question_id}.")
        if last_result not in (None, "correct", "incorrect"):
            raise ValueError(f"Invalid last_result for {question_id}.")
        if asked == 0 and (last_sequence is not None or last_result is not None):
            raise ValueError(f"Unseen question {question_id} has result history.")
        if asked > 0 and (not isinstance(last_sequence, int) or last_result is None):
            raise ValueError(f"Seen question {question_id} lacks result history.")
        category_id = bank_questions[question_id]["category"]
        category_totals[category_id]["questions_given"] += asked
        category_totals[category_id]["correct"] += correct

    for category_id, metrics in state["categories"].items():
        if metrics["question_bank_size"] != bank_categories[category_id]["question_bank_size"]:
            raise ValueError(f"Bank size drift detected for {category_id}.")
        given = metrics["questions_given"]
        correct = metrics["correct"]
        if given != category_totals[category_id]["questions_given"]:
            raise ValueError(f"Question count drift detected for {category_id}.")
        if correct != category_totals[category_id]["correct"]:
            raise ValueError(f"Correct count drift detected for {category_id}.")
        expected = None if given == 0 else round(100 * correct / given, 1)
        if metrics["percent_correct"] != expected:
            raise ValueError(f"Incorrect percent_correct for {category_id}.")


def select_question(
    bank: dict[str, Any],
    state: dict[str, Any],
    requested_category: str | None,
) -> dict[str, Any]:
    if state["active_question"] is not None:
        return questions_by_id(bank)[state["active_question"]]

    categories = category_map(bank)
    if requested_category is not None and requested_category not in categories:
        options = ", ".join(categories)
        raise SystemExit(f"Unknown category '{requested_category}'. Choose from: {options}")

    candidates = [
        question
        for question in bank["questions"]
        if requested_category is None or question["category"] == requested_category
    ]
    sequence = state["sequence_number"]
    question_states = state["questions"]
    category_order = {
        category["id"]: index for index, category in enumerate(bank["categories"])
    }

    due_misses = [
        question
        for question in candidates
        if question_states[question["id"]]["last_result"] == "incorrect"
        and sequence - question_states[question["id"]]["last_asked_sequence"]
        >= REVIEW_GAP
    ]
    if due_misses:
        return min(
            due_misses,
            key=lambda question: (
                question_states[question["id"]]["last_asked_sequence"],
                question["id"],
            ),
        )

    unseen = [
        question
        for question in candidates
        if question_states[question["id"]]["times_asked"] == 0
    ]
    if unseen:
        return min(
            unseen,
            key=lambda question: (
                category_order[question["category"]],
                question["id"],
            ),
        )

    return min(
        candidates,
        key=lambda question: (
            question_states[question["id"]]["times_correct"]
            / question_states[question["id"]]["times_asked"],
            question_states[question["id"]]["last_asked_sequence"],
            question["id"],
        ),
    )


def question_payload(bank: dict[str, Any], question: dict[str, Any]) -> dict[str, Any]:
    category = category_map(bank)[question["category"]]
    return {
        "question_id": question["id"],
        "category": question["category"],
        "category_label": category["label"],
        "prompt": question["prompt"],
    }


def activated_question_payload(
    bank: dict[str, Any],
    state: dict[str, Any],
    question: dict[str, Any],
) -> dict[str, Any]:
    payload = question_payload(bank, question)
    if state["questions"][question["id"]]["times_asked"] == 0:
        payload["mode"] = "initial"
        return payload

    payload["mode"] = "review"
    payload["review_source"] = {
        "prompt": question["prompt"],
        "answer": question["answer"],
        "explanation": question["explanation"],
    }
    return payload


def apply_result(
    bank: dict[str, Any],
    state: dict[str, Any],
    result: str,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    question_id = state["active_question"]
    if question_id is None:
        raise SystemExit("There is no active question to record.")

    question = questions_by_id(bank)[question_id]
    is_correct = result == "correct"
    state["sequence_number"] += 1
    sequence = state["sequence_number"]

    question_state = state["questions"][question_id]
    question_state["times_asked"] += 1
    question_state["times_correct"] += int(is_correct)
    question_state["last_asked_sequence"] = sequence
    question_state["last_result"] = result

    metrics = state["categories"][question["category"]]
    metrics["questions_given"] += 1
    metrics["correct"] += int(is_correct)
    metrics["percent_correct"] = round(
        100 * metrics["correct"] / metrics["questions_given"], 1
    )

    state["active_question"] = None
    state["updated_at"] = utc_now()
    return question_id, question, metrics


def persist_result(
    repo_root: Path,
    path: Path,
    state: dict[str, Any],
    question_id: str,
    result: str,
    track: str,
) -> None:
    write_json(path, state)
    if result == "incorrect":
        append_json_line(
            mistakes_path(repo_root, track),
            {"question_id": question_id, "last_result": "incorrect"},
        )


def recorded_payload(
    question_id: str,
    question: dict[str, Any],
    result: str,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    return {
        "recorded": question_id,
        "result": result,
        "category": question["category"],
        "category_metrics": metrics,
    }


def command_init(args: argparse.Namespace) -> None:
    bank = bank_data(args.track)
    repo_root = find_repo_root(Path(args.repo_root))
    path, state = ensure_state(repo_root, bank, args.track)
    log_path = mistakes_path(repo_root, args.track)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.touch()
    print(
        json.dumps(
            {
                "state_path": str(path),
                "mistakes_path": str(log_path),
                "categories": state["categories"],
            },
            indent=2,
        )
    )


def command_validate(args: argparse.Namespace) -> None:
    bank = bank_data(args.track)
    repo_root = find_repo_root(Path(args.repo_root))
    path, state = ensure_state(repo_root, bank, args.track)
    validate_state(state, bank, args.track)
    print(
        json.dumps(
            {
                "valid": True,
                "track": args.track,
                "question_count": len(bank["questions"]),
                "category_count": len(bank["categories"]),
                "state_path": str(path),
                "mistakes_path": str(mistakes_path(repo_root, args.track)),
            },
            indent=2,
        )
    )


def command_next(args: argparse.Namespace) -> None:
    bank = bank_data(args.track)
    repo_root = find_repo_root(Path(args.repo_root))
    path, state = ensure_state(repo_root, bank, args.track)
    question = select_question(bank, state, args.category)
    state["active_question"] = question["id"]
    state["updated_at"] = utc_now()
    write_json(path, state)
    print(json.dumps(activated_question_payload(bank, state, question), indent=2))


def command_sample(args: argparse.Namespace) -> None:
    bank = bank_data(args.track)
    state = new_state(bank, args.track)
    question = select_question(bank, state, args.category)
    print(json.dumps(question_payload(bank, question), indent=2))


def command_record(args: argparse.Namespace) -> None:
    bank = bank_data(args.track)
    repo_root = find_repo_root(Path(args.repo_root))
    path, state = ensure_state(repo_root, bank, args.track)
    question_id, question, metrics = apply_result(bank, state, args.result)
    persist_result(repo_root, path, state, question_id, args.result, args.track)
    print(
        json.dumps(
            recorded_payload(
                question_id,
                question,
                args.result,
                metrics,
            ),
            indent=2,
        )
    )


def command_advance(args: argparse.Namespace) -> None:
    bank = bank_data(args.track)
    repo_root = find_repo_root(Path(args.repo_root))
    path, state = ensure_state(repo_root, bank, args.track)
    question_id, question, metrics = apply_result(bank, state, args.result)

    next_question = select_question(bank, state, args.category)
    state["active_question"] = next_question["id"]
    state["updated_at"] = utc_now()
    persist_result(repo_root, path, state, question_id, args.result, args.track)

    print(
        json.dumps(
            {
                **recorded_payload(
                    question_id,
                    question,
                    args.result,
                    metrics,
                ),
                "next_question": activated_question_payload(
                    bank,
                    state,
                    next_question,
                ),
            },
            indent=2,
        )
    )


def command_mistakes(args: argparse.Namespace) -> None:
    bank = bank_data(args.track)
    repo_root = find_repo_root(Path(args.repo_root))
    ensure_state(repo_root, bank, args.track)
    path = mistakes_path(repo_root, args.track)
    questions = questions_by_id(bank)
    retired_questions = {
        question["id"]: question for question in bank.get("retired_questions", [])
    }
    question_history = {**retired_questions, **questions}
    resolved = []
    for line_number, entry in enumerate(load_json_lines(path), start=1):
        if set(entry) != {"question_id", "last_result"}:
            raise ValueError(
                f"Mistakes log line {line_number} must contain only "
                "question_id and last_result."
            )
        question_id = entry["question_id"]
        if question_id not in question_history:
            raise ValueError(
                f"Mistakes log line {line_number} references unknown question "
                f"{question_id!r}."
            )
        if entry["last_result"] != "incorrect":
            raise ValueError(
                f"Mistakes log line {line_number} must have last_result='incorrect'."
            )
        question = question_history[question_id]
        resolved.append(
            {
                **entry,
                "category": question["category"],
                "prompt": question["prompt"],
                "answer": question["answer"],
                "explanation": question["explanation"],
            }
        )
    print(
        json.dumps(
            {"mistakes_path": str(path), "mistakes": resolved},
            indent=2,
            ensure_ascii=False,
        )
    )


def command_status(args: argparse.Namespace) -> None:
    bank = bank_data(args.track)
    repo_root = find_repo_root(Path(args.repo_root))
    _, state = ensure_state(repo_root, bank, args.track)
    print(json.dumps({"categories": state["categories"]}, indent=2))


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--repo-root",
        default=".",
        help="Any path inside the repository (default: current directory).",
    )
    result.add_argument(
        "--track",
        choices=tuple(TRACKS),
        default=DEFAULT_TRACK,
        help=f"Drill track to use (default: {DEFAULT_TRACK}).",
    )
    subparsers = result.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize progress if missing.")
    init_parser.set_defaults(handler=command_init)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate the bank and progress state."
    )
    validate_parser.set_defaults(handler=command_validate)

    next_parser = subparsers.add_parser("next", help="Select and activate one question.")
    next_parser.add_argument("--category")
    next_parser.set_defaults(handler=command_next)

    sample_parser = subparsers.add_parser(
        "sample", help="Return an unscored question without changing progress."
    )
    sample_parser.add_argument("--category")
    sample_parser.set_defaults(handler=command_sample)

    record_parser = subparsers.add_parser(
        "record", help="Record the result for the active question."
    )
    record_parser.add_argument(
        "--result", choices=("correct", "incorrect"), required=True
    )
    record_parser.set_defaults(handler=command_record)

    advance_parser = subparsers.add_parser(
        "advance",
        help="Record the model's verdict and activate the next question.",
    )
    advance_parser.add_argument(
        "--result", choices=("correct", "incorrect"), required=True
    )
    advance_parser.add_argument("--category")
    advance_parser.set_defaults(handler=command_advance)

    mistakes_parser = subparsers.add_parser(
        "mistakes", help="Resolve append-only mistake entries to bank questions."
    )
    mistakes_parser.set_defaults(handler=command_mistakes)

    status_parser = subparsers.add_parser("status", help="Show category metrics.")
    status_parser.set_defaults(handler=command_status)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
