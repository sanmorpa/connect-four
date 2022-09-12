from linear_board import *

class SquareBoard():
	"""
	A square board of BOARD_LENGTH X BOARD_LENGTH
	"""
	@classmethod
	def fromList(cls, list_of_lists):
		"""
		It allows us to instance a SquareBoard from a pre-configured list
		"""
		if len(list_of_lists) != BOARD_LENGTH:
			raise ValueError
		for item in list_of_lists:
			if len(item) != BOARD_LENGTH:
				raise ValueError
		board = cls()
		board._board = list_of_lists
		return board

	def __init__(self):
		"""
		A list of None-filled lists
		"""
		self._board = [[None for i in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]

	def is_full(self):
		"""
		True if all LinearBoards are full
		"""
		for column in self._board:
			if None not in column:
				return True
		return False

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
			if find_streak(column, char, VICTORY_STRIKE) == True:
				return True
		return False
	
	def _horizontal_victory(self, char):
		"""
		True if there's a horizontal victory of char
		"""
		transp = transpose(self._board)
		tmp = SquareBoard.fromList(transp)
		return tmp._vertical_victory(char)

	def _rise_victory(self, char):
		"""
		True if there's a rising diagonal victory of char
		"""
		reversed = reverse_matrix(self._board)
		tmp = SquareBoard.fromList(reversed)
		return tmp._sink_victory(char)

	def _sink_victory(self, char):
		"""
		True if there's a sinking diagonal victory of char
		"""
		displaced = displace_matrix(self._board)
		tmp = SquareBoard.fromList(displaced)
		return tmp._horizontal_victory(char)

	# dunders
	def __repr__(self):
		return f"{self.__class__}:{self._board}"
	
	def __len__(self):
		return len(self._board)