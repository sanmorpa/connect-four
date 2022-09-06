import pytest
from list_outils import *

# tests for the outils 
def test_fin_one():
	needle = 1
	none = [0, 0, 5, 's']
	beginning = [1, None, 9, 6, 0, 0]
	end = ['x', '0', 1]
	several = [0, 0, 3, 4, 1, 3, 2, 1, 2, 4]

	assert find_one(none, needle) == False
	assert find_one(beginning, needle)
	assert find_one(end, needle)
	assert find_one(several, needle)

def test_fin_one():
	needle = 1
	none = [0, 0, 5, 's']
	beginning = [1, None, 9, 6, 0, 0]
	end = ['x', '0', 1]
	several = [0, 0, 3, 4, 1, 3, 2, 1, 2, 4]

	assert find_one(none, needle) == False
	assert find_one(beginning, needle)
	assert find_one(end, needle)
	assert find_one(several, needle)

def test_find_n():
	assert find_n([2, 3, 4, 5, 6], 2, -1) == False
	assert find_n([1, 2, 3, 4, 5], 42, 2) == False
	assert find_n([1, 2, 3, 4, 5], 1, 2) == False
	assert find_n([1, 3, 4, 5], 2, 0)
	assert find_n([1, 2, 3, 2, 4, 5], 2, 2)
	assert find_n([1, 2, 3, 2, 4, 5, 4, 6, 4, 7, 4, 6], 4, 2)

def test_find_streak():
	assert find_streak([2, 3, 4, 5, 6], 2, -1) == False
	assert find_streak([1, 2, 3, 4, 5], 42, 2) == False
	assert find_streak([1, 2, 3, 4, 5], 1, 2) == False
	assert find_streak([1, 2, 3, 4], 4, 1)
	assert find_streak([1, 2, 3, 1, 2], 2, 2) == False
	assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 3)
	assert find_streak([5, 5, 5, 5, 1, 2, 3, 4], 5, 3)
	assert find_streak([1, 2, 5, 5, 5, 5, 3, 4], 5, 3)
	assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 4) == False