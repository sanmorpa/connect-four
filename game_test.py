from game import Game
from square_board import SquareBoard


def test_created_with_defaults():
	game = Game()
	assert game.round_type != None
	assert game.match != None
	assert game.board != None
	assert game.board.is_full() == False

def test_is_game_over():
	game = Game()
	win_x = SquareBoard.fromList([['x', 'o', None, None, None],
								['x', 'x', None, None, None],
								['x', 'o', 'x', 'o', None],
								['x', 'o', None, None, None],
								['x', 'o', None, None, None]])

	win_o = SquareBoard.fromList([['x', 'o', 'x', 'o', None],
								['o', 'x', 'o', None, None],
								['o', 'o', None, None, None],
								['o', 'x', None, None, None],
								['o', 'x', None, None, None]])

	tie = SquareBoard.fromList([['o', 'x', 'x', 'o', 'o'],
								['x', 'o', 'o', 'x', 'o'],
								['o', 'x', 'x', 'o', 'o'],
								['x', 'o', 'o', 'x', 'x'],
								['x', 'x', 'o', 'x', 'x']])

	unfinished = SquareBoard.fromList([['o', 'x', 'x', 'o', None],
									[None, None, None, None, None],
									[None, None, None, None, None],
									[None, None, None, None, None],
									[None, None, None, None, None]])

	game.board = win_x
	assert game._game_over() == True

	game.board = win_o
	assert game._game_over() == True

	game.board = tie
	assert game._game_over() == True

	game.board = unfinished
	assert game._game_over() == False
