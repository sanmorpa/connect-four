def find_one(list, needle):
	"""
	Returns True if it encounters one or more occurences of needle in the list
	"""
	return find_n(list, needle, 1)

def find_n(list, needle, n):
	"""
	Returns True if it encounters n or more occurences of needle in the list. n < 0 will return False
	"""
	if n < 0:
		return False
	seen = 0
	for i in list:
		if i == needle: seen += 1
	return seen >= n

def find_streak(list, needle, n):
	"""
	Returns True if it encounters n or more adjacent occurences of needle in the list. n < 0 will return False
	"""
	if n < 0:
		return False
	seen = 0
	for i in list:
		if i == needle: seen += 1
		else: seen = 0
		if seen == n: break
	return seen >= n