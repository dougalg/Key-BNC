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

class KeyBNCBaseTests(TestCase):

    def setUp(self):
        self.calculator = KEY_BNC(file_basepath='..')

    def testWordCounts(self):
        # Check BNC wordcounts
        self.assertEqual(len(self.calculator.bnc_words), 439435)
        self.assertEqual(self.calculator.bnc_corpus_size, 99831892)

    def testWordCountsNN(self):
        # Check BNC wordcounts without numbers
        self.calculator.ignore_numbers = True
        self.assertEqual(len(self.calculator.bnc_words), 397036)
        self.assertEqual(self.calculator.bnc_corpus_size, 98628225)

class KeyBNCFileTests(TestCase):

    def setUp(self):
        self.calculator = KEY_BNC(file_basepath='..')
        self.callback = MagicMock()

    def testFileLoadOK(self):
        # Make sure it loads a file OK and calls the callback with the filename as argument
        test_file = './Data/Cayuga-Finite-State-Morphology.txt'

        bad_files = self.calculator.load_target_file(test_file, self.callback)
        self.assertEqual(bad_files, {'ignored': [], 'guessed': []})
        self.callback.assert_called_with('Cayuga-Finite-State-Morphology.txt')
        self.assertEqual(self.calculator.target_corpus_size, 48052)

    def testFileLoadBad(self):
        # Make sure it fails to load the file and does not call the callback
        test_file = './Data/Cayuga-Finite-State-Morphology.pdf'

        bad_files = self.calculator.load_target_file(test_file, self.callback)
        self.assertEqual(bad_files, {'ignored': ['Cayuga-Finite-State-Morphology.pdf'], 'guessed': []})
        self.assertEqual(self.callback.called, False)
        self.assertEqual(self.calculator.target_corpus_size, 0)

    def testDirLoad(self):
        # Make sure it can load a dir OK
        test_dir = './Data'
        bad_files = self.calculator.load_target_data_dir(test_dir, self.callback)
        self.assertEqual(bad_files, {'ignored': ['Cayuga-Finite-State-Morphology.pdf'], 'guessed': ['Japanese.txt']})
        self.callback.has_calls(['Japanese.txt', 'Cayuga-Finite-State-Morphology.txt'])
        self.assertEqual(self.callback.call_count, 2)
        self.assertEqual(self.calculator.target_corpus_size, 48055)


class KeyBNCResultTests(TestCase):

    def testResults(self):

        calculator = KEY_BNC(file_basepath='..')
        test_dir = './Data'
        bad_files = calculator.load_target_data_dir(test_dir)
        words_to_check = ['the', 'cayuga', 'new']
        word_results = [('cayuga', 61, 0, 932.0041191087499, 255848.54050985005), 
                        ('new', 6, 125363, -80.96596656846012, 0.09931643412522852), 
                        ('the', 1431, 6057593, -932.2279330155097, 0.4751315170375143)]
        stats = calculator.get_stats(for_words=words_to_check)

        bnc_size = calculator.bnc_corpus_size
        test_corpus_size = calculator.target_corpus_size

        self.assertEqual(word_results, stats)


if __name__ == '__main__':
    doctests()
    unittest.main()
