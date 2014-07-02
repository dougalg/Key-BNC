import unittest

def doctests():
    from doctest import testmod
    from KEY_BNC import functions
    testmod(functions)

# Check BNC wordcounts

# Test LL values against the BNC

# Test OR values against the BNC

if __name__ == '__main__':
    doctests()
    unittest.main()
