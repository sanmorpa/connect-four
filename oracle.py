from enum import Enum
from square_board import *

class ColumnClassification(Enum):
	FULL = 1
	MAYBE = 0

class ColumnRecommendation():
	def __init__(self, index, classification):
		self.index = index
		self.classification = ColumnClassification(classification)

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False
		return self.index == other.index and self.classification == other.classification

	def __hash__(self) -> int:
		return hash((self.index, self.classification))


class BaseOracle():
	def get_recommendation(self, board, player = None):
		"""
		Returns a list of ColumnRecommendations
		"""
		recommendations = list()
		for line in range(len(board)):
			if None in board._board[line]:
				recommendations.append(ColumnRecommendation(line, 0))
			else:
				recommendations.append(ColumnRecommendation(line, 1))
		return recommendations
