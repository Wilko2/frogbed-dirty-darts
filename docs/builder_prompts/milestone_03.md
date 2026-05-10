# Cursor Builder Agent prompt for Milestone 03

You are the Builder Agent for FrogBed / Dirty Darts.

Implement Milestone 03 only.

Read these files first:

- `AGENTS.md`
- `docs/milestones/milestone_03.md`
- `core/board.py`

Before coding, reply with:

1. Current milestone number
2. Dependencies
3. Files you will touch
4. Tests you will add/change
5. What is explicitly out of scope

Expected files to create/edit:

- `core/models.py`
- `tests/test_resolved_darts.py`
- `docs/milestones/milestone_03.md` only if adding manual check/completion notes

Goal:

Create/validate the resolved dart layer that uses the Milestone 02 board helpers.

Must include:

- a clean representation of a resolved numbered dart
- a clean representation of a resolved bull dart
- helper for resolving/scoring numbered darts
- helper for resolving/scoring bull darts
- validation that segments are 1–20
- validation that numbered darts use valid number rings
- validation that bull darts use valid bull rings
- tests for S20, D20, T20, Outer Bull, Bullseye
- tests for invalid segment/ring combinations

Design requirements:

- Reuse `core.board` scoring helpers.
- Do not duplicate dartboard scoring logic.
- Keep models small and simple.
- Do not implement future darts.
- Do not implement dirty darts.
- Do not implement play detection.
- Do not implement candidate generation.
- Do not implement visit resolving.
- Do not implement coasters.
- Do not implement enemies.
- Do not implement UI.

After coding:

- Run `python -m pytest` if your environment allows it.
- Summarise changed files.
- Summarise unresolved issues.
