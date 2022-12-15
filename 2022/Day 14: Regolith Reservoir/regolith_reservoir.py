"""Day 14: Regolith Reservoir"""


import re
from operator import itemgetter


def parse(filename):
    """Return an iterable of rock coordinates of the cave."""
    with open(filename, 'r', encoding='utf-8') as file_:
        yield from (point for line in file_ for point in _parse(line))


def _parse(line):
    points = [
        (int(p_x), int(p_y))
        for p_x, p_y in re.findall(r'(\d+),(\d+)', line)
    ]
    for (s_x, s_y), (t_x, t_y) in zip(points, points[1:]):
        if s_x == t_x:
            step = 1 if t_y > s_y else -1
            path = ((s_x, p_y) for p_y in range(s_y, t_y + step, step))
        elif s_y == t_y:
            step = 1 if t_x > s_x else -1
            path = ((p_x, s_y) for p_x in range(s_x, t_x + step, step))

        yield from path


def simulate(rocks):
    """Simulate the falling sand and return an iterable of sand
    positions.
    """
    occupied = set(rocks)
    _, bottom = max(rocks, key=itemgetter(1))

    while True:
        p_x, p_y = 500, 0
        while True:
            if p_y == bottom:
                return

            for n_x, n_y in ((p_x, p_y + 1),
                             (p_x - 1, p_y + 1),
                             (p_x + 1, p_y + 1)):
                if (n_x, n_y) not in occupied:
                    p_x, p_y = n_x, n_y
                    break
            else:
                occupied.add((p_x, p_y))
                yield p_x, p_y
                if p_y == 0:
                    return
                break


def add_floor(rocks):
    """Add floor at the bottom of the scan."""
    rocks = list(rocks)
    pouring_y = 500
    floor_y = 2
    _, bottom = max(rocks, key=itemgetter(1))

    rocks.append((pouring_y, bottom + floor_y))
    for i in range(1, bottom + floor_y + 1):
        for j in (1, -1):
            rocks.append((pouring_y + i * j, bottom + floor_y))

    return rocks


def main():
    """Entry point."""
    rocks = list(parse('input'))
    assert len(list(simulate(rocks))) == 793
    assert len(list(simulate(add_floor(rocks)))) == 24166


if __name__ == '__main__':
    main()
