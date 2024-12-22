"""Day 21: Keypad Conundrum"""


import math
from functools import cached_property, lru_cache
from collections import defaultdict
from itertools import pairwise
from heapq import heappush, heappop


class Keypad:
    """Base class for keypads."""

    keypad = ''
    start = ''
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }

    def __init__(self, directional_keypad):
        self.d_keypad = directional_keypad

    def __call__(self, code):
        return sum(
            self.find_dist(a, b)
            for a, b in pairwise(self.start + code)
        )

    @cached_property
    def vertices(self):
        """Retrun a dictionary of coordinates to buttons."""
        return {
            (i // 3, i % 3): char
            for i, char in enumerate(self.keypad)
            if char != ' '
        }

    @cached_property
    def graph(self):
        """Return a graph of vertices and directions."""
        graph = defaultdict(dict)

        for vertex in self.vertices:
            x, y = vertex
            for direction, (dx, dy) in self.directions.items():
                neighbor = (x + dx, y + dy)
                if neighbor not in self.vertices:
                    continue

                u = self.vertices[vertex]
                v = self.vertices[neighbor]
                graph[u][v] = direction

        return graph

    @lru_cache
    def find_dist(self, start, end):
        """Return the length of the shortest sequence of button
        presses.
        """
        min_dist = math.inf

        for u, d_u, dist in self._dijkstra(start):
            if u != end:
                continue

            dist += self.d_keypad.find_dist(d_u, self.d_keypad.start)
            if dist > min_dist:
                break

            min_dist = min(min_dist, dist)

        return min_dist

    def _dijkstra(self, start):
        queue = [(0, start, self.d_keypad.start)]
        visited = set()

        while queue:
            dist, u, d_u = heappop(queue)
            if (u, d_u) in visited:
                continue

            visited.add((u, d_u))
            yield u, d_u, dist

            for v, d_v in self.graph[u].items():
                d_dist = self.d_keypad.find_dist(d_u, d_v)
                heappush(queue, (dist + d_dist, v, d_v))


class NumericKeypad(Keypad):
    """Keypad with numeric buttons."""

    keypad = (
        '789'
        '456'
        '123'
        ' 0A'
    )
    start = 'A'


class DirectionalKeypad(Keypad):
    """Keypad with directional buttons."""

    keypad = (
        ' ^A'
        '<v>'
    )
    start = 'A'


class YourKeypad(DirectionalKeypad):
    """The directional keypad that you are using."""

    def __init__(self):
        super().__init__(None)

    def find_dist(self, start, end):
        return 1


def parse(filename):
    """Parse the input file and return a list of door codes."""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]


def create_keypads(num_keypads):
    """Create a chain of keypads.

    :param num_keypads: The number of remote directional keypads.
    """
    keypad = YourKeypad()
    for _ in range(num_keypads):
        keypad = DirectionalKeypad(keypad)
    return NumericKeypad(keypad)


def sum_complexities(keypad, codes):
    """Return the sum of complexities for all door codes."""
    return sum(keypad(code) * int(code[:-1]) for code in codes)


def test_example():
    """Test the example."""
    codes = parse('example.txt')
    keypad = create_keypads(2)
    assert sum_complexities(keypad, codes) == 126384


def test_puzzle():
    """Test the puzzle."""
    codes = parse('input.txt')
    keypad = create_keypads(2)
    assert sum_complexities(keypad, codes) == 182844

    keypad = create_keypads(25)
    assert sum_complexities(keypad, codes) == 226179529377982
