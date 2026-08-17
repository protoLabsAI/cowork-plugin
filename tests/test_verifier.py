"""cowork:folder_changed behaves: fence-honest, glob-aware, change-visible.

Host-free: the verifier lazy-imports ``graph.goals.types`` (host-only), so
these tests stub that module with the same three-field VerifyResult shape —
the frozen contract (met, reason, evidence).
"""

from __future__ import annotations

import asyncio
import sys
import types
from dataclasses import dataclass

import pytest

import cowork_plugin

if "graph.goals.types" not in sys.modules:

    @dataclass
    class _VerifyResult:
        met: bool
        reason: str = ""
        evidence: str = ""

    _graph = sys.modules.setdefault("graph", types.ModuleType("graph"))
    _goals = sys.modules.setdefault("graph.goals", types.ModuleType("graph.goals"))
    _types = types.ModuleType("graph.goals.types")
    _types.VerifyResult = _VerifyResult
    sys.modules["graph.goals.types"] = _types
    _graph.goals = _goals
    _goals.types = _types


class _Ctx:
    def __init__(self, roots):
        self.config = types.SimpleNamespace(
            effective_filesystem_projects=lambda: [{"name": r.name, "path": str(r)} for r in roots]
        )


def _run(spec, ctx):
    return asyncio.run(cowork_plugin._folder_changed(spec, ctx))


def _spec(**args):
    return {"type": "plugin", "check": "cowork:folder_changed", "args": args}


@pytest.fixture
def fenced(tmp_path):
    root = tmp_path / "work"
    root.mkdir()
    return root


def test_met_when_files_match_and_evidence_lists_them(fenced):
    (fenced / "report.pdf").write_bytes(b"x")
    r = _run(_spec(path=str(fenced), glob="*.pdf"), _Ctx([fenced]))
    assert r.met and "report.pdf" in r.evidence and "1 file(s)" in r.reason


def test_not_met_when_nothing_matches_but_still_verifies(fenced):
    r = _run(_spec(path=str(fenced), glob="*.pdf"), _Ctx([fenced]))
    assert not r.met and r.evidence == ""


def test_evidence_moves_on_delete(fenced):
    a, b = fenced / "a.csv", fenced / "b.csv"
    a.write_bytes(b"x")
    b.write_bytes(b"y")
    ctx = _Ctx([fenced])
    before = _run(_spec(path=str(fenced), glob="*.csv"), ctx).evidence
    b.unlink()
    after = _run(_spec(path=str(fenced), glob="*.csv"), ctx).evidence
    assert before != after and "b.csv" not in after


def test_recursive_opt_in(fenced):
    sub = fenced / "inbox"
    sub.mkdir()
    (sub / "deep.txt").write_bytes(b"x")
    flat = _run(_spec(path=str(fenced), glob="*.txt"), _Ctx([fenced]))
    deep = _run(_spec(path=str(fenced), glob="*.txt", recursive=True), _Ctx([fenced]))
    assert not flat.met and deep.met


def test_subfolder_of_a_fenced_root_is_inside_the_fence(fenced):
    sub = fenced / "drops"
    sub.mkdir()
    (sub / "f.txt").write_bytes(b"x")
    assert _run(_spec(path=str(sub)), _Ctx([fenced])).met


def test_outside_the_fence_is_refused(tmp_path, fenced):
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    r = _run(_spec(path=str(outside)), _Ctx([fenced]))
    assert not r.met and "outside the fenced" in r.reason


def test_no_fence_configured_is_refused(fenced):
    r = _run(_spec(path=str(fenced)), _Ctx([]))
    assert not r.met and "no fenced work folders" in r.reason


def test_missing_path_and_escaping_glob_are_refused(fenced):
    assert "args.path is required" in _run(_spec(), _Ctx([fenced])).reason
    r = _run(_spec(path=str(fenced), glob="../*"), _Ctx([fenced]))
    assert not r.met and "relative" in r.reason


def test_config_without_effective_helper_falls_back_to_raw_field(fenced):
    (fenced / "x.txt").write_bytes(b"x")
    ctx = types.SimpleNamespace(config=types.SimpleNamespace(filesystem_projects=[{"path": str(fenced)}]))
    assert _run(_spec(path=str(fenced)), ctx).met
