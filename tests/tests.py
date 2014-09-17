import unittest
from unittest import TestCase
from unittest.mock import MagicMock

import sys
sys.path.append('../')

from KEY_BNC.KEY_BNC import KEY_BNC

def doctests():
    from doctest import testmod
    from KEY_BNC import functions
    testmod(functions)

class KeyBNCTests(TestCase):

    def setUp(self):
        self.calculator = KEY_BNC(file_basepath='..')
        self.callback = MagicMock()

    def testWordCounts(self):
        # Check BNC wordcounts
        self.assertEqual(len(self.calculator.bnc_words), 439435)
        self.assertEqual(self.calculator.bnc_corpus_size, 99831892)

    def testWordCountsNN(self):
        # Check BNC wordcounts without numbers
        self.calculator.ignore_numbers = True
        self.assertEqual(len(self.calculator.bnc_words), 397036)
        self.assertEqual(self.calculator.bnc_corpus_size, 98628225)

    def testFileLoadOK(self):
        # Make sure it loads a file OK and calls the callback with the filename as argument
        test_file = './Data/Cayuga-Finite-State-Morphology.txt'

        bad_files = self.calculator.load_target_file(test_file, self.callback)
        self.assertEqual(bad_files, {'ignored': [], 'guessed': []})
        self.callback.assert_called_with('Cayuga-Finite-State-Morphology.txt')

    def testFileLoadBad(self):
        # Make sure it fails to load the file and does not call the callback
        test_file = './Data/Cayuga-Finite-State-Morphology.pdf'

        bad_files = self.calculator.load_target_file(test_file, self.callback)
        self.assertEqual(bad_files, {'ignored': ['Cayuga-Finite-State-Morphology.pdf'], 'guessed': []})
        self.assertEqual(self.callback.called, False)

    def testDirLoad(self):
        # Make sure it can load a dir OK
        test_dir = './Data'
        bad_files = self.calculator.load_target_data_dir(test_dir, self.callback)
        self.assertEqual(bad_files, {'ignored': ['Cayuga-Finite-State-Morphology.pdf'], 'guessed': ['Japanese.txt']})
        self.callback.has_calls(['Japanese.txt', 'Cayuga-Finite-State-Morphology.txt'])
        self.assertEqual(self.callback.call_count, 2)

    def testLLValues(self):
        # Test LL values against the BNC
        pass

    def testORValues(self):
        # Test OR values against the BNC
        pass

    def testSorting(self):
        pass

if __name__ == '__main__':
    doctests()
    unittest.main()
