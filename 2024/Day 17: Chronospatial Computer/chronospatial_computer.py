"""Day 17: Chronospatial Computer"""


import re
from typing import NamedTuple


class Instruction:
    """The Chronospatial Computer instructions."""

    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class Computer(NamedTuple):
    """The Chronospatial Computer."""

    registers: dict[str, int]
    program: list[int]

    def run(self):
        """Run the program and return the output."""
        output = []
        pointer = 0

        while pointer < len(self.program) - 1:
            opcode, operand = self.program[pointer], self.program[pointer + 1]
            match opcode:
                case Instruction.ADV:
                    self.registers['A'] = self._dv(operand)
                case Instruction.BXL:
                    self.registers['B'] ^= operand
                case Instruction.BST:
                    self.registers['B'] = self._combo(operand) % 8
                case Instruction.JNZ if self.registers['A'] != 0:
                    pointer = operand
                    continue
                case Instruction.BXC:
                    self.registers['B'] ^= self.registers['C']
                case Instruction.OUT:
                    output.append(self._combo(operand) % 8)
                case Instruction.BDV:
                    self.registers['B'] = self._dv(operand)
                case Instruction.CDV:
                    self.registers['C'] = self._dv(operand)

            pointer += 2

        return output

    def _dv(self, operand):
        numerator = self.registers['A']
        denominator = 2 ** self._combo(operand)
        return numerator // denominator

    def _combo(self, operand):
        match operand:
            case 4:
                return self.registers['A']
            case 5:
                return self.registers['B']
            case 6:
                return self.registers['C']
            case _:
                return operand


def parse(filename):
    """Parse the input file and return a Computer instance."""
    with open(filename, 'r', encoding='utf-8') as f:
        top, bottom = f.read().strip().split('\n\n')
        registers = {
            m.group(1): int(m.group(2))
            for line in top.splitlines()
            if (m := re.match(r'Register ([A-C]): (\d+)', line))
        }
        program = [int(n) for n in bottom.split(':')[1].split(',')]

    return Computer(registers, program)


def search_initial_value(computer):
    """Search for the lowest initial value of register A that causes the
    program to output a copy of itself.
    """
    def _search(pos, a=0):
        if pos < 0:
            return a

        for i in range(8):
            value = a + i * 8**pos
            computer.registers['A'] = value
            out = computer.run()
            try:
                n = out[pos]
            except IndexError:
                continue

            if n != computer.program[pos]:
                continue

            if value := _search(pos - 1, value):
                return value

        return None

    return _search(len(computer.program) - 1)


def test_example():
    """Test the example."""
    computer = parse('example1.txt')
    output = computer.run()
    assert ','.join(map(str, output)) == '4,6,3,5,6,3,5,2,1,0'

    computer = parse('example2.txt')
    assert search_initial_value(computer) == 117440


def test_puzzle():
    """Test the puzzle."""
    computer = parse('input.txt')
    output = computer.run()
    assert ','.join(map(str, output)) == '6,4,6,0,4,5,7,2,7'
    assert search_initial_value(computer) == 164541160582845
