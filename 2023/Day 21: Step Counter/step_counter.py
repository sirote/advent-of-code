"""Day 21: Step Counter"""


import math
from collections import deque, defaultdict


def parse(filename):
    """Parse the garden map."""
    map_ = []
    start = None
    with open(filename, 'r', encoding='utf-8') as file_:
        for i, line in enumerate(file_):
            for j, char in enumerate(line.strip()):
                if char == 'S':
                    start = (i, j)
                    map_.append(line.strip().replace('S', '.'))
                    break
            else:
                map_.append(line.strip())

    return map_, start


def iter_garden_plots(map_, start):
    """Iterate over number of reachable garden plots on each step."""
    curr_step = 0
    visited = set()
    tiles = defaultdict(int)
    queue = deque([(curr_step, start)])
    while queue:
        step, (x, y) = queue.popleft()
        if step > curr_step:
            yield sum(
                amount for step, amount in tiles.items()
                if step % 2 == curr_step % 2
            )
            curr_step = step

        if (x, y) in visited:
            continue

        tiles[step] += 1
        visited.add((x, y))

        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            mx, my = nx % len(map_), ny % len(map_[0])
            if map_[mx][my] == '.':
                queue.append((step + 1, (nx, ny)))


def count_garden_plots(map_, start, steps):
    """Count the number of reachable garden plots in given steps."""
    if _calculable(map_, start, steps):
        return _calculate(map_, start, steps)
    return _simulate(map_, start, steps)


def _calculable(map_, start, steps):
    """Check if the number of reachable garden plots is calculable by
    solving a quadratic function.
    """
    if len(map_) != len(map_[0]):
        return False

    x, y = start
    if (any(map_[i][y] == '#' for i in range(len(map_)))
            or any(map_[x][j] == '#' for j in range(len(map_[0])))):
        return False

    if steps % len(map_) != x:
        return False

    return True


def _simulate(map_, start, steps):
    for step, amount in enumerate(iter_garden_plots(map_, start)):
        if step == steps:
            return amount
    return math.inf


def _calculate(map_, start, steps):
    length = len(map_)
    x, _ = start
    target_steps = (x, x + length, x + 2 * length)
    plots = []
    for step, amount in enumerate(iter_garden_plots(map_, start)):
        if step in target_steps:
            plots.append(amount)
            if len(plots) == len(target_steps):
                break

    a = (plots[2] - 2 * plots[1] + plots[0]) // 2
    b = plots[1] - plots[0] - a
    c = plots[0]
    steps = (steps - x) // length

    return a * steps ** 2 + b * steps + c


def main():
    """Main program."""
    map_, start = parse('input')
    assert count_garden_plots(map_, start, 64) == 3671
    assert count_garden_plots(map_, start, 26501365) == 609708004316870


if __name__ == '__main__':
    main()
