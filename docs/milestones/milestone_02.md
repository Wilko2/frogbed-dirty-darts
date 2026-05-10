# Milestone 02 — Board Model

## Goal

Implement the dartboard as a pure model.

## Dependencies

- Previous milestone must be complete unless this is Milestone 00.
- `python -m pytest` must pass before starting.

## Expected files / areas

- `core/board.py`
- `tests/test_board.py`

## Must include

- `Standard dart order.`
- `Clockwise and anti-clockwise neighbours.`
- `Distance around board.`
- `Ring multiplier.`
- `Bull handling.`
- `Outer Bull = 25.`
- `Bullseye = 50.`
- `Prime and high-prime helpers.`
- `Hemisphere helpers.`
- `Score helper.`

## Explicitly out of scope

- Weighting
- future dart generation
- play detection
- visit resolving

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

From the repo root, run:

```bash
python -m pytest

## Completion notes

- What changed:
  - Added `core/board.py`.
  - Added `tests/test_board.py`.
  - Implemented fixed dartboard order, segment lookup, neighbours, distance, ring multipliers, bull scoring, prime helpers, hemisphere helpers, and score helpers.
- What remains unsolved:
  - Hemisphere convention is currently defined as first 10 vs last 10 segments in standard board order. This can be revisited later if the design needs a more visual/geometric split.
  - ResolvedDart validation and broader scoring integration are deliberately left for Milestone 03.
- Risks:
  - Later systems must not duplicate scoring logic; they should reuse these helpers.
