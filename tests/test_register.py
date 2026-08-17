"""register() wires the skill dir through the registry seam, host-free."""

from __future__ import annotations

import cowork_plugin


def test_register_contributes_skills(registry):
    cowork_plugin.register(registry)
    assert registry.skill_dirs == ["skills"]


def test_register_contributes_folder_changed_verifier(registry):
    cowork_plugin.register(registry)
    fn, description = registry.verifiers["cowork:folder_changed"]
    assert callable(fn) and description


def test_register_survives_a_broken_registry():
    class Broken:
        config = {}

        def register_skill_dir(self, path):
            raise RuntimeError("boom")

    cowork_plugin.register(Broken())  # must not raise


def test_register_survives_a_host_without_verifiers():
    # An older host registry has no register_goal_verifier — skills must
    # still land and register() must not raise.
    class OldHost:
        config = {}

        def __init__(self):
            self.skill_dirs = []

        def register_skill_dir(self, path):
            self.skill_dirs.append(path)

    old = OldHost()
    cowork_plugin.register(old)
    assert old.skill_dirs == ["skills"]
