"""register() wires the skill dir through the registry seam, host-free."""

from __future__ import annotations

import cowork_plugin


def test_register_contributes_skills(registry):
    cowork_plugin.register(registry)
    assert registry.skill_dirs == ["skills"]


def test_register_survives_a_broken_registry():
    class Broken:
        config = {}

        def register_skill_dir(self, path):
            raise RuntimeError("boom")

    cowork_plugin.register(Broken())  # must not raise
