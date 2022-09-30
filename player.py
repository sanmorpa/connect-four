from settings import *
from oracle import *
from random import *

class Player():
	def __init__(self, name, char = None, opponent = None, oracle = SmartOracle()):
		self.name = name
		self.char = char
		self.oracle = oracle
		self.opponent = opponent
		self.last_move = None

	@property
	def opponent(self):
		return self._opponent

	@opponent.setter
	def opponent(self, newValue):
		if newValue != None:
			self._opponent = newValue
			newValue._opponent = self

	def play(self, board):
		'''
		The player plays in a position recommended by the oracle
		'''
		(recommendation, best) = self._ask_oracle(board)
		self._play_on(board, best)

	def _play_on(self, board, best):
		'''
		It allows the player to play on the best column
		'''
		board.play(self.char, best)
		self.last_move = best

	def _choose(self, recommendations):
		'''
		Gives the best position to play according to what the oracle recommends
		'''
		valid = [i for i in recommendations if i.classification.value != -1]
		valid = sorted(valid, key=lambda x: x.classification.value, reverse = True)
		if all_same(valid):
			return (choice(valid).index)
		return (valid[0].index)

	def _ask_oracle(self, board):
		'''
		It asks the oracle for all predictions and the best one
		'''
		recommendations = self.oracle.get_recommendation(board, self)
		best = self._choose(recommendations)
		return (recommendations, best)

	def __repr__(self):
		return f"Class Player({self.name}, {self.char}, {self.oracle})"
	def __str__(self) -> str:
		return f"Robot player '{self.name}' with icon '{self.char}'"

class HumanPlayer(Player):
	def __init__(self, name, char = None):
		super().__init__(name, char)

	def _ask_oracle(self, board):
		'''
		Operator Overloading of _ask_oracle to change the oracle to the human's input
		'''
		user_input = input(f"Where do you want to play {self.name}? (to ask the oracle type 'h' or 'help')\n>> ")
		while 1:
			if _is_int(user_input) and _is_within_column_range(board, int(user_input)) and _is_non_full_column(board, int(user_input)):
				return (self.oracle.get_recommendation(board, self), int(user_input))
			elif user_input == 'h' or user_input == 'help':
				rec = self.oracle.get_recommendation(board, self)
				for i in rec:
					print(f"For column with index {i.index} the oracle says: {i.classification.name}")
			else:
				print("Error, invalid input. Please enter the index of the column in digits. if you want a recommendation, insert 'h' or 'help")
			user_input = input(f"Where do you want to play {self.name}? (to ask the oracle type 'h' or 'help')\n>> ")

	def __repr__(self):
		return f"Class HumanPlayer({self.name}, {self.char}, {self.opponent} , {self.oracle})"
	def __str__(self) -> str:
		return f"Player '{self.name}' with icon '{self.char}'"

def	_is_non_full_column(board, num):
	'''
	Checks if the user's input is well within range of our parameters and a possible play
	'''
	if  _is_within_column_range(board, num) == False or _is_int(num) == False:
		return False
	return None in board._board[num]

def _is_within_column_range(board, num):
	'''
	Checks if the user's input is within range of our board
	'''
	return num >= 0 and num < len(board._board)

def _is_int(num):
	'''
	Checks if the user's input is indeed an integer
	'''
	try:
		int(num)
		return True
	except:
		return False


