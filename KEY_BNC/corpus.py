from KEY_BNC.constants import data_dirs, BNC_wordlist
from KEY_BNC.functions import *
from KEY_BNC.corpus_part import CorpusPart
from KEY_BNC.stats.dispersion import dp_norm
from KEY_BNC.stats.odds_ratio import OR
from KEY_BNC.stats.log_likelyhood import LL
from operator import itemgetter
import os, csv, string, collections
from collections import Counter


class Corpus(object):

	def __init__(self, file_basepath=None):
		self.zero_adjustment = 0.5  # Default frequency for calculating OR which
									# requires a non-zero frequency

		# Do we want to ignore numbers?
		# This will affect counts of types and tokens and therefore
		# also the LL/OR values
		self.ignore_numbers = False
		self.file_basepath = file_basepath or '.'

		self.corpus_parts = []
		self.bnc_corpus = CorpusPart(self.load_BNC_data())

		self.sort_reverse = True
		self.sort_col = None
		self.sort_key = None

		# Set default sort key to LL
		self.set_sort(3)

		self.clear()

	@property
	def bnc_words(self):
		return self.bnc_corpus.getWords(self.ignore_numbers)

	@property
	def bnc_corpus_size(self):
		return self.bnc_corpus.getSize(self.ignore_numbers)

	@property
	def target_corpus_size(self):
		counts = [part.getSize(self.ignore_numbers) for part in self.corpus_parts]
		return sum(counts)

	@property
	def target_words(self):
		counts = [part.getWords(self.ignore_numbers) for part in self.corpus_parts]
		return sum(counts, Counter())

	def get_cols(self):
		return ["Word Type", "Frequency", "Frequency BNC", "Log Likelihood", "Odds Ratio", "Dispersion"]

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
		return sorted([
			self.get_stats_for_word(w) for w in self.target_words if self.is_valid(w, target_words)],
			key=self.sort_key,
			reverse=self.sort_reverse
		)

	def get_stats_for_word(self, w):
		return (
			w,
			self.target_words[w],
			self.bnc_words.get(w, 0),
			self.LL(w),
			self.OR(w),
			self.dp_norm(w)
		)

	def clear(self):
		self.corpus_parts = []

	def load_file(self, file_name, func=None, indecipherable_files=None):
		if indecipherable_files is None:
			indecipherable_files = {'ignored':[],'guessed':[]}

		fn, f = os.path.split(file_name)
		fn, ext = os.path.splitext(file_name)
		if ext == '.txt':
			error = None
			try:
				with open(file_name, encoding='utf8') as fh:
					self.corpus_parts.append(CorpusPart(tokenize(fh.read())))
			except UnicodeDecodeError:
				try:
					with open(file_name, encoding='latin-1', errors='surrogateescape') as fh:
						self.corpus_parts.append(CorpusPart(tokenize(fh.read())))
						indecipherable_files['guessed'].append(f)
				except UnicodeDecodeError:
					indecipherable_files['ignored'].append(f)
			if func is not None and error is None:
				func(f)
		else:
			indecipherable_files['ignored'].append(f)

		return indecipherable_files

	def load_target_file(self, file_name, func=None):
		return self.load_file(file_name, func)

	def load_target_data_dir(self, dir_name, func=None):
		indecipherable_files = {'ignored':[],'guessed':[]}

		for root, dirs, files in os.walk(dir_name):
			for f in files:
				fname = os.path.join(root, f)
				indecipherable_files = self.load_file(fname, func, indecipherable_files)

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
		return LL(
			self.target_words[target_word],
			self.target_corpus_size,
			self.bnc_words.get(target_word, 0),
			self.bnc_corpus_size
		)

	def OR(self, target_word):
		r"""
		A convenience method to calculate OR

		Replaces BNC F 0, with 10^-10
		"""
		return OR(
			self.target_words[target_word],
			self.target_corpus_size,
			self.bnc_words.get(target_word, 0),
			self.bnc_corpus_size,
			zero_adjustment = self.zero_adjustment
		)

	def dp_norm(self, target_word):
		r"""
		A convenience method to calculate normalized dispersion for a word
		"""
		s = [ part.getSize(self.ignore_numbers) / self.target_corpus_size for part in self.corpus_parts ]
		v = [ part.getWords(self.ignore_numbers)[target_word] for part in self.corpus_parts ]
		return dp_norm(s, v, self.target_words[target_word])
