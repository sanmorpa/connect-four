from enum import Enum
from inspect import CO_ASYNC_GENERATOR
from syslog import LOG_USER
from square_board import *
from copy import deepcopy
from beautifultable import BeautifulTable
from settings import BOARD_LENGTH
from outils import *

class ColumnClassification(Enum):
	FULL	= -1
	BAD		= 1
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
	def get_recommendations(self, board, player = None):
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
		"""
		It print's the oracle's recommendations for each column
		"""
		rec = [[i.classification.name] for i in self.get_recommendations(board, player)]
		matrix = reverse_matrix(rec)
		bt = BeautifulTable()
		for col in matrix:
			bt.columns.append(col)
		bt.columns.header = [str(i) for i in range(1, BOARD_LENGTH + 1)]
		print(bt)

	def __repr__(self) -> str:
		return f"Class BaseOracle()"

class SmartOracle(BaseOracle):
	def get_recommendations(self, board, player = None):
		"""
		It refines super's calssification and tries to find Win or lose columns
		"""
		recommendation = super().get_recommendations(board, player)
		for i in range (len(recommendation)):
			if recommendation[i].classification == ColumnClassification.MAYBE:
				if self._is_winning_move(board, i, player) == True:
					recommendation[i].classification = ColumnClassification.WIN
				elif self._is_losing_move(board, i, player) == True:
					recommendation[i].classification = ColumnClassification.BAD
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

class MemoizingOracle(SmartOracle):

	def __init__(self):
		self._past_recommendations = {}

	def get_recommendations(self, board, player = None):
		"""
		Overloads method get_recommendations so it's memoized
		"""
		collapsed = collapse_matrix(board._board)
		if collapsed in self._past_recommendations:
			return self._past_recommendations[collapsed]
		recommendation = super().get_recommendations(board, player)
		self._past_recommendations[collapsed] = recommendation
		return recommendation

class LearningOracle(MemoizingOracle):
	def update_to_bad(self, board_code, player, position):
		"""
		It updates a recommendation to bad if it made the player loose last time
		"""
		board = SquareBoard.fromBoardCode(board_code)
		key = collapse_matrix(board)
		recommendation = self.get_recommendations(board, player)
		recommendation[position] = ColumnRecommendation(position, ColumnClassification.BAD)
		self._past_recommendations[key] = recommendation

