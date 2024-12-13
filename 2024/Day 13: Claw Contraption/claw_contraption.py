"""Day 13: Claw Contraption"""


import re
from typing import NamedTuple


class Position(NamedTuple):
    """Position of a button or prize."""
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x - other.x, self.y - other.y)

    def is_zero(self):
        """Return True if the position is at the origin."""
        return self.x == 0 and self.y == 0


def parse(filename):
    """Parse the input file and return a list of claw machine
    configurations.
    """
    claw_machines = []
    claw_machine = {}
    button_pattern = re.compile(r'Button (A|B): X\+(\d+), Y\+(\d+)')
    prize_pattern = re.compile(r'Prize: X=(\d+), Y=(\d+)')

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == '':
                claw_machines.append(claw_machine)
                claw_machine = {}
                continue

            if m := button_pattern.match(line):
                button, x, y = m.groups()
                claw_machine[button] = Position(int(x), int(y))
            elif m := prize_pattern.match(line):
                x, y = m.groups()
                claw_machine['P'] = Position(int(x), int(y))

    if claw_machine:
        claw_machines.append(claw_machine)

    return claw_machines


def find_cost(claw_machine, max_pressed=100):
    """Find the fewest of tokens to to spend to win the prize."""
    move_a = claw_machine['A']
    move_b = claw_machine['B']
    pos = claw_machine['P']
    queue = [(pos, 0, 0, 0)]
    visited = set()

    while queue:
        target, press_a, press_b, tokens = queue.pop()
        if target.is_zero():
            return tokens

        if target in visited:
            continue

        visited.add(target)

        if (
            target.x < 0
            or target.y < 0
            or press_a > max_pressed
            or press_b > max_pressed
        ):
            continue

        queue.extend((
            (target - move_a, press_a + 1, press_b, tokens + 3),
            (target - move_b, press_a, press_b + 1, tokens + 1)
        ))

    return None


def compute_cost(claw_machine):
    """Compute the number of tokens to spend to win the prize."""
    a1, a2 = claw_machine['A']
    b1, b2 = claw_machine['B']
    c1, c2 = claw_machine['P']

    a_numerator = b2 * c1 - b1 * c2
    a_denominator = a1 * b2 - a2 * b1
    if a_numerator % a_denominator != 0:
        return None

    b_numerator = c2 * a1 - c1 * a2
    b_denominator = a1 * b2 - a2 * b1
    if b_numerator % b_denominator != 0:
        return None

    a, b = a_numerator // a_denominator, b_numerator // b_denominator
    return 3 * a + b


def test_eample():
    """Test the example."""
    claw_machines = parse('example.txt')
    assert sum(
        tokens
        for claw_machine in claw_machines
        if (tokens := find_cost(claw_machine)) is not None
    ) == 480


def test_puzzle():
    """Test the puzzle."""
    claw_machines = parse('input.txt')
    assert sum(
        tokens
        for claw_machine in claw_machines
        if (tokens := find_cost(claw_machine)) is not None
    ) == 29201

    claw_machines = (
        {**claw_machine, 'P': claw_machine['P'] + Position(10**13, 10**13)}
        for claw_machine in claw_machines
    )
    assert sum(
        tokens
        for claw_machine in claw_machines
        if (tokens := compute_cost(claw_machine)) is not None
    ) == 104140871044942
