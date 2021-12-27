"""Day 23: Amphipod"""


import math
from heapq import heappush, heappop
from pathlib import Path


PATH = Path(__file__).parent

# The width of the Amphipod diagram
WIDTH = 13


class Burrow:

    amphipods = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }
    rooms = {
        'A': {29, 42},
        'B': {31, 44},
        'C': {33, 46},
        'D': {35, 48},
    }
    hallway = {14, 15, 17, 19, 21, 23, 24}
    outside_room = {16, 18, 20, 22}

    def __init__(self, diagram, energy=0, hueristic=0):
        self.diagram = diagram
        self.energy = energy
        self.hueristic = hueristic

    def __repr__(self):
        return f'Energy: {self.energy}\n' + ''.join(
            f'{char}\n' if index % WIDTH == 0 else char
            for index, char in enumerate(self.diagram, start=1)
        )

    def __hash__(self):
        return hash(self.diagram)

    def __eq__(self, other):
        return self.diagram == other.diagram

    def __lt__(self, other):
        return self.energy < other.energy

    def __iter__(self):
        length = len(self.diagram)
        for pos, char in enumerate(self.diagram):
            if char not in self.amphipods or self._is_correct_room(char, pos):
                continue

            for steps in range(-length, length + 1):
                new_pos = pos + steps
                if (not self._is_valid_space(new_pos)
                        or self._is_immediate_outside_room(new_pos)
                        or not self._is_valid_move(char, pos, new_pos)):
                    continue

                steps = self._get_steps(pos, new_pos)
                if steps == math.inf:
                    continue

                cost = steps * self.amphipods[char]
                energy = self.energy + cost
                hueristic = self.hueristic
                if new_pos not in self.rooms[char]:
                    hueristic += cost

                yield type(self)(
                    self._move(char, pos, new_pos), energy, hueristic
                )

    def _move(self, amphipod, pos, new_pos):
        diagram = (
            f'{self.diagram[:new_pos]}{amphipod}'
            f'{self.diagram[new_pos + 1:]}'
        )
        return f'{diagram[:pos]}.{diagram[pos + 1:]}'

    def _is_valid_space(self, pos):
        if pos < 0:
            return False

        try:
            return self.diagram[pos] == '.'
        except IndexError:
            return False

    def _is_correct_room(self, amphipod, pos):
        valid_rooms = self.rooms[amphipod]
        return (
            pos == max(valid_rooms)
            or pos in valid_rooms
            and all(
                self.diagram[room] == amphipod
                for room in valid_rooms
                if room > pos
            )
        )

    def _is_immediate_outside_room(self, pos):
        return pos in self.outside_room

    def _is_valid_move(self, amphipod, pos, new_pos):
        if self._is_correct_room(amphipod, new_pos):
            return True

        if pos not in self.hallway:
            return new_pos in self.hallway

        return False

    def _get_steps(self, pos, new_pos):
        visited = set()

        def get_steps(pos, new_pos, steps):
            if pos == new_pos:
                return steps

            if pos in visited or not self._is_valid_space(pos):
                return math.inf

            visited.add(pos)

            return min(
                get_steps(pos + adj, new_pos, steps + 1)
                for adj in (-WIDTH, -1, 1, WIDTH)
            )

        return min(
            get_steps(pos + adj, new_pos, 1)
            for adj in (-WIDTH, -1, 1, WIDTH)
        )


class Burrow2(Burrow):

    rooms = {
        'A': {29, 42, 55, 68},
        'B': {31, 44, 57, 70},
        'C': {33, 46, 59, 72},
        'D': {35, 48, 61, 74},
    }


class Amphipod:

    def __init__(self, burrow, goal):
        self._burrow = burrow
        self._goal = goal
        self._trail = {}

    def __repr__(self):
        trail = []
        burrow = self._goal
        while burrow != self._burrow:
            trail.append(burrow)
            burrow = self._trail[burrow]
        trail.append(self._burrow)

        return '\n'.join(str(burrow) for burrow in reversed(trail))

    def organize(self):
        visited = set()
        queue = [(0, self._burrow)]
        energies = {self._burrow: 0}
        self._trail.clear()
        while queue:
            _, burrow = heappop(queue)
            if burrow == self._goal:
                self._goal = burrow
                return energies[burrow]

            if burrow in visited:
                continue

            visited.add(burrow)
            for next_burrow in burrow:
                energy = next_burrow.energy
                if energy < energies.get(next_burrow, math.inf):
                    energies[next_burrow] = energy
                    self._trail[next_burrow] = burrow
                heappush(queue, (next_burrow.hueristic, next_burrow))

        return math.inf


def parse(path):
    with path.open(encoding='utf-8') as input_file:
        return ''.join(
            line.rstrip().ljust(WIDTH)
            for line in input_file
        )


def test_example1():
    goal = Burrow(
        '#############'
        '#...........#'
        '###A#B#C#D###'
        '  #A#B#C#D#  '
        '  #########  '
    )
    burrow = Burrow(parse(PATH / 'example1'))
    assert Amphipod(burrow, goal).organize() == 12521


def test_example2():
    goal = Burrow2(
        '#############'
        '#...........#'
        '###A#B#C#D###'
        '  #A#B#C#D#  '
        '  #A#B#C#D#  '
        '  #A#B#C#D#  '
        '  #########  '
    )
    burrow = Burrow2(parse(PATH / 'example2'))
    assert Amphipod(burrow, goal).organize() == 44169


def test_part1():
    goal = Burrow(
        '#############'
        '#...........#'
        '###A#B#C#D###'
        '  #A#B#C#D#  '
        '  #########  '
    )
    burrow = Burrow(parse(PATH / 'input1'))
    assert Amphipod(burrow, goal).organize() == 15299


def test_part2():
    goal = Burrow2(
        '#############'
        '#...........#'
        '###A#B#C#D###'
        '  #A#B#C#D#  '
        '  #A#B#C#D#  '
        '  #A#B#C#D#  '
        '  #########  '
    )
    burrow = Burrow2(parse(PATH / 'input2'))
    assert Amphipod(burrow, goal).organize() == 47193
