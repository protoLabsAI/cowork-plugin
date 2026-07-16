"""cowork — the knowledge-work skill pack behind protoAgent's Cowork archetype.

Skills only (ADR 0083 D3: original clean-room document skills — Anthropic's
Cowork skills are all-rights-reserved and must never be vendored here).
Host-only imports stay lazy; there are none today.
"""

from __future__ import annotations

import logging

log = logging.getLogger("protoagent.plugins.cowork")


def register(registry) -> None:
    try:
        registry.register_skill_dir("skills")
    except Exception:  # noqa: BLE001
        log.exception("[cowork] registering skills failed")

    log.info("[cowork] registered")
