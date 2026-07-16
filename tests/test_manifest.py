"""Manifest sanity + the ADR 0083 contracts."""

from __future__ import annotations

import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _manifest() -> dict:
    return yaml.safe_load((ROOT / "protoagent.plugin.yaml").read_text())


def test_identity_and_trust_defaults():
    m = _manifest()
    assert m["id"] == "cowork"
    assert m["enabled"] is False
    assert isinstance(m["config_section"], str)


def test_version_lockstep_with_pyproject():
    py = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert _manifest()["version"] == py["project"]["version"]


def test_document_skill_deps_declared():
    pips = _manifest()["requires_pip"]
    for pkg in ("python-docx", "openpyxl", "python-pptx", "pypdf", "reportlab"):
        assert pkg in pips


def test_capabilities_are_honest():
    caps = _manifest()["capabilities"]
    assert caps["network"] == [] and caps["filesystem"] == "none"
