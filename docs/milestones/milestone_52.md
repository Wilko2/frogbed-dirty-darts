# Milestone 52 — The Big Design Fork

## Goal

Compare scoring models after alpha.

## Dependencies

- Previous milestone must be complete unless this is Milestone 00.
- `python -m pytest` must pass before starting.

## Expected files / areas

- `docs/design/big_design_fork.md`

## Must include

- `Model A: Best 3 Score, All 5 Event.`
- `Model B: First 3 Create State, All 5 Score.`
- `Model C: Dirty Darts Utility Only.`
- `Model D: Full State Visit Model.`
- `Do not switch away from Model A until Model A is playable and measured.`

## Explicitly out of scope

- Switching scoring model before alpha is measured

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
