---
name: setup-cowork
description: Guided first-run setup for the Cowork archetype — connect folders and tools, import existing Claude Code/Cowork state, try a document skill, set up a writing voice, and wire the first scheduled task.
user_facing: true
slash: setup-cowork
---

# Cowork setup

Walk the operator from "fresh install" to "this already works like my
workspace, but it's mine". Six steps, one at a time, every one skippable.
Keep each message to a few sentences. If they wander into real work
mid-setup, help with it, then pick up where you left off.

## 1. Frame it

Two or three sentences: this agent handles multi-step knowledge work —
reports, spreadsheets, decks, research — as real files, on their machine,
with their choice of model. Skills run via `/`, plugins add capabilities,
everything is inspectable. Then: "Let's take a few minutes to set it up."

## 2. Folders

Deliverables need somewhere to land. Ask which folders the agent should
work in (Documents / Desktop / a projects dir), and have the operator wire
them in Settings ▸ Tools (the fenced filesystem tools). State the contract
plainly: those folders only, and never a permanent delete without asking.

## 3. Import what they already have

If the claude-bridge plugin is enabled, offer to look at their existing
Claude Code/Cowork state: memory for context, and any **user-authored**
skills worth migrating (Anthropic's own bundled skills are licensed to
their services and are not imported — this pack's document skills replace
them). Summarize what you find before importing anything; import only what
they approve.

## 4. Connect their tools

Inventory what's enabled (Gmail/Calendar/Drive via the Google plugin, notes,
artifacts) and point them at Settings ▸ Plugins for whatever's missing. If
`requires_pip` packages for the document skills aren't installed yet, have
them run install-deps now — it's one click and everything downstream needs
it.

## 5. Prove it, then personalize it

Offer one real task from their actual work ("point me at a messy folder or
a spreadsheet"), run it end to end with the relevant document skill, and
name the file you produced. Then offer the writing-voice skill: what it
does, that it takes two minutes, that nothing saves without review — and
that skipping is fine (they can just ask later).

## 6. Wrap with the habit

Show what recurring work looks like: "Anything we did today can run on a
schedule — say 'every Friday' and it happens." If a natural candidate came
up during setup, offer to schedule it now (schedule skill). Close with:
type `/` to see skills, and ask for anything the way they'd ask a
colleague.
