"""Day 4: Giant Squid"""


import os
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property


INPUT = os.path.join(os.path.dirname(__file__), 'input')


@contextmanager
def parse_input(filename):
    """Parse bingo input.

    The first line of the input is draw numbers followed by a blank line.
    The remaining lines are a set of boards. Each board is separated by
    a blank line.
    """
    with open(filename, encoding='utf-8') as input_file:
        try:
            line = next(input_file)
        except StopIteration:
            numbers = []
            boards = iter([])
        else:
            numbers = line.rstrip().split(',')
            boards = _iter_boards(input_file)

        yield numbers, boards


def _iter_boards(input_file):
    for line in input_file:
        if not (line := line.rstrip()):
            continue

        board = [line.split()]
        for board_line in input_file:
            if not (board_line := board_line.rstrip()):
                break

            board.append(board_line.split())

        yield Board(board)


@dataclass
class Cell:
    """A cell of Bingo board"""

    number: str
    marked: bool = False


class Board:
    """A Bingo board"""

    def __init__(self, data):
        self.last_draw = None
        self.numbers = {}
        self.board = {}

        for i, row in enumerate(data):
            for j, number in enumerate(row):
                self.numbers[number] = (i, j)
                self.board[i, j] = Cell(number)

    def __str__(self):
        width = max(len(number) for number in self.numbers) + 1
        rows, cols = self.shape

        return '\n'.join(
            ''.join(
                self._format_cell(self.board[row, col], width)
                for col in range(cols)
            )
            for row in range(rows)
        )

    @staticmethod
    def _format_cell(cell, width):
        number = f'{cell.number:>{width}}'
        if cell.marked:
            return f'\033[92m\033[1m{number}\033[0m'
        return number

    @cached_property
    def shape(self):
        rows, cols = max(self.board)
        return rows + 1, cols + 1

    def draw(self, number):
        self.last_draw = number
        try:
            position = self.numbers[number]
        except KeyError:
            # The number is not on the board
            pass
        else:
            self.board[position].marked = True

    @property
    def bingo(self):
        return self._is_row_complete() or self._is_col_complete()

    def _is_row_complete(self):
        rows, cols = self.shape
        for row in range(rows):
            if all(self.board[row, col].marked for col in range(cols)):
                return True

        return False

    def _is_col_complete(self):
        rows, cols = self.shape
        for col in range(cols):
            if all(self.board[row, col].marked for row in range(rows)):
                return True

        return False

    @property
    def score(self):
        return int(self.last_draw) * sum(
            int(cell.number)
            for cell in self.board.values()
            if not cell.marked
        )


class Game1:

    @classmethod
    def play(cls, numbers, boards):
        if winning_board := cls._play(numbers, list(boards)):
            return winning_board

        raise RuntimeError('No winning board found.')

    @staticmethod
    def _play(numbers, boards):
        for number in numbers:
            for board in boards:
                board.draw(number)
                if board.bingo:
                    return board

        return None


class Game2(Game1):

    @staticmethod
    def _play(numbers, boards):
        for number in numbers:
            remaining_boards = []
            for board in boards:
                board.draw(number)
                if board.bingo:
                    is_last_board = len(boards) == 1
                    if is_last_board:
                        return board
                else:
                    remaining_boards.append(board)

            boards = remaining_boards

        return None


def test_part1():
    with parse_input(INPUT) as data:
        winning_board = Game1.play(*data)
        print()
        print(winning_board)
        assert winning_board.score == 82440


def test_part2():
    with parse_input(INPUT) as data:
        winning_board = Game2.play(*data)
        print()
        print(winning_board)
        assert winning_board.score == 20774
