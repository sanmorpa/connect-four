from oracle import *
from square_board import SquareBoard
from player import Player
from settings import BOARD_LENGTH


def test_base_oracle():
	board = SquareBoard.fromList([[None, None, None, None, None],
								['x', 'o', 'x', 'o', 'x' ],
								['o', 'o', 'x', 'x', 'x'],
								['o', None, None, None, None],
								['o', None, None, None, None]])
	expected = [ColumnRecommendation(0, ColumnClassification.MAYBE),
				ColumnRecommendation(1, ColumnClassification.FULL),
				ColumnRecommendation(2, ColumnClassification.FULL),
				ColumnRecommendation(3, ColumnClassification.MAYBE),
				ColumnRecommendation(4, ColumnClassification.MAYBE)]

	rappel = BaseOracle()

	assert len(rappel.get_recommendations(board, None)) == len(expected)
	assert rappel.get_recommendations(board, None) == expected


def test_equality():
	cr = ColumnRecommendation(2, ColumnClassification.MAYBE)

	assert cr == cr
	assert cr == ColumnRecommendation(2, ColumnClassification.MAYBE)
	assert cr != ColumnRecommendation(2, ColumnClassification.FULL)
	assert cr != ColumnRecommendation(3, ColumnClassification.FULL)


def test_is_winning_move():
	winner = Player('Xavier', 'x')
	loser = Player('Otto', 'o')

	empty = SquareBoard()
	almost = SquareBoard.fromList([['o', 'x', 'o', None, None],
									['o', 'x', 'o', None, None],
									['x', None, None, None, None],
									['o', 'x', None, None, None],
									[None, None, None, None, None]])
	oracle = SmartOracle()

	for i in range(0, BOARD_LENGTH):
		assert oracle._is_winning_move(empty, i, winner) == False
		assert oracle._is_winning_move(empty, i, loser) == False
	for i in range(0, BOARD_LENGTH):
		assert oracle._is_winning_move(almost, i, loser) == False

	assert oracle._is_winning_move(almost, 2, winner)


def test_no_good_options():
	x = Player('xavier', char='x')
	o = Player('Otto', char='o', opponent=x)

	oracle = SmartOracle()

	maybe = SquareBoard.fromBoardRawCode('.....|o....|.....|.....|.....')
	bad_and_full = SquareBoard.fromBoardRawCode('x....|ooo..|o....|xoxoo|.....')
	all_bad = SquareBoard.fromBoardRawCode('x....|ooo..|o....|o....|.....')

	assert oracle.no_good_options(maybe, x) == False
	assert oracle.no_good_options(bad_and_full, x)
	assert oracle.no_good_options(all_bad, x)


def test_classification():
	x = Player('xavier', char='x')
	o = Player('Otto', char='o', opponent=x)

	oracle1 = SmartOracle()
	oracle2 = LearningOracle()

	board1 = SquareBoard.fromBoardRawCode('o....|o....|.....|x....|.....')
	expected = [ColumnRecommendation(0, ColumnClassification.LOSE),
				ColumnRecommendation(1, ColumnClassification.LOSE),
		ColumnRecommendation(2, ColumnClassification.MAYBE),
		ColumnRecommendation(3, ColumnClassification.LOSE)]

	assert oracle1.get_recommendations(board1, x) == expected
	assert oracle2.get_recommendations(board1, x) == expected
