from linear_board import *

class SquareBoard():
	"""
	A square board of BOARD_LENGTH X BOARD_LENGTH
	"""
	@classmethod
	def fromList(cls, list_of_lists):
		"""
		It transform a list of lists to a LinearBoard
		"""
		board = cls()
		board._board = list(map(lambda element: LinearBoard.fromList(element), list_of_lists))

	def __init__(self):
		self._board = [LinearBoard() for i in range(BOARD_LENGTH)]

	def is_full(self):
		"""
		True if all LinearBoards are full
		"""
		for column in self._board:
			if None in column:
				return False
		return True

	def is_victory(self, char):
		"""
		True if there is any victory either vertical, horizontal or diagonal
		"""
		return self._vertical_victory(char) or self._horizontal_victory(char) or self._rise_victory(char) or self._sink_victory(char)
	
	def _vertical_victory(self, char):
		"""
		True if there's a vertical victory of char
		"""
		for column in self._board:
			if column.is_victory(char):
				return True
		return False
	
	def _horizontal_victory(self, char):
		pass

	def _rise_victory(self, char):
		pass

	def _sink_victory(self, char):
		pass

	# dunders
	def __repr__(self):
		return f"{self.__class__}:{self._board}"