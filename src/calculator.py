def clamp(value: int, lower: int, upper: int) -> int:
    """Return value constrained to the inclusive lower/upper bounds."""
    lo, hi = min(lower, upper), max(lower, upper)
    return max(lo, min(value, hi))
