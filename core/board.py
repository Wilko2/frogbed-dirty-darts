"""Pure dartboard geometry and scoring helpers (segment order, rings, bulls).

This module models the fixed standard wire order only — no physics, UI, or play rules.
"""

from __future__ import annotations

from enum import Enum


# Standard clockface order clockwise beginning at 12 o'clock (segment 20 at the top).
STANDARD_SEGMENT_ORDER: tuple[int, ...] = (
    20,
    1,
    18,
    4,
    13,
    6,
    10,
    15,
    2,
    17,
    3,
    19,
    7,
    16,
    8,
    11,
    14,
    9,
    12,
    5,
)

SEGMENT_COUNT: int = len(STANDARD_SEGMENT_ORDER)

OUTER_BULL_SCORE: int = 25
BULLSEYE_SCORE: int = 50

# First ten segments clockwise from the top wire; the remainder form the lower hemisphere.
_UPPER_HEMISPHERE: frozenset[int] = frozenset(STANDARD_SEGMENT_ORDER[: SEGMENT_COUNT // 2])
_LOWER_HEMISPHERE: frozenset[int] = frozenset(STANDARD_SEGMENT_ORDER[SEGMENT_COUNT // 2 :])


class NumberRing(str, Enum):
    """Scoring ring on the numbered spider (single / double / triple)."""

    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"


class BullRing(str, Enum):
    """Bull area; doubles/triples on the number ring do not apply here."""

    OUTER_BULL = "outer_bull"
    BULLSEYE = "bullseye"


_SEGMENT_TO_INDEX: dict[int, int] = {
    value: index for index, value in enumerate(STANDARD_SEGMENT_ORDER)
}


def _require_valid_segment(segment: int) -> None:
    if segment not in _SEGMENT_TO_INDEX:
        raise ValueError(f"expected segment 1–20, got {segment!r}")


def segment_index(segment: int) -> int:
    """Return the 0-based index of this segment in `STANDARD_SEGMENT_ORDER`."""
    _require_valid_segment(segment)
    return _SEGMENT_TO_INDEX[segment]


def segment_at_clockwise_index(index: int) -> int:
    """Segment occupying the given clockwise index, wrapping every `SEGMENT_COUNT` steps."""
    if not isinstance(index, int):
        raise TypeError(f"index must be int, not {type(index).__name__}")
    return STANDARD_SEGMENT_ORDER[index % SEGMENT_COUNT]


def clockwise_neighbour(segment: int) -> int:
    """Next segment when moving clockwise (following `STANDARD_SEGMENT_ORDER`)."""
    i = segment_index(segment)
    return STANDARD_SEGMENT_ORDER[(i + 1) % SEGMENT_COUNT]


def anticlockwise_neighbour(segment: int) -> int:
    """Next segment when moving anti-clockwise."""
    i = segment_index(segment)
    return STANDARD_SEGMENT_ORDER[(i - 1) % SEGMENT_COUNT]


def distance_around_board(segment_a: int, segment_b: int) -> int:
    """Minimum number of neighbour steps along the ring between two segments (0–10)."""
    ia = segment_index(segment_a)
    ib = segment_index(segment_b)
    forward = (ib - ia) % SEGMENT_COUNT
    backward = (ia - ib) % SEGMENT_COUNT
    return min(forward, backward)


def ring_multiplier(ring: NumberRing) -> int:
    """Multiplier applied to the segment number for singles, doubles, or triples."""
    if ring is NumberRing.SINGLE:
        return 1
    if ring is NumberRing.DOUBLE:
        return 2
    if ring is NumberRing.TRIPLE:
        return 3
    raise AssertionError("unhandled NumberRing")


def bull_score(ring: BullRing) -> int:
    """Fixed scores: outer bull 25, bullseye 50."""
    if ring is BullRing.OUTER_BULL:
        return OUTER_BULL_SCORE
    if ring is BullRing.BULLSEYE:
        return BULLSEYE_SCORE
    raise AssertionError("unhandled BullRing")


def is_prime_segment_value(value: int) -> bool:
    """True iff `value` is prime (intended for dart segment numbers 1–20)."""
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    r = int(value**0.5) + 1
    for d in range(3, r, 2):
        if value % d == 0:
            return False
    return True


def is_high_prime_segment_value(value: int) -> bool:
    """Primes strictly greater than 10 on the board (11, 13, 17, 19)."""
    return value > 10 and is_prime_segment_value(value)


def is_upper_hemisphere(segment: int) -> bool:
    _require_valid_segment(segment)
    return segment in _UPPER_HEMISPHERE


def is_lower_hemisphere(segment: int) -> bool:
    _require_valid_segment(segment)
    return segment in _LOWER_HEMISPHERE


def same_hemisphere(segment_a: int, segment_b: int) -> bool:
    _require_valid_segment(segment_a)
    _require_valid_segment(segment_b)
    return (segment_a in _UPPER_HEMISPHERE) == (segment_b in _UPPER_HEMISPHERE)


def score_number_hit(segment: int, ring: NumberRing) -> int:
    """Points for a hit on the numbered spider: segment value × ring multiplier."""
    _require_valid_segment(segment)
    return segment * ring_multiplier(ring)


def score_bull_hit(ring: BullRing) -> int:
    """Points for the outer bull or bullseye (no segment multiplier)."""
    return bull_score(ring)
