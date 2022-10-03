from enum import Enum
from syslog import LOG_USER
from square_board import *
from copy import deepcopy
from settings import BOARD_LENGTH

class ColumnClassification(Enum):
	FULL	= -1
	LOSE	= 5
	MAYBE	= 10
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
				recommendations.append(ColumnRecommendation(line, 10))
			else:
				recommendations.append(ColumnRecommendation(line, -1))
		return recommendations

	def __repr__(self) -> str:
		return f"Class Oracle()"

class SmartOracle(BaseOracle):
	def get_recommendation(self, board, player = None):
		"""
		It refines super's calssification and tries to find Win or lose columns
		"""
		recommendation = super().get_recommendation(board, player)
		for i in range (len(recommendation)):
			if recommendation[i].classification == ColumnClassification.MAYBE:
				if self._is_winning_move(board, i, player) == True:
					recommendation[i].classification = ColumnClassification.WIN
				elif self._is_losing_move(board, i, player) == True:
					recommendation[i].classification = ColumnClassification.LOSE
			print(recommendation[i])
		return recommendation

	def _is_winning_move(self, board, index, player):
		"""
		it checks if playing in the column would make the player win
		"""
		c_board = deepcopy(board)
		c_board.play(player.char, index)
		return c_board.is_victory(player.char)

	def _is_losing_move(self, board, index, player):
		"""
		it checks if playing in the column would make the opponent win the next round
		"""
		c_board = deepcopy(board)
		c_board.play(player.char, index)
		for i in range(0, BOARD_LENGTH):
			cc_board = c_board
			if None in board._board[index]:
				if self._is_winning_move(cc_board, i, player.opponent):
					return True
		return False

