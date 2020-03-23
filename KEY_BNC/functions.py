import math
import string
import re

def is_number(word):
    r"""
    Returns True if it is a number

    >>> is_number('1245')
    True

    >>> is_number('12:45')
    True

    >>> is_number('12a')
    False
    """
    search=re.compile(r'[^0-9.,:]').search
    return not bool(search(word))

word_breaks = string.whitespace+string.punctuation+'“”‘’…"–•—′\x85'
def tokenize(data):
    r"""
    Tokenize data into words
    1) Add space before punct if space follows punct
    2) Add space before apostrophe
    3) Tokenize on spaces

    >>> list(tokenize("'adventure 2'adventure"))
    ['adventure', '2', 'adventure']

    >>> list(tokenize("You're fine, fire-truck!"))
    ['you', "'re", 'fine', 'fire', 'truck']

    >>> list(tokenize("This is a 'quotation'."))
    ['this', 'is', 'a', 'quotation']

    >>> list(tokenize('So is "this"'))
    ['so', 'is', 'this']

    >>> list(tokenize("There are 100,000,000,000.00 words in the BNC."))
    ['there', 'are', '100,000,000,000.00', 'words', 'in', 'the', 'bnc']

    >>> list(tokenize("\"'tis!\" replied Aunt Helga."))
    ['tis', 'replied', 'aunt', 'helga']

    >>> list(tokenize("Don't tell someone what they can or can't do"))
    ['don', "'t", 'tell', 'someone', 'what', 'they', 'can', 'or', 'can', "'t", 'do']
    """
    data += '  '   # Append space to make sure we get the last character
    prev_char = ''
    curr_char = ''
    next_char = ''
    word = ''

    for next_char in data.lower():
        do_yield = True
        # If it is a colon/comma/period in a number, join
        if curr_char in ',.:' and prev_char in string.digits and next_char in string.digits:
            do_yield = False
        elif curr_char in "'’":
            if prev_char == '' or prev_char in word_breaks or prev_char in string.digits or next_char in word_breaks:
                curr_char = ''
            else:
                if not word == '':
                    yield word
                word = ''
                curr_char = "'"
                do_yield = False
        elif curr_char in word_breaks:
            curr_char = ''
        else:
            do_yield = False

        if do_yield and not word == '':
            yield word
            word = ''
        else:
            word += curr_char

        prev_char, curr_char = curr_char, next_char

def is_word(word):
    r"""
    >>> is_word('test')
    True

    >>> is_word('!')
    False

    >>> is_word('.')
    False
    """
    if len(word) == 1 and word not in string.ascii_letters+string.digits:
        return False
    return True

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
