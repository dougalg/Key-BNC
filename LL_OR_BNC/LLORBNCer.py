from LL_OR_BNC.functions import *
import LL_OR_BNC
import os, csv, string, collections

data_dir = r'LL_OR_BNC\Data'
BNC_wordlist = r'BNC_wordlist.csv'

class LLORBNCer(object):

    def __init__(self):
        self.bnc_words = self.load_BNC_data()
        self.bnc_corpus_size = self.size_from_words(self.bnc_words)

        self.target_words = {}
        self.target_corpus_size = 0

    def get_stats(self):
        r"""
        Runs the statistics and returns the results as a list of tuples:
        [ (word, f, f_bnc, LL, OL), ... ] sorted by f
        """
        return sorted([(w, self.target_words[w], self.bnc_words.get(w, 0), self.LL(w), self.OR(w)) for w in self.target_words], key=lambda x: x[1], reverse=True)

    def size_from_words(self, words):
        r"""
        Counts total number of words

        >>> words = {'a': 12, 'b': 2, 'c': 0}
        >>> o = LLORBNCer()
        >>> o.size_from_words(words)
        14
        """
        return sum(words.values())

    def load_target_data_dir(self, dir_name, func=None):
        results = collections.Counter()
        for root, dirs, files in os.walk(dir_name):
            for f in files:
                fname = os.path.join(root, f)
                with open(fname, encoding='utf8') as fh:
                    results.update(self.words_from_text(fh.read()))
                    if func is not None:
                        func(f)
        self.target_words = results
        self.target_corpus_size = self.size_from_words(self.target_words)

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
            if c in ['"', '“', '”', '‘']:
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
        BNC_wordlist_path = os.path.join(data_dir, BNC_wordlist)
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
        A convenience method to calculate LL
        """
        return OR(self.target_words[target_word], self.target_corpus_size,
                  self.bnc_words.get(target_word, 0), self.bnc_corpus_size)
