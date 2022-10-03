from enum import Enum
from syslog import LOG_USER
from square_board import *
from copy import deepcopy
from beautifultable import BeautifulTable
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

	def print_recommendation(self, board, player = None):
		recommendation = self.get_recommendation(board, player)
		rec = [list(i.classification.name) for i in recommendation]
		matrix = reverse_matrix(rec)
		print(matrix)
		bt = BeautifulTable()
		for col in matrix:
			bt.columns.append(col)
		print(bt)
		bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]
		print(bt)

	def __repr__(self) -> str:
		return f"Class BaseOracle()"

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
		return recommendation

	def _is_winning_move(self, board, index, player):
		"""
		it checks if playing in the column would make the player win
		"""
		if None not in board._board[index]:
			return False
		c_board = deepcopy(board)
		c_board.play(player.char, index)
		return c_board.is_victory(player.char)

	def _is_losing_move(self, board, index, player):
		"""
		it checks if playing in the column would make the opponent win the next round
		"""
		if None not in board._board[index]:
			return False
		c_board = deepcopy(board)
		c_board.play(player.char, index)
		for i in range(0, BOARD_LENGTH):
			if self._is_winning_move(c_board, i, player.opponent):
				return True
		return False

	def __repr__(self) -> str:
		return f"Class SmartOracle()"

