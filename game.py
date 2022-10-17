from enum import Enum, auto
from outils import reverse_matrix
from oracle import BaseOracle, LearningOracle, MemoizingOracle, SmartOracle
from move import Move
from pyfiglet import *
from match import Match
from player import Player, HumanPlayer, ReportingPlayer
from settings import BOARD_LENGTH
from square_board import SquareBoard
from beautifultable import BeautifulTable

class RoundType(Enum):
	NPC_VS_NPC = auto()
	NPC_VS_PC = auto()
	PC_VS_PC = auto()

class DifficultyLevel(Enum):
	LOW = auto()
	MEDIUM = auto()
	HIGH = auto()

class Game():
	def __init__(self):
		self.round_type = RoundType.NPC_VS_NPC
		self.match = Match(ReportingPlayer("Little Robot"), ReportingPlayer("Huge Robot"))
		self.difficulty = DifficultyLevel.MEDIUM
		self.board = SquareBoard()

	def start(self):
		"""
		Starts the game
		"""
		self.print_logo()
		while 1:
			self._user_configuration()
			self._game_loop()
			if self._break_loop() == True:
				break
		print("Bye-bye! Thanks for playing!")

	def print_logo(self):
		"""
		Prints the logo of the game
		"""
		logo = Figlet(font='rounded')
		print(logo.renderText("Connect four"))

	def _user_configuration(self):
		"""
		Asks user for type of match and difficulty level
		"""
		self.round_type = self._get_round_type()
		if self.round_type == RoundType.NPC_VS_PC:
			self.difficulty = self._get_difficulty()
		self.match = self._make_match()

	def _game_loop(self):
		"""
		Game loop
		"""
		self.display_board()
		while self._game_over() == False:
			current_player = self.match.next_player
			current_player.play(self.board)
			self.display_move(current_player)
			self.display_board()
		self.display_result()

	def _break_loop(self):
		cont = input("\nAnother round?\n>> ")
		while cont != "yes" and cont != "y"  and cont != "no" and cont != "n":
			cont = input("\nError. please type yes/y or no/n.\nAnother round?\n >> ")
		if cont == "yes" or cont == "y":
			return False
		return True

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
		type = input("Select a type of round:\n1) Computer VS Computer\n2) Computer VS Human\n3) Human VS Human\n>> ")
		while (type != "1" and type != "2" and type != "3"):
			type = input("Error. It can only be 1, 2 or 3.\n\nSelect a type of round:\n1) Computer vs Computer\n2) Computer vs Human\n3) Human VS Human\n>> ")
		if type == "1":
			return RoundType.NPC_VS_NPC
		elif type == "2":
			return RoundType.NPC_VS_PC
		else:
			return RoundType.PC_VS_PC

	def _make_match(self):
		_levels = {DifficultyLevel.LOW: BaseOracle(),
		DifficultyLevel.MEDIUM: MemoizingOracle(),
		DifficultyLevel.HIGH: LearningOracle()
		}
		player1 = self.match._players['x']
		player1.oracle = _levels[self.difficulty]
		if self.round_type == RoundType.NPC_VS_PC:
			name = input("What's your name?\n>> ")
			while len(name) == 0:
				name = input("Error, enter a name.\nWhat's your name?\n>> ")
			player2 = HumanPlayer(name)
		elif self.round_type == RoundType.PC_VS_PC:
			name_1 = input("What's player 1's name?\n>> ")
			while len(name_1) == 0:
				name_1 = input("Error, enter a name.\nWhat's player 1's name?\n>> ")
			player1 = HumanPlayer(name_1)
			name_2 = input("What's player 2's name?\n>> ")
			while len(name_2) == 0:
				name_2 = input("Error, enter a name.\nWhat's player 2's name?\n>> ")
			player2 = HumanPlayer(name_2)
		else:
			player2  = self.match._players['o']
		return Match(player1, player2)

	def _game_over(self):
		return self.match.get_winner(self.board) != None or self.board.is_full()

	def display_move(self, player):
		print(f"\nPlayer {player.name} ({player.char}) has played on column {player.last_move.position + 1}")

	def display_board(self):
		matrix = reverse_matrix(self.board._board)
		bt = BeautifulTable()
		for col in matrix:
			bt.columns.append(col)
		bt.columns.header = [str(i) for i in range(1, BOARD_LENGTH + 1)]
		print(bt)

	def display_result(self):
		winner = self.match.get_winner(self.board)
		if winner:
			print(f"\nThe winner is {winner}!!")
		else:
			print(f"\nA tie between {self.match.get_player('x')} and {self.match.get_player('o')}!!")
