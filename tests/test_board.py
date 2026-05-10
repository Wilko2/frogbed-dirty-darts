import pytest

from core.board import (
    BULLSEYE_SCORE,
    BullRing,
    NumberRing,
    OUTER_BULL_SCORE,
    SEGMENT_COUNT,
    STANDARD_SEGMENT_ORDER,
    anticlockwise_neighbour,
    bull_score,
    clockwise_neighbour,
    distance_around_board,
    is_high_prime_segment_value,
    is_lower_hemisphere,
    is_prime_segment_value,
    is_upper_hemisphere,
    ring_multiplier,
    same_hemisphere,
    score_bull_hit,
    score_number_hit,
    segment_at_clockwise_index,
    segment_index,
)


def test_standard_segment_order_length_and_values():
    assert SEGMENT_COUNT == 20
    assert len(STANDARD_SEGMENT_ORDER) == 20
    assert set(STANDARD_SEGMENT_ORDER) == set(range(1, 21))


def test_standard_segment_order_starts_at_top_with_twenty():
    assert STANDARD_SEGMENT_ORDER[0] == 20
    assert STANDARD_SEGMENT_ORDER[1] == 1
    assert STANDARD_SEGMENT_ORDER[-1] == 5


def test_segment_lookup_round_trip():
    for i, seg in enumerate(STANDARD_SEGMENT_ORDER):
        assert segment_index(seg) == i
        assert segment_at_clockwise_index(i) == seg


def test_segment_at_clockwise_index_wraps():
    assert segment_at_clockwise_index(SEGMENT_COUNT) == STANDARD_SEGMENT_ORDER[0]
    assert segment_at_clockwise_index(-1) == STANDARD_SEGMENT_ORDER[-1]


def test_clockwise_neighbour_follows_standard_order():
    for seg in STANDARD_SEGMENT_ORDER:
        i = segment_index(seg)
        nxt = STANDARD_SEGMENT_ORDER[(i + 1) % SEGMENT_COUNT]
        assert clockwise_neighbour(seg) == nxt


def test_anticlockwise_neighbour_follows_standard_order():
    for seg in STANDARD_SEGMENT_ORDER:
        i = segment_index(seg)
        prev = STANDARD_SEGMENT_ORDER[(i - 1) % SEGMENT_COUNT]
        assert anticlockwise_neighbour(seg) == prev


def test_clockwise_and_anticlockwise_are_inverse_ops():
    s = 18
    assert anticlockwise_neighbour(clockwise_neighbour(s)) == s
    assert clockwise_neighbour(anticlockwise_neighbour(s)) == s


def test_distance_around_board_zero_for_same_segment():
    assert distance_around_board(10, 10) == 0


def test_distance_around_board_adjacent_is_one():
    assert distance_around_board(20, 1) == 1
    assert distance_around_board(5, 20) == 1


def test_distance_around_board_opposite_max_ten():
    # Halfway around the 20-segment ring (20 at index 0, 3 at index 10).
    assert distance_around_board(20, 3) == 10


def test_ring_multiplier_single_double_triple():
    assert ring_multiplier(NumberRing.SINGLE) == 1
    assert ring_multiplier(NumberRing.DOUBLE) == 2
    assert ring_multiplier(NumberRing.TRIPLE) == 3


def test_bull_scores_constants_and_helpers():
    assert OUTER_BULL_SCORE == 25
    assert BULLSEYE_SCORE == 50
    assert bull_score(BullRing.OUTER_BULL) == 25
    assert bull_score(BullRing.BULLSEYE) == 50
    assert score_bull_hit(BullRing.OUTER_BULL) == 25
    assert score_bull_hit(BullRing.BULLSEYE) == 50


def test_is_prime_segment_value_examples():
    assert is_prime_segment_value(1) is False
    assert is_prime_segment_value(2) is True
    assert is_prime_segment_value(4) is False
    assert is_prime_segment_value(17) is True
    assert is_prime_segment_value(20) is False


def test_is_high_prime_segment_value_examples():
    assert is_high_prime_segment_value(7) is False
    assert is_high_prime_segment_value(11) is True
    assert is_high_prime_segment_value(13) is True
    assert is_high_prime_segment_value(10) is False


def test_upper_and_lower_hemisphere_partition():
    upper = {s for s in STANDARD_SEGMENT_ORDER if is_upper_hemisphere(s)}
    lower = {s for s in STANDARD_SEGMENT_ORDER if is_lower_hemisphere(s)}
    assert len(upper) == 10
    assert len(lower) == 10
    assert upper | lower == set(STANDARD_SEGMENT_ORDER)
    assert upper & lower == set()
    assert 20 in upper
    assert 5 in lower


def test_same_hemisphere():
    assert same_hemisphere(20, 17) is True
    assert same_hemisphere(3, 5) is True
    assert same_hemisphere(20, 3) is False


def test_score_number_hit():
    assert score_number_hit(20, NumberRing.SINGLE) == 20
    assert score_number_hit(20, NumberRing.DOUBLE) == 40
    assert score_number_hit(7, NumberRing.TRIPLE) == 21


def test_invalid_segment_rejected():
    with pytest.raises(ValueError):
        segment_index(0)
    with pytest.raises(ValueError):
        is_upper_hemisphere(25)
    with pytest.raises(ValueError):
        same_hemisphere(1, 99)
