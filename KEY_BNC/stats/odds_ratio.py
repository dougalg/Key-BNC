def OR(
        target_freq,
        target_corpus_size,
        comparison_freq,
        comparison_corpus_size,
        zero_adjustment=None
    ):
    r"""
    Based on the definition found at:
    http://www.medcalc.org/manual/relativerisk_oddsratio.php

    >>> OR(12,24,12,24)
    1.0

    >>> OR(100, 105, 12, 24)
    20.0

    Division by 0 returns infinity
    >>> OR(12,12,100,1000)
    inf

    Can be ignored with a zero_adjustment value
    >>> OR(12,12,100,1000, zero_adjustment=0.5)
    224.00497512437812

    >>> OR(1,10000000,10**-9,1000000000000)
    100000010000000.98
    """

    a = float(target_freq)
    b = float(target_corpus_size - target_freq)
    c = float(comparison_freq)
    d = float(comparison_corpus_size - comparison_freq)

    if 0 in [b, c, d] and zero_adjustment is not None:
        a, b, c, d = [i+zero_adjustment for i in [a, b, c, d]]

    try:
        return (a/b)/(c/d)
    except (FloatingPointError, ZeroDivisionError):
        return float('inf')