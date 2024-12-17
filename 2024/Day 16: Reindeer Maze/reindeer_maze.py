"""Day 16: Reindeer Maze"""


import math
from collections import defaultdict, deque
from typing import NamedTuple


class Maze(NamedTuple):
    """The Reindeer Maze."""

    map: list[str]
    start: tuple[int, int]
    end: tuple[int, int]
    direction: tuple[int, int]

    def start_reindeer(self):
        """Return the starting Reindeer."""
        return Reindeer(self.start, self.direction, 0)


class Reindeer(NamedTuple):
    """The Reindeer in the maze."""

    position: tuple[int, int]
    direction: tuple[int, int]
    score: int

    def moves(self, maze_map):
        """Return the possible moves for the Reindeer."""
        for dx, dy in (0, 1), (1, 0), (0, -1), (-1, 0):
            m, n = self.position[0] + dx, self.position[1] + dy
            if maze_map[m][n] == '#':
                continue

            if self.direction[0] + dx == 0 and self.direction[1] + dy == 0:
                continue

            score = self.score + 1
            if (dx, dy) != self.direction:
                score += 1000

            yield Reindeer((m, n), (dx, dy), score)


def parse(filename):
    """Parse the input file and return a Maze object."""
    start = end = None
    direction = (0, 1)
    map_ = []

    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            map_.append(line := line.strip())
            for j, cell in enumerate(line):
                if cell == 'S':
                    start = (i, j)
                elif cell == 'E':
                    end = (i, j)

    return Maze(map_, start, end, direction)


def solve(maze):
    """Solve the maze and return the lowest score and the number of
    tiles that are part of of at least one of the best paths.
    """
    reindeer = maze.start_reindeer()
    queue = deque([(reindeer, {reindeer})])
    visited = defaultdict(lambda: math.inf)
    joints = {}
    min_score = math.inf
    min_paths = []

    while queue:
        reindeer, path = queue.popleft()
        if reindeer.position == maze.end:
            if reindeer.score < min_score:
                min_score = reindeer.score
                min_paths = [path]
            elif reindeer.score == min_score:
                min_paths.append(path)
            continue

        if reindeer.score > min_score:
            continue

        visit_score = visited[reindeer.position, reindeer.direction]
        if reindeer.score > visit_score:
            continue

        if reindeer.score == visit_score:
            joints[reindeer] = path
            continue

        visited[reindeer.position, reindeer.direction] = reindeer.score

        for _reindeer in reindeer.moves(maze.map):
            queue.append((_reindeer, path | {_reindeer}))

    tiles = {
        tile
        for path in min_paths
        for tile in _merge_paths(path, joints)
    }
    return min_score, len(tiles)


def _merge_paths(path, joints):
    result = {r.position for r in path}
    queue = [path]

    while queue:
        path = queue.pop()
        for reindeer in path:
            if _reindeer := joints.pop(reindeer, None):
                queue.append(_reindeer)
                result.update(r.position for r in _reindeer)

    return result


def test_example():
    """Test the example."""
    score, tiles = solve(parse('example1.txt'))
    assert score == 7036
    assert tiles == 45

    score, tiles = solve(parse('example2.txt'))
    assert score == 11048
    assert tiles == 64


def test_puzzle():
    """Test the puzzle."""
    score, tiles = solve(parse('input.txt'))
    assert score == 74392
    assert tiles == 426
