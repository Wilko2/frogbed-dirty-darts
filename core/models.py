"""Resolved dart types: a scored landing on the board, using `core.board` for all math."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from core.board import BullRing, NumberRing, score_bull_hit, score_number_hit

ResolvedDart: TypeAlias = "ResolvedNumberDart | ResolvedBullDart"


@dataclass(frozen=True)
class ResolvedNumberDart:
    """A hit on the numbered spider (single, double, or triple)."""

    segment: int
    ring: NumberRing

    def __post_init__(self) -> None:
        # All segment and ring rules live in `core.board`; keep this type honest.
        score_number_hit(self.segment, self.ring)


@dataclass(frozen=True)
class ResolvedBullDart:
    """Outer bull or bullseye only — never combined with a segment multiplier."""

    ring: BullRing

    def __post_init__(self) -> None:
        score_bull_hit(self.ring)


def resolve_number_dart(segment: int, ring: NumberRing) -> ResolvedNumberDart:
    """Build a validated resolved numbered dart (segment must be 1–20, ring a number ring)."""
    return ResolvedNumberDart(segment=segment, ring=ring)


def resolve_bull_dart(ring: BullRing) -> ResolvedBullDart:
    """Build a validated resolved bull dart (ring must be a bull ring, not double/triple wire)."""
    return ResolvedBullDart(ring=ring)


def score_resolved_number(dart: ResolvedNumberDart) -> int:
    """Points for a resolved numbered dart (delegates to `core.board`)."""
    return score_number_hit(dart.segment, dart.ring)


def score_resolved_bull(dart: ResolvedBullDart) -> int:
    """Points for a resolved bull dart (delegates to `core.board`)."""
    return score_bull_hit(dart.ring)


def score_resolved(dart: ResolvedDart) -> int:
    """Dispatch scoring for either resolved dart shape."""
    if isinstance(dart, ResolvedNumberDart):
        return score_resolved_number(dart)
    if isinstance(dart, ResolvedBullDart):
        return score_resolved_bull(dart)
    raise TypeError(f"unsupported resolved dart type: {type(dart).__name__}")
