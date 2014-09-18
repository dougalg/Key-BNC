from KEY_BNC.functions import *
from operator import itemgetter
import os, csv, string, collections

data_dirs = ['KEY_BNC', 'Data']
BNC_wordlist = r'BNC_wordlist.csv'

class KEY_BNC(object):

    def __init__(self, file_basepath=None):
        self.zero_adjustment = 0.5 # Default frequency for calculating OR which
                                  # requires a non-zero frequency

        # Do we want to ignore numbers?
        # This will affect counts of types and tokens and therefore
        # also the LL/OR values
        self.ignore_numbers = False
        self.file_basepath = file_basepath or '.'

        self.init_bnc_words()

        self.target_words = {}

        self.sort_reverse = True
        self.sort_col = None
        self.sort_key = None

        # Set default sort key to LL
        self.set_sort(3)

        self.clear()

    def init_bnc_words(self):
        # With numbers
        self.bnc_words_wn = self.load_BNC_data()
        self.bnc_corpus_size_wn = self.size_from_words(self.bnc_words)

        # No numbers
        self.bnc_words_nn = {k:v for k, v in self.bnc_words_wn.items() if not is_number(k)}
        self.bnc_corpus_size_nn = self.size_from_words(self.bnc_words_nn)

    @property
    def bnc_words(self):
        if self.ignore_numbers:
            return self.bnc_words_nn
        return self.bnc_words_wn

    @property
    def bnc_corpus_size(self):
        if self.ignore_numbers:
            return self.bnc_corpus_size_nn
        return self.bnc_corpus_size_wn

    @property
    def target_corpus_size(self):
        if self.ignore_numbers:
            return self.target_corpus_size_nn
        return self.target_corpus_size_wn

    @property
    def target_words(self):
        if self.ignore_numbers:
            return self.target_words_nn
        return self.target_words_wn

    @target_words.setter
    def target_words(self, value):
        self.target_words_wn = value
        self.target_words_nn = {k:v for k, v in self.target_words_wn.items() if not is_number(k)}

        self.target_corpus_size_wn = self.size_from_words(self.target_words_wn)
        self.target_corpus_size_nn = self.size_from_words(self.target_words_nn)

    def get_cols(self):
        return ["Word Type", "Frequency", "Frequency BNC", "Log Likelihood", "Odds Ratio"]

    def set_sort(self, col):
        if self.sort_col == col:
            self.sort_reverse = not self.sort_reverse # Reverse sort on 2nd click
        else:
            self.sort_reverse = True

        if col == 0:
            self.sort_reverse = not self.sort_reverse # Word sort needs a reverse

        self.sort_col = col
        self.sort_key = itemgetter(col)

    def is_valid(self, word, target_words):
        return target_words == [] or word in target_words

    def get_stats(self, for_words=None):
        r"""
        Runs the statistics and returns the results as a list of tuples:
        [ (word, f, f_bnc, LL, OR), ... ] sorted by self.sort_key

        filter to specific words with a list: KEY_BNC.get_stats(for_words=['and', 'the'])
        will return only 2 results
        """
        target_words = for_words or []
        return sorted([(w, self.target_words[w], self.bnc_words.get(w, 0), self.LL(w), self.OR(w)) for w in self.target_words if self.is_valid(w, target_words)], key=self.sort_key, reverse=self.sort_reverse)

    def size_from_words(self, words):
        r"""
        Counts total number of words

        >>> words = {'a': 12, 'b': 2, 'c': 0}
        >>> o = KEY_BNC()
        >>> o.size_from_words(words)
        14
        """
        return sum(words.values())

    def clear(self):
        self.target_words = collections.Counter()

    def load_file(self, file_name, func=None, indecipherable_files=None):
        if indecipherable_files is None:
            indecipherable_files = {'ignored':[],'guessed':[]}

        results = self.target_words_wn
        fn, f = os.path.split(file_name)
        fn, ext = os.path.splitext(file_name)
        if ext == '.txt':
            error = None
            try:
                with open(file_name, encoding='utf8') as fh:
                    results.update(tokenize(fh.read()))
            except UnicodeDecodeError:
                try:
                    with open(file_name, encoding='latin-1', errors='surrogateescape') as fh:
                        results.update(tokenize(fh.read()))
                        indecipherable_files['guessed'].append(f)
                except UnicodeDecodeError:
                    indecipherable_files['ignored'].append(f)
            if func is not None and error is None:
                func(f)
        else:
            indecipherable_files['ignored'].append(f)

        self.target_words_wn = results
        return indecipherable_files

    def load_target_file(self, file_name, func=None):
        results = self.load_file(file_name, func)
        self.target_words = self.target_words_wn
        return results

    def load_target_data_dir(self, dir_name, func=None):
        indecipherable_files = {'ignored':[],'guessed':[]}

        for root, dirs, files in os.walk(dir_name):
            for f in files:
                fname = os.path.join(root, f)
                indecipherable_files = self.load_file(fname, func, indecipherable_files)

        self.target_words = self.target_words_wn
        return indecipherable_files

    def load_BNC_data(self):
        r"""
        Loads and returns a dictionary of the BNC data from CSV
        This is a large file (10MB) and will consume significant memory

        The keys are words, the values a tuple:
        {
            'word1': (frequency1, rank1),
            'word2': (frequency2, rank2),
            ...
        }
        """
        BNC_wordlist_path = os.path.join(self.file_basepath, data_dirs[0], data_dirs[1], BNC_wordlist)
        data = {}
        with open(BNC_wordlist_path, encoding='utf8') as bnc_data:
            reader = csv.reader(bnc_data)
            headers = reader.__next__()
            data = {word: int(f) for rank, f, word in reader}

        return data

    def LL(self, target_word):
        r"""
        A convenience method to calculate LL
        """
        return LL(self.target_words[target_word], self.target_corpus_size,
                  self.bnc_words.get(target_word, 0), self.bnc_corpus_size)

    def OR(self, target_word):
        r"""
        A convenience method to calculate OR

        Replaces BNC F 0, with 10^-10
        """
        return OR(self.target_words[target_word], self.target_corpus_size,
                  self.bnc_words.get(target_word, 0), self.bnc_corpus_size,
                  zero_adjustment = self.zero_adjustment)
