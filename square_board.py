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
		return board

	def __init__(self):
		self._board = [LinearBoard() for i in range(BOARD_LENGTH)]

	def is_full(self):
		"""
		True if all LinearBoards are full
		"""
		for column in self._board:
			if column.is_full() == False:
				return False
		return True
	
	def as_matrix(self):
		"""
		Returns a list of lists of the board
		"""
		return list(map(lambda x: x._column, self._board))

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
			if column.is_victory(char) == True:
				return True
		return False
	
	def _horizontal_victory(self, char):
		"""
		True if there's a horizontal victory of char
		"""
		transp = transpose(self.as_matrix())
		tmp = SquareBoard.fromList(transp)
		return tmp._vertical_victory(char)

	def _rise_victory(self, char):
		"""
		True if there's a rising diagonal victory of char
		"""
		return False

	def _sink_victory(self, char):
		"""
		True if there's a sinking diagonal victory of char
		"""
		displaced = displace_matrix(self.as_matrix())
		tmp = SquareBoard.fromList(displaced)
		return tmp._horizontal_victory(char)

	# dunders
	def __repr__(self):
		return f"{self.__class__}:{self._board}"