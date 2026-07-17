from calculator import clamp


def test_clamp_with_ordered_bounds():
    assert clamp(12, 0, 10) == 10
    assert clamp(-2, 0, 10) == 0
    assert clamp(5, 0, 10) == 5
