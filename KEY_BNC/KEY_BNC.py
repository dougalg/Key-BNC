from KEY_BNC.functions import *
from operator import itemgetter
import os, csv, string, collections

data_dirs = ['KEY_BNC', 'Data']
BNC_wordlist = r'BNC_wordlist.csv'

class KEY_BNC(object):

    def __init__(self):
        self.zero_adjustment = 0.5 # Default frequency for calculating OR which
                                  # requires a non-zero frequency

        self.bnc_words = self.load_BNC_data()
        self.bnc_corpus_size = self.size_from_words(self.bnc_words)

        self.sort_reverse = True
        self.sort_col = None
        self.sort_key = None
        self.set_sort(3)

        self.clear()

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

    def get_stats(self):
        r"""
        Runs the statistics and returns the results as a list of tuples:
        [ (word, f, f_bnc, LL, OR), ... ] sorted by f
        """
        return sorted([(w, self.target_words[w], self.bnc_words.get(w, 0), self.LL(w), self.OR(w)) for w in self.target_words], key=self.sort_key, reverse=self.sort_reverse)

    def size_from_words(self, words):
        r"""
        Counts total number of words

        >>> words = {'a': 12, 'b': 2, 'c': 0}
        >>> o = LLORBNCer()
        >>> o.size_from_words(words)
        14
        """
        return sum(words.values())

    def clear(self):
        self.target_words = collections.Counter()
        self.target_corpus_size = 0

    def load_file(self, file_name, func=None, indecipherable_files=None):
        if indecipherable_files is None:
            indecipherable_files = {'ignored':[],'guessed':[]}

        results = self.target_words
        fn, f = os.path.split(file_name)
        fn, ext = os.path.splitext(file_name)
        if ext == '.txt':
            error = None
            try:
                with open(file_name, encoding='utf8') as fh:
                    results.update(self.words_from_text(fh.read()))
            except UnicodeDecodeError:
                try:
                    with open(file_name, encoding='latin-1', errors='surrogateescape') as fh:
                        results.update(self.words_from_text(fh.read()))
                        indecipherable_files['guessed'].append(f)
                except UnicodeDecodeError:
                    indecipherable_files['ignored'].append(f)
            if func is not None and error is None:
                func(f)
        else:
            indecipherable_files['ignored'].append(f)

        self.target_words = results
        return indecipherable_files

    def load_target_file(self, file_name, func=None):
        indecipherable_files = self.load_file(file_name, func)
        self.target_corpus_size = self.size_from_words(self.target_words)
        return indecipherable_files

    def load_target_data_dir(self, dir_name, func=None):
        indecipherable_files = {'ignored':[],'guessed':[]}

        for root, dirs, files in os.walk(dir_name):
            for f in files:
                fname = os.path.join(root, f)
                indecipherable_files = self.load_file(fname, func, indecipherable_files)

        self.target_corpus_size = self.size_from_words(self.target_words)

        return indecipherable_files

    def words_from_text(self, data):
        r"""
        Tokenize data into words
        1) Add space before punct if space follows punct
        2) Add space before apostrophe
        3) Tokenize on spaces

        >>> o = LLORBNCer()
        >>> list(o.words_from_text("You're fine, fire-truck!"))
        ['you', "'re", 'fine', ',', 'fire-truck', '!']
        """
        word = ''
        num_char = len(data)
        for i, c in enumerate(data):
            c = c.lower()
            if c in ['"', '“', '”', '‘', '(', ')', '{', '}', '[', ']']:
                if word != '':
                    yield word
                yield c
                word = ''
            elif c not in string.punctuation:
                if c in string.whitespace:
                    if word != '':
                        yield word
                    word = ''
                else:
                    word += c
            elif c in ["'", '’'] or (i+1 < num_char and data[i+1] in string.whitespace) or i+1 == num_char:
                if word != '':
                    yield word
                word = c
            else:
                word += c

            if i+1 == num_char and word != '':
                yield word

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
        BNC_wordlist_path = os.path.join(data_dirs[0], data_dirs[1], BNC_wordlist)
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
