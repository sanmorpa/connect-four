class Player():
	def __init__(self, name, char, oracle):
		self.name = name
		self.char = char
		self.oracle = oracle

	def play(self, board):
		'''
		The player plays in a position recommended by the oracle
		'''
		board.play(self.char, self._choose(board))

	def _choose(self, board):
		'''
		Gives the best position to play according to what the oracle says
		'''
		recommendation = self.oracle.get_recommendation(board)
		for i in range(len(recommendation)):
			if recommendation[i].classification.value == 0:
				return i

