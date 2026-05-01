# Milestone 03 — Ring and Resolved Dart Validation

## Goal

Make sure every resolved dart has valid score logic.

## Dependencies

- Previous milestone must be complete unless this is Milestone 00.
- `python -m pytest` must pass before starting.

## Expected files / areas

- `core/models.py`
- `core/board.py`
- `tests/test_resolved_darts.py`

## Must include

- `Validate ResolvedDart creation through helpers.`
- `Avoid duplicated score calculation.`
- `Add resolve_score(tile, ring) helper.`
- `Bulls cannot accidentally use double/triple rings.`

## Explicitly out of scope

- Future dart generation
- play detection
- dirty darts

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
