# Milestone 00 — Freeze the Project Spine

## Goal

Protect the architecture before adding systems.

## Dependencies

- Previous milestone must be complete unless this is Milestone 00.
- `python -m pytest` must pass before starting.

## Expected files / areas

- `README.md`
- `constants.py`
- `core/enums.py`
- `core/models.py`
- `systems/`
- `content/`
- `ui/`

## Must include

- `No UI imports inside core or systems.`
- `No game rules hidden inside content.`
- `Existing dataclasses are not randomly rewritten.`
- `Tests still pass.`

## Explicitly out of scope

- Feature implementation
- visual UI work
- coasters
- dirty dart logic

## Agent pre-flight checklist

Before coding, state:

1. Current milestone number
2. Dependencies
3. Files you will touch
4. Tests you will add/change
5. What is explicitly out of scope

## Implementation tasks

- [ ] Read `AGENTS.md`
- [ ] Read this milestone file
- [ ] Implement only this milestone
- [ ] Add or update tests if code changed
- [ ] Run `python -m pytest`
- [ ] Add manual check instructions

## Acceptance criteria

- [ ] Code/design output exists for this milestone
- [ ] Tests pass, where applicable
- [ ] No later milestone features added
- [ ] No previous milestone behaviour deleted
- [ ] Manual check documented

## Manual check

Write exact commands and expected output here.

## Completion notes

- What changed:
- What remains unsolved:
- Risks:
