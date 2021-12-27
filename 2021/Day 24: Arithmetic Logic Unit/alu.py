"""Day 24: Arithmetic Logic Unit"""


from collections import namedtuple
from functools import cache
from pathlib import Path


PATH = Path(__file__).parent

Vars = namedtuple('Vars', ['w', 'x', 'y', 'z'])

# Number of instruction lines per digit
NUM_INST_PER_DIGIT = 18
# Z stores base-26 numbers
Z_BASE = 26
# Model numbers are fourteen-digit numbers
TOTAL_DIGITS = 14


class ModelFinder:

    def __init__(self, instructions):
        self.instructions = instructions

    def find_largest(self):
        return self._find(
            index=0,
            vars_=Vars(0, 0, 0, 0),
            digits=list(range(9, 0, -1)),
        )

    def find_smallest(self):
        return self._find(
            index=0,
            vars_=Vars(0, 0, 0, 0),
            digits=list(range(1, 10)),
        )

    def _find(self, index, vars_, digits):
        @cache
        def _do_find(index, vars_):
            # Constraint from analyzing inputs
            if ((level := index // NUM_INST_PER_DIGIT) < TOTAL_DIGITS // 2
                    and vars_.z > Z_BASE ** (level + 1)
                    or level >= TOTAL_DIGITS // 2
                    and vars_.z > Z_BASE ** (TOTAL_DIGITS - level)):
                return None

            if index >= len(self.instructions):
                return '' if vars_.z == 0 else None

            code, *operands = self.instructions[index]
            if code == 'inp':
                for digit in digits:
                    values = {operands[0]: digit}
                    result = _do_find(index + 1, vars_._replace(**values))
                    if result is not None:
                        return f'{digit}{result}'
                return None

            var1, var2 = operands
            val1 = getattr(vars_, var1)
            val2 = var2 if isinstance(var2, int) else getattr(vars_, var2)
            if code == 'add':
                values = {var1: val1 + val2}
            elif code == 'mul':
                values = {var1: val1 * val2}
            elif code == 'div':
                values = {var1: val1 // val2}
            elif code == 'mod':
                values = {var1: val1 % val2}
            elif code == 'eql':
                values = {var1: int(val1 == val2)}
            else:
                raise ValueError(
                    f'Invalid instruction: {self.instructions[index]}'
                )

            return _do_find(index + 1, vars_._replace(**values))

        return _do_find(index, vars_)


def parse(path):
    with path.open(encoding='utf-8') as input_file:
        for line in input_file:
            if not line.strip():
                return

            code, variable, *operands = line.split()
            if operands:
                try:
                    operand = int(operands[0])
                except ValueError:
                    operand = operands[0]
                yield code, variable, operand
            else:
                yield code, variable


def test_part1():
    finder = ModelFinder(list(parse(PATH / 'input')))
    assert finder.find_largest() == '99893999291967'


def test_part2():
    finder = ModelFinder(list(parse(PATH / 'input')))
    assert finder.find_smallest() == '34171911181211'
