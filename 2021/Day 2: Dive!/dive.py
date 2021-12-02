"""Day 2: Dive!"""


import os


INPUT = os.path.join(os.path.dirname(__file__), 'input')


class Submarine1:

    def __init__(self, horizontal=0, depth=0):
        self.horizontal = horizontal
        self.depth = depth

    @property
    def multiplication(self):
        return self.horizontal * self.depth

    def forward(self, number):
        self.horizontal += number

    def down(self, number):
        self.depth += number

    def up(self, number):
        self.depth -= number

    def dive(self, instructions):
        for direction, number in self._read_commands(instructions):
            getattr(self, direction)(number)

    @staticmethod
    def _read_commands(instructions):
        with open(instructions, encoding='utf-8') as input_file:
            for line in input_file:
                direction, number = line.split()
                yield direction.strip(), int(number)


class Submarine2(Submarine1):

    def __init__(self, horizontal=0, depth=0, aim=0):
        super().__init__(horizontal=horizontal, depth=depth)
        self.aim = aim

    def forward(self, number):
        self.horizontal += number
        self.depth += self.aim * number

    def down(self, number):
        self.aim += number

    def up(self, number):
        self.aim -= number


def test_part1():
    submarine = Submarine1()
    submarine.dive(INPUT)
    assert submarine.multiplication == 1692075


def test_part2():
    submarine = Submarine2()
    submarine.dive(INPUT)
    assert submarine.multiplication == 1749524700
