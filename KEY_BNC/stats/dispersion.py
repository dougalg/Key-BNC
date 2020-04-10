# dp_norm(DP, min_s)
def dp_norm(s, v, f):
	r"""
	Calculates the normalized dispersion based:
	s: An array of the percentages of the n corpus part sizes
	v: An array of the frequencies of the target word in each corpus part
	f: The overall frequency of the target word in the corpus

	>>> s = (0.18, 0.2, 0.2, 0.2, 0.22)
	>>> v = (1, 2, 3, 4, 5)
	>>> f = 15
	>>> dp_norm(s, v, f)
	0.2195121951219512

	>>> s = (0.9,0.1)
	>>> v = (9,1)
	>>> f = 10
	>>> dp_norm(s, v, f)
	0.0

	>>> s = (0.9,0.1)
	>>> v = (10,0)
	>>> f = 10
	>>> dp_norm(s, v, f)
	0.1111111111111111

	>>> s = (1,)
	>>> v = (10,)
	>>> f = 10
	>>> dp_norm(s, v, f)
	Traceback (most recent call last):
	 File "/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/lib/python3.7/doctest.py", line 1330, in __run
		compileflags, 1), test.globs)
	 File "<doctest dispersion.dp_norm[15]>", line 1, in <module>
		dp_norm(s, v, f)
	 File "KEY_BNC/stats/dispersion.py", line 40, in dp_norm
		return dp(s, v, f) / (1 - min(s))
	ZeroDivisionError: float division by zero
	"""
	return dp(s, v, f) / (1 - min(s))

def dp(s, v, f):
	r"""
	Calculates the dispersion for a word based on:
	s: An array of the percentages of the n corpus part sizes
	v: An array of the frequencies of the target word in each corpus part
	f: The overall frequency of the target word in the corpus

	>>> s = (0.18, 0.2, 0.2, 0.2, 0.22)
	>>> v = (1, 2, 3, 4, 5)
	>>> f = 15
	>>> dp(s, v, f)
	0.18
	"""
	assert len(s) == len(v), "The number of part sizes, and frequencies must be the same."

	calculated_parts = map(calculate_part_value, s, v, [f for i in v])

	return 0.5 * sum(calculated_parts)

def calculate_part_value(size_percentage, frequency, overall_frequency):
	return abs((frequency / overall_frequency) - size_percentage)