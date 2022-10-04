from settings import *
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

	@classmethod
	def fromBoardCode(cls, board_code):
		"""
		It allows us to instance a SquareBoard from a BoardCode class
		"""
		return cls.fromBoardRawCode(board_code._raw_code)

	@classmethod
	def fromBoardRawCode(cls, raw_code):
		"""
		Creates a instance of SquareBoard from the raw string of the BoardCode class
		"""
		lst = []
		i = 0
		while i < len(raw_code):
			aux_lst = []
			while i < len(raw_code) and raw_code[i] != "|":
				if raw_code[i] == ".":
					aux_lst.append(None)
				else:
					aux_lst.append(raw_code[i])
				i += 1
			lst.append(aux_lst)
			if i < len(raw_code):
				i += 1
		return cls.fromList(lst)

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
			if None in column:
				return False
		return True

	def play(self, char, col):
		if None in self._board[col]:
			self._board[col][self._board[col].index(None)] = char
		else:
			print(f"Error, column {col} is full")

	def as_code(self):
		return BoardCode(self)

	def is_tie(self, char1, char2):
		return self.is_full() and not self.is_victory(char1) and not self.is_victory(char2)

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

	def __repr__(self):
		return f"{self.__class__}:{self._board}"

	def __len__(self):
		return len(self._board)

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self._board == other._board

	def __hash__(self) -> int:
		return hash((self._board))

class BoardCode:
	def __init__(self, board):
		self._raw_code = collapse_matrix(board._board)

	@property
	def raw_code(self):
		return self._raw_code

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False
		return self._raw_code == other._raw_code

	def __hash__(self) -> int:
		return hash((self._raw_code))

	def __repr__(self):
		return f"BoardCode({self._raw_code})"
