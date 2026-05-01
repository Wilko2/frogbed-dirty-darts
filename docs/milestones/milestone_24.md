# Milestone 24 — Next-Visit Weight Modifiers from State

## Goal

States affect future dart generation.

## Dependencies

- Previous milestone must be complete unless this is Milestone 00.
- `python -m pytest` must pass before starting.

## Expected files / areas

- `systems/weighting.py`
- `systems/future_darts.py`
- `systems/state_resolver.py`
- `tests/test_state_weight_modifiers.py`

## Must include

- `RUN biases adjacent continuation tiles.`
- `FROGBED PRESSURE biases repeated tile/ring.`
- `PARITY_ODD biases odd tiles.`
- `PARITY_EVEN biases even tiles.`
- `State from Visit 1 can affect dart generation in Visit 2.`

## Explicitly out of scope

- Coasters
- drinks
- rituals

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
