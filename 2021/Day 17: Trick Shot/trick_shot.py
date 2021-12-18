"""Day 17: Trick Shot"""


import re
from itertools import count, takewhile
from pathlib import Path


PATH = Path(__file__).parent


class TrickShot:

    def __init__(self, target_area):
        self.target_area = target_area
        self.drag = 1
        self.gravity = 1

    def get_highest(self, velocity_y):
        """Return the highest y position."""
        if velocity_y <= 0:
            return 0

        pos_y = 0
        while velocity_y:
            pos_y += velocity_y
            velocity_y -= self.gravity

        return pos_y

    def get_initial_velocities(self):
        """Return a set of initial velocity values cause the probe to be
        within the target area after any step.
        """
        _, _, min_y, max_y = self.target_area
        assert max_y < 0, (
            'Assume target area is below initial position to set upper'
            'bound of y velocity'
        )
        return {
            (x, y)
            for y in range(min_y, abs(min_y))
            for steps in self._steps(y)
            for x in self._x_velocities(steps)
        }

    def draw(self, initial_velocity):
        ax1, ax2, ay1, ay2 = self.target_area

        def in_boundary(point):
            pos_x, pos_y = point
            return (
                (ax1 < 0 and pos_x >= ax1 or ax2 > 0 and pos_x <= ax2)
                and (ay1 < 0 and  pos_y >= ay1 or ay2 > 0 and pos_y <= ay2)
            )

        def marker(point):
            if point == (0, 0):
                return 'S'
            if point in positions:
                return '#'
            if ax1 <= point[0] <= ax2 and ay1 <= point[1] <= ay2:
                return 'T'
            return '.'

        positions = set(takewhile(
            in_boundary,
            self._trajectory(initial_velocity)
        ))
        max_x = max(max(x for x, _ in positions), ax2, 0)
        min_x = min(min(x for x, _ in positions), ax1, 0)
        max_y = max(max(y for _, y in positions), ay2, 0)
        min_y = min(min(y for _, y in positions), ay1, 0)

        print('\n'.join(reversed([
            ''.join(marker((x, y)) for x in range(min_x, max_x + 1))
            for y in range(min_y, max_y + 1)
        ])))

    def _steps(self, velocity_y):
        _, _, min_y, max_y = self.target_area
        pos_y = 0

        for step in count(1):
            pos_y += velocity_y
            velocity_y -= self.gravity
            if min_y <= pos_y <= max_y:
                yield step
            elif pos_y < min_y:
                return

    def _x_velocities(self, steps):
        def _get_from(velocity_x):
            drag = self.drag * 1 if velocity_x > 0 else -1
            pos_x = 0
            for _ in range(steps):
                pos_x += velocity_x
                if velocity_x != 0:
                    velocity_x -= drag

            return pos_x

        min_x, max_x, _, _ = self.target_area
        for velocity_x in range(1, max_x + 1):
            pos_x = _get_from(velocity_x)
            if min_x <= pos_x <= max_x:
                yield velocity_x

    def _trajectory(self, initial_velocity):
        velocity_x, velocity_y = initial_velocity
        drag = self.drag * 1 if velocity_x > 0 else -1
        pos_x = pos_y = 0
        while True:
            pos_x += velocity_x
            pos_y += velocity_y
            yield pos_x, pos_y
            velocity_x = velocity_x - drag if velocity_x != 0 else 0
            velocity_y -= 1


def parse(path):
    with path.open(encoding='utf-8') as input_file:
        line = input_file.read().strip()
        pattern = r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)'
        if match := re.match(pattern, line):
            return tuple(int(n) for n in match.groups())

        raise ValueError(line)


def test_example():
    trick_short = TrickShot(parse(PATH / 'example'))
    _, _, area_y1, _ = trick_short.target_area
    max_velocity_y = abs(area_y1) - 1
    print()
    trick_short.draw((6, max_velocity_y))
    assert trick_short.get_highest(max_velocity_y) == 45


def test_part1():
    trick_short = TrickShot(parse(PATH / 'input'))
    _, _, area_y1, _ = trick_short.target_area
    max_velocity_y = abs(area_y1) - 1
    assert trick_short.get_highest(max_velocity_y) == 10585


def test_part2():
    trick_short = TrickShot(parse(PATH / 'input'))
    assert len(trick_short.get_initial_velocities()) == 5247
