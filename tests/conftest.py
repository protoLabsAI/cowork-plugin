"""Test bootstrap — the plugin must import and register with NO protoAgent host."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PKG = "cowork_plugin"

if PKG not in sys.modules:
    _spec = importlib.util.spec_from_file_location(PKG, ROOT / "__init__.py", submodule_search_locations=[str(ROOT)])
    assert _spec and _spec.loader
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules[PKG] = _mod
    _spec.loader.exec_module(_mod)


class FakeRegistry:
    def __init__(self):
        self.config = {}
        self.skill_dirs = []

    def register_skill_dir(self, path):
        self.skill_dirs.append(path)


@pytest.fixture
def registry():
    return FakeRegistry()
