from KEY_BNC.functions import is_number
from collections import Counter

class CorpusPart():

	def __init__(self, words):
		self.words_all = Counter()
		self.words_numberless = {}

		self.size_all = 0
		self.size_numberless = 0

		self.setWords(words)

	def setWords(self, value):
		self.words_all = Counter(value)
		self.words_numberless = Counter({k:v for k, v in self.words_all.items() if not is_number(k)})

		self.size_all = size_from_words(self.words_all)
		self.size_numberless = size_from_words(self.words_numberless)

	def getWords(self, should_ignore_numbers):
		if should_ignore_numbers:
			return self.words_numberless
		return self.words_all

	def getSize(self, should_ignore_numbers):
		if should_ignore_numbers:
			return self.size_numberless
		return self.size_all

def size_from_words(words):
	r"""
	Counts total number of words

	>>> words = {'a': 12, 'b': 2, 'c': 0}
	>>> o = corpus_part()
	>>> o.size_from_words(words)
	14
	"""
	return sum(words.values())
