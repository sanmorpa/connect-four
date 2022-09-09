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

def transpose(matrix):
	"""
	Transposes a list of lists
	"""
	transposed = []
	for i in range(len(matrix[0])):
		transposed.append(list())
	for n in matrix:
		iter = 0
		for item in n:
			transposed[iter].append(item)
			iter += 1
	return transposed

def displace(line, pos, char = None):
	"""
	Returns a displaced list o line. It moves it pos times to the right (pos > 0) or left (pos < 0) and fills the rest with char items
	"""
	if pos == 0 or len(line) == 0:
		return line
	elif pos > 0:
		filled = [char] * pos
		displaced = filled + line
		return displaced[:-pos]
	else:
		if (pos * -1) > len(line):
			pos = (len(line) * -1)
		displaced = line[pos * -1:]
		displaced += [char] * (pos * -1)
		return displaced

def displace_matrix(matrix, char = None):
	"""
	It returns a list of displaced lists
	"""
	new = list()
	for i in range(len(matrix)):
		new.append(displace(matrix[i], i - 1, char))
	return new

def reverse_list(list):
	"""
	It returns a reversed list
	"""
	return list[::-1]

def reverse_matrix(matrix):
	"""
	It returns a list of reversed lists
	"""
	new = list()
	for item in matrix:
		new.append(reverse_list(item))
	return new