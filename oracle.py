from enum import Enum
from square_board import *
from copy import deepcopy

class ColumnClassification(Enum):
	FULL	= -1
	MAYBE	= 0
	WIN		= 100

class ColumnRecommendation():
	def __init__(self, index, classification):
		self.index = index
		self.classification = ColumnClassification(classification)

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False
		return self.classification == other.classification

	def __hash__(self) -> int:
		return hash((self.index, self.classification))

	def __repr__(self):
		return f"ColumnRecomendation({self.index}, {self.classification})"

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
				recommendations.append(ColumnRecommendation(line, -1))
		return recommendations

	def __repr__(self) -> str:
		return f"Class Oracle()"

class SmartOracle(BaseOracle):
	def get_recommendation(self, board, player = None):
		"""
		It refines super's calssification and tries to find Win columns
		"""
		recommendation = super().get_recommendation(board, player)
		for i in range (len(recommendation)):
			if recommendation[i].classification.value == 0:
				if self._is_winning_move(board, i, player):
					recommendation[i] = ColumnRecommendation(i, 100)
		print(recommendation)
		return recommendation

	def _is_winning_move(self, board, index, player):
		"""
		it checks if playing in the column would make the player win
		"""
		c_board = deepcopy(board)
		player._play_on(c_board, index)
		if c_board.is_victory(player.char):
			return True
		return False

