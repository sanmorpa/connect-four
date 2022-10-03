from enum import Enum, auto
from list_outils import reverse_matrix
from pyfiglet import *
from match import Match
from player import Player, HumanPlayer
from settings import BOARD_LENGTH
from square_board import SquareBoard
from beautifultable import BeautifulTable

class RoundType(Enum):
	NPC_VS_NPC = auto()
	NPC_VS_PC = auto()

class DifficultyLevel(Enum):
	LOW = auto()
	MEDIUM = auto()
	HIGH = auto()

class Game():
	def __init__(self):
		self.round_type = RoundType.NPC_VS_NPC
		self.match = Match(Player("Little Robot"), Player("Huge Robot"))
		self.difficulty = DifficultyLevel.MEDIUM
		self.board = SquareBoard()

	def start(self):
		self.print_logo()
		self._user_configuration()
		self._start_game_loop()

	def print_logo(self):
		logo = Figlet(font='rounded')
		print(logo.renderText("Connect four"))

	def _user_configuration(self):
		"""
		Asks user for type of match and difficulty level
		"""
		self.round_type = self._get_round_type()
		self.difficulty = self._get_difficulty()
		self.match = self._make_match()

	def _start_game():
		pass

	def _start_game_loop(self):
		while self._game_over() == False:
			current_player = self.match.next_player
			current_player.play(self.board)
			self.display_move(current_player)
			self.display_board()
		self.display_result()

	def _get_difficulty(self):
		type = input("Select a difficulty:\n1) LOW\n2) MEDIUM\n3) HIGH\n>> ")
		while (type != "1" and type != "2" and type != "3"):
			type = input("Error. It can only be 1, 2 or 3.\n\nSelect a difficulty:\n1) LOW\n2) MEDIUM\n3) HIGH\n>> ")
		if type == "1":
			return DifficultyLevel.LOW
		elif type == "2":
			return DifficultyLevel.MEDIUM
		else:
			return DifficultyLevel.HIGH

	def _get_round_type(self):
		type = input("Select a type of round:\n1) Computer vs Computer\n2) Computer vs Human\n>> ")
		while (type != "1" and type != "2"):
			type = input("Error. It can only be 1 or 2.\n\nSelect a type of round:\n1) Computer vs Computer\n2) Computer vs Human\n>> ")
		if type == "1":
			return RoundType.NPC_VS_NPC
		else:
			return RoundType.NPC_VS_PC

	def _make_match(self):
		player1 = self.match._players['x']
		if self.round_type == RoundType.NPC_VS_PC:
			name = input("What's your name?\n>> ")
			while len(name) == 0:
				name = input("Error, enter a name.\nWhat's your name?\n>> ")
			player2 = HumanPlayer(name)
		else:
			player2  = self.match._players['o']
		return Match(player1, player2)

	def _game_over(self):
		return self.match.get_winner(self.board) != None or self.board.is_full()

	def display_move(self, player):
		print(f"\nPlayer {player.name} ({player.char}) has played on column {player.last_move}")

	def display_board(self):
		matrix = reverse_matrix(self.board._board)
		bt = BeautifulTable()
		for col in matrix:
			bt.columns.append(col)
		bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]
		print(bt)

	def display_result(self):
		winner = self.match.get_winner(self.board)
		if winner:
			print(f"\nThe winner is {winner}!!")
		else:
			print(f"\nA tie between {self.match.get_player('x')} and {self.match.get_player('o')}!!")
