import pytest

from core.board import BULLSEYE_SCORE, BullRing, NumberRing, OUTER_BULL_SCORE
from core.models import (
    ResolvedBullDart,
    ResolvedNumberDart,
    resolve_bull_dart,
    resolve_number_dart,
    score_resolved,
    score_resolved_bull,
    score_resolved_number,
)


def test_s20_d20_t20_scores():
    s20 = resolve_number_dart(20, NumberRing.SINGLE)
    d20 = resolve_number_dart(20, NumberRing.DOUBLE)
    t20 = resolve_number_dart(20, NumberRing.TRIPLE)
    assert score_resolved_number(s20) == 20
    assert score_resolved_number(d20) == 40
    assert score_resolved_number(t20) == 60
    assert score_resolved(s20) == 20
    assert score_resolved(d20) == 40
    assert score_resolved(t20) == 60


def test_outer_bull_and_bullseye_scores():
    outer = resolve_bull_dart(BullRing.OUTER_BULL)
    inner = resolve_bull_dart(BullRing.BULLSEYE)
    assert score_resolved_bull(outer) == OUTER_BULL_SCORE == 25
    assert score_resolved_bull(inner) == BULLSEYE_SCORE == 50
    assert score_resolved(outer) == 25
    assert score_resolved(inner) == 50


def test_invalid_segment_rejected_on_resolve():
    with pytest.raises(ValueError, match="expected segment"):
        resolve_number_dart(0, NumberRing.SINGLE)
    with pytest.raises(ValueError, match="expected segment"):
        resolve_number_dart(21, NumberRing.DOUBLE)


def test_invalid_segment_rejected_on_direct_construct():
    with pytest.raises(ValueError, match="expected segment"):
        ResolvedNumberDart(segment=99, ring=NumberRing.TRIPLE)


def test_bull_and_number_rings_are_not_interchangeable():
    # Type system keeps bull vs number rings apart; factories only accept the right enum.
    assert resolve_bull_dart(BullRing.OUTER_BULL).ring is BullRing.OUTER_BULL
    n = resolve_number_dart(1, NumberRing.SINGLE)
    assert n.ring in NumberRing
