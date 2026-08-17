"""The eval suite stays runnable: valid JSON, known keys, one assertion per case.

The cases run against a live instance via protoAgent's eval runner
(``python -m evals.runner --tasks-file .../cowork-plugin/evals/tasks.json``);
this host-free test only guards the file's shape, so a typo'd key fails here
instead of silently asserting nothing there.
"""

from __future__ import annotations

import json
from pathlib import Path

TASKS = Path(__file__).resolve().parent.parent / "evals" / "tasks.json"

# The runner ignores unknown keys, so a misspelled assertion key would pass
# vacuously — this vocabulary is the tripwire.
ALLOWED_KEYS = {
    "id",
    "category",
    "kind",
    "name",
    "prompt",
    "expected_tools",
    "expected_any_tools",
    "forbidden_tools",
    "expected_patterns",
    "forbidden_patterns",
    "tool_outcome",
    "verify_kb",
    "verify_rubric",
    "setup",
    "teardown",
    "requires_env",
}

ASSERTION_KEYS = {
    "expected_tools",
    "expected_any_tools",
    "forbidden_tools",
    "expected_patterns",
    "forbidden_patterns",
    "verify_kb",
    "verify_rubric",
}


def _cases() -> list[dict]:
    return json.loads(TASKS.read_text(encoding="utf-8"))


def test_tasks_parse_with_unique_prefixed_ids():
    cases = _cases()
    assert cases, "empty suite"
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids)), "duplicate case ids"
    assert all(i.startswith("cowork_") for i in ids), "ids must be cowork_-prefixed"


def test_every_case_is_an_ask_with_known_keys():
    for c in _cases():
        assert c["kind"] == "ask", c["id"]
        assert c.get("prompt", "").strip(), c["id"]
        assert c.get("category", "").startswith("cowork-"), c["id"]
        unknown = set(c) - ALLOWED_KEYS
        assert not unknown, f"{c['id']}: unknown keys {sorted(unknown)}"


def test_every_case_asserts_something():
    for c in _cases():
        assert ASSERTION_KEYS & set(c), f"{c['id']} asserts nothing"
