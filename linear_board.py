from settings import BOARD_LENGTH, VICTORY_STRIKE
from list_outils import *

class LinearBoard():
	"""
	Class tht represents a board of just one column
	x is a player's tile
	o is another player's tile
	None is an empty space
	"""

	def __init__(self):
		"""
		A list of None
		"""
		self._column = [None for i in range(BOARD_LENGTH)] #_ means it's a private attribute
	
	def add(self, char):
		"""
		It puts a tile in the first available position
		"""
		if not self.is_full():
			i = self._column.index(None)
			self._column[i] = char
		else:
			print("Error, this line is full already")

	def is_full(self):
		"""
		It checks if a line is full
		"""
		return None not in self._column

	def is_victory(self, char):
		"""
		It checks if a player has won
		"""
		return find_streak(self._column, char, 3)

	def is_tie(self, char1, char2):
		"""
		It checks if there is a tie between players: No victory of player1 nor player2 
		"""
		return (self.is_full() == True and self.is_victory(char1) == False and self.is_victory(char2) == False)