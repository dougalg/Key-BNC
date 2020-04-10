def LL(target_freq, target_corpus_size, comparison_freq, comparison_corpus_size):
    r"""
    Calculates Log Likelihood for a pair of words, given the corpus sizes
    and word frequencies

    A positive value shows that the frequency is greater in the target
    corpus than in the comparison corpus and a negative frequency
    vice-versa.

    Note: This should only be used if the target corpus can be considered a subset of the comparison corpus

    Based on: http://ucrel.lancs.ac.uk/llwizard.html

    >>> LL(1,2,3,4)
    -0.13133406903473888

    >>> LL(200, 80000, 2546, 10000000)
    542.1871524060532
    """

    target_freq, target_corpus_size, comparison_freq, comparison_corpus_size = float(target_freq), float(target_corpus_size), float(comparison_freq), float(comparison_corpus_size)
    f1mil_1 = target_freq / target_corpus_size * 1000000
    f1mil_2 = comparison_freq / comparison_corpus_size * 1000000

    expected_freq_1 = target_corpus_size * \
        (target_freq + comparison_freq) / (target_corpus_size + comparison_corpus_size)
    expected_freq_2 = comparison_corpus_size * \
        (target_freq + comparison_freq) / (target_corpus_size + comparison_corpus_size)

    log1 = logdivision(target_freq, expected_freq_1)
    log2 = logdivision(comparison_freq, expected_freq_2)

    ll = 2 * (
        (target_freq * log1) +
        (comparison_freq * log2)
    )

    if f1mil_1 < f1mil_2:
        return -ll

    return ll

def logdivision(target_freq, expected_freq):
    r"""
    Calculates the log of a division, and returns 0 if there is
    a division by zero error

    >>> logdivision(12, 4)
    1.0986122886681098

    >>> logdivision(100, 0)
    0.0
    """

    try:
        return math.log(target_freq / expected_freq)
    except (FloatingPointError, ZeroDivisionError, ValueError):
        return float(0)
