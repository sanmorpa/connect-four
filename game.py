from enum import Enum, auto
from pyfiglet import *
from match import Match
from player import Player, HumanPlayer
from square_board import SquareBoard

class RoundType(Enum):
	NPC_VS_NPC = auto()
	NPC_VS_PC = auto()

class DifficultyLevel(Enum):
	LOW = auto()
	MEDIUM = auto()
	HIGH = auto()

class Game():
	def __init__(self, round_type = RoundType.NPC_VS_NPC, match = Match(Player("Patrisio"), Player("Pinwinasio"))):
		self.round_type = round_type
		self.match = match
		self.board = SquareBoard()

	def start(self):
		self.print_logo()
		self._user_configuration()
		self._start_game()

	def print_logo(self):
		logo = Figlet(font='rounded')
		print(logo.renderText("Connect four"))

	def _user_configuration(self):
		"""
		Asks user for type of match and difficulty level
		"""
		self.round_type = self._get_round_type()
		self.match = self._make_match()

	def _start_game():
		pass

	def _get_round_type(self):
		type = input("""Select a type of round:\n1) Computer vs Computer\n2)Computer vs Human\n>> """)
		while (type != "1" and type != "2"):
			type = input("""Error. It can only be 1 or 2.\n\nSelect a type of round:\n1) Computer vs Computer\n2)Computer vs Human\n>> """)
		if type == "1":
			return RoundType.NPC_VS_NPC
		else:
			return RoundType.NPC_VS_PC

	def _make_match(self):
		player1 = Player("Lil' Robot")
		if self.round_type == RoundType.NPC_VS_PC:
			name = input("What's your name?\n>> ")
			while len(name) == 0:
				name = input("Error, enter a name.\nWhat's your name?\n>> ")
			player2 = HumanPlayer(name)
		else:
			player2 = Player("Big Robot")
		return Match(player1, player2)

	def _has_winner_or_tie(self):
		return self.match.get_winner(self.board)
