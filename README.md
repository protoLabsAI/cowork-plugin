# cowork-plugin

The skill pack behind [protoAgent](https://github.com/protoLabsAI/protoAgent)'s
**Cowork archetype** (ADR 0083) — for knowledge workers graduating from Claude
Cowork to a self-hosted agent whose deliverables are real files.

## Skills

| Skill | What it does |
|---|---|
| `docx` / `xlsx` / `pptx` / `pdf` | Produce and edit Word/Excel/PowerPoint/PDF deliverables via `execute_code` + the standard Python libraries |
| `schedule` | Distill the current session into a self-contained prompt and run it on any cron cadence or one-shot |
| `consolidate-memory` | Reflective maintenance pass over long-term memory — merge, retire, sharpen |
| `writing-voice` | Learn the operator's voice from samples they share; saved as a `my-writing-style` skill |
| `/setup-cowork` | Guided first-run: folders → import existing Claude Code/Cowork state (via claude-bridge) → connect tools → try a skill → voice → first schedule |

## Licensing note (ADR 0083 D3)

These document skills are **original, clean-room work** over `python-docx`,
`openpyxl`, `python-pptx`, `pypdf`, and `reportlab`. Anthropic's Cowork skills
are all-rights-reserved and are not used here; a test tripwire
(`test_no_anthropic_licensed_material_vendored`) keeps it that way.

## Install

Normally installed by the [`cowork-stack`](https://github.com/protoLabsAI/cowork-stack)
bundle (picked as the **Cowork** archetype in setup or fleet-create). Standalone:

```
plugin install https://github.com/protoLabsAI/cowork-plugin
```

Then enable `cowork` and run install-deps for the `requires_pip` packages.
Document skills expect the `execute_code` plugin to be enabled.

## Development

```
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt ruff
.venv/bin/pytest -q     # host-free
```
