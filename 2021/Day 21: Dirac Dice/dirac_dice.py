"""Day 21: Dirac Dice"""


from functools import cache
from itertools import cycle, product
from pathlib import Path


PATH = Path(__file__).parent


class Dice:

    def __init__(self, position1, position2):
        self._pos1 = position1
        self._pos2 = position2

    def play(self):
        return self._play(self._pos1, self._pos2)

    @staticmethod
    def move(position, roll):
        return 1 + (position + roll - 1) % 10

    def _play(self, pos1, pos2, score1=0, score2=0):
        raise NotImplementedError


class DeterministicDice(Dice):

    win_points = 1000

    @staticmethod
    def rolls():
        roll = cycle(range(1, 101))
        while True:
            yield sum(next(roll, 0) for _ in range(3))

    def _play(self, pos1, pos2, score1=0, score2=0):
        rolls = self.rolls()
        count = 0

        for p1_roll, p2_roll in zip(rolls, rolls):
            pos1 = self.move(pos1, p1_roll)
            score1 += pos1
            count += 3
            if score1 >= self.win_points:
                break

            pos2 = self.move(pos2, p2_roll)
            score2 += pos2
            count += 3
            if score2 >= self.win_points:
                break

        return count * min(score1, score2)


class DiracDice(Dice):

    win_points = 21

    @staticmethod
    def rolls():
        return (sum(rolls) for rolls in product((1, 2, 3), repeat=3))

    @cache
    def _play(self, pos1, pos2, score1=0, score2=0):
        if score1 >= self.win_points:
            return 1, 0

        if score2 >= self.win_points:
            return 0, 1

        p1_wins = p2_wins = 0
        for p1_roll in self.rolls():
            new_pos1 = self.move(pos1, p1_roll)
            new_score1 = score1 + new_pos1
            if new_score1 >= self.win_points:
                p1_wins += 1
                continue

            for p2_roll in self.rolls():
                new_pos2 = self.move(pos2, p2_roll)
                new_score2 = score2 + new_pos2
                _p1_wins, _p2_wins = self._play(
                    new_pos1, new_pos2, new_score1, new_score2
                )
                p1_wins += _p1_wins
                p2_wins += _p2_wins

        return p1_wins, p2_wins


def parse(path):
    with path.open(encoding='utf-8') as input_file:
        positions = []
        for line in input_file:
            _, position = line.split(':')
            positions.append(int(position))

        return positions


def test_example1():
    number = DeterministicDice(*parse(PATH / 'example')).play()
    assert number == 739785


def test_example2():
    wins = DiracDice(*parse(PATH / 'example')).play()
    assert max(wins) == 444356092776315


def test_part1():
    number = DeterministicDice(*parse(PATH / 'input')).play()
    assert number == 998088


def test_part2():
    wins = DiracDice(*parse(PATH / 'input')).play()
    assert max(wins) == 306621346123766
