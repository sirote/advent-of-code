"""Day 14: Restroom Redoubt"""


import math
import re
from collections import Counter
from dataclasses import dataclass
from itertools import count
from typing import List, NamedTuple, Tuple


class Robot(NamedTuple):
    """Robot with position and velocity."""

    pos: Tuple[int, int]
    vel: Tuple[int, int]

    def move(self, wide, tall, seconds=1):
        """Move robot to new position in a given space after number of
        seconds.
        """
        return Robot(
            (
                (self.pos[0] + self.vel[0] * seconds) % wide,
                (self.pos[1] + self.vel[1] * seconds) % tall,
            ),
            self.vel,
        )


@dataclass
class Space:
    """The space outside the restroom."""

    wide: int
    tall: int
    robots: List[Robot]

    def next(self, seconds=1):
        """Move all robots to new positions after number of seconds."""
        self.robots = [
            r.move(self.wide, self.tall, seconds)
            for r in self.robots
        ]

    def quadrants(self):
        """Count robots in each quadrant."""
        quadrant = Counter()
        mid_x = self.wide // 2
        mid_y = self.tall // 2

        for robot in self.robots:
            x, y = robot.pos
            if x == mid_x or y == mid_y:
                continue

            quadrant[int(x > mid_x), int(y > mid_y)] += 1

        return quadrant

    def draw(self):
        """Draw robots in the space."""
        positions = {robot.pos for robot in self.robots}

        for y in range(self.tall):
            for x in range(self.wide):
                if (x, y) in positions:
                    print('#', end='')
                else:
                    print('.', end='')
            print()


def parse(filename):
    """Parse input file with robots positions and velocities."""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
            yield Robot(
                (int(m.group(1)), int(m.group(2))),
                (int(m.group(3)), int(m.group(4))),
            )


def entropy(robots):
    """Calculate entropy of the robots positions."""
    result = 0
    positions = {robot.pos for robot in robots}

    while positions:
        queue = [positions.pop()]
        result += 1
        while queue:
            x, y = queue.pop()
            for m, n in (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1):
                try:
                    positions.remove((m, n))
                except KeyError:
                    pass
                else:
                    queue.append((m, n))

    return result


def test_example():
    """Test the example."""
    robots = list(parse('example.txt'))
    space = Space(11, 7, robots)
    space.next(100)
    assert math.prod(space.quadrants().values()) == 12


def test_puzzle():
    """Test the puzzle."""
    robots = list(parse('input.txt'))
    space = Space(101, 103, robots)
    space.next(100)
    assert math.prod(space.quadrants().values()) == 221616000

    space = Space(101, 103, robots)
    for seconds in count(1):
        space.next()
        if entropy(space.robots) < len(robots) // 2:
            space.draw()
            assert seconds == 7572
            break
