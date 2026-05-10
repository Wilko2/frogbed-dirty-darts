# Milestone 03 — Ring and Resolved Dart Validation

## Goal

Make sure every resolved dart has valid score logic.

Milestone 02 created the pure board model. This milestone creates and validates the resolved dart layer that later systems will use when a dart has already landed.

A resolved dart should represent a real scored result such as:

- S20 = 20
- D20 = 40
- T20 = 60
- Outer Bull = 25
- Bullseye = 50

## Dependencies

- Milestone 02 must be merged into `main`.
- `core/board.py` must exist.
- `python -m pytest` must pass before starting.

## Expected files / areas

- `core/models.py`
- `core/board.py`
- `tests/test_resolved_darts.py`

## Must include

- A clear way to represent a resolved numbered dart.
- A clear way to represent a resolved bull dart.
- A score helper that uses `core.board`, not duplicated scoring logic.
- Validation that numbered darts use segments 1–20.
- Validation that numbered darts only use valid number rings.
- Validation that bull darts only use bull rings.
- Tests proving S20, D20, T20, Outer Bull, and Bullseye score correctly.
- Tests proving invalid segment/ring combinations fail clearly.

## Suggested design

Use the existing board helpers from `core/board.py`.

Do not duplicate the board scoring table.

Possible structure (alternative to the two-type model in `core/models.py`):

```python
@dataclass(frozen=True)
class ResolvedDart:
    segment: int | None
    number_ring: NumberRing | None
    bull_ring: BullRing | None
    score: int
```

## Explicitly out of scope

- Future dart generation
- Dirty darts
- Play detection
- Candidate generation
- Visit resolving
- Coasters
- Enemies
- UI

## Acceptance criteria

- [x] Code/design output exists for this milestone
- [x] Tests pass, where applicable
- [x] No later milestone features added
- [x] No previous milestone behaviour deleted
- [x] Manual check documented

## Manual check

From the repository root:

```bash
python -m pytest
```

Expected: all tests pass (including `tests/test_resolved_darts.py`).

## Completion notes

- **What changed:** Added `core/models.py` with `ResolvedNumberDart`, `ResolvedBullDart`, resolve/score helpers delegating to `core.board`. Added `tests/test_resolved_darts.py`.
- **What remains unsolved:** No unified “miss” or off-board resolved dart; no visit package or leg context.
- **Risks:** Callers must use the factories or dataclasses as intended so bull and number paths stay separated.