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
