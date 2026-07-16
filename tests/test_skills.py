"""Every skill parses against protoAgent's SKILL.md contract (ADR 0060)."""

from __future__ import annotations

from pathlib import Path

import yaml

SKILLS = Path(__file__).resolve().parent.parent / "skills"

EXPECTED = {
    "docx",
    "xlsx",
    "pptx",
    "pdf",
    "schedule",
    "consolidate-memory",
    "writing-voice",
    "setup-cowork",
}


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---"), f"{path} lacks frontmatter"
    _, fm, body = text.split("---", 2)
    data = yaml.safe_load(fm)
    assert body.strip(), f"{path} has an empty body"
    return data


def test_expected_skill_set():
    assert {p.name for p in SKILLS.iterdir() if p.is_dir()} == EXPECTED


def test_every_skill_meets_the_loader_contract():
    for d in sorted(SKILLS.iterdir()):
        fm = _frontmatter(d / "SKILL.md")
        assert fm["name"] == d.name, f"{d.name}: frontmatter name must match the folder"
        desc = fm["description"]
        assert desc and len(desc) <= 1024, f"{d.name}: description missing or over the 1024-char cap"


def test_setup_skill_is_slash_invocable():
    fm = _frontmatter(SKILLS / "setup-cowork" / "SKILL.md")
    assert fm.get("user_facing") is True
    assert fm.get("slash") == "setup-cowork"


def test_no_anthropic_licensed_material_vendored():
    # ADR 0083 D3: Anthropic's Cowork skills are all-rights-reserved and must
    # never be copied into this pack. Tripwire, not a formality.
    for path in SKILLS.rglob("*"):
        assert path.name != "LICENSE.txt", f"vendored license file at {path}"
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            assert "Anthropic, PBC" not in text, f"Anthropic-licensed text in {path}"
