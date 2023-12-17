"""Day 16: The Floor Will Be Lava"""


from itertools import chain
from typing import NamedTuple


RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)

directions = {
    RIGHT: {
        '.': [RIGHT],
        '|': [UP, DOWN],
        '-': [RIGHT],
        '\\': [DOWN],
        '/': [UP],
    },
    LEFT: {
        '.': [LEFT],
        '|': [UP, DOWN],
        '-': [LEFT],
        '\\': [UP],
        '/': [DOWN],
    },
    UP: {
        '.': [UP],
        '|': [UP],
        '-': [LEFT, RIGHT],
        '\\': [LEFT],
        '/': [RIGHT],
    },
    DOWN: {
        '.': [DOWN],
        '|': [DOWN],
        '-': [LEFT, RIGHT],
        '\\': [RIGHT],
        '/': [LEFT],
    },
}


def parse(filename):
    """Parse the the layout of the contraption into a grid."""
    with open(filename, 'r', encoding='utf-8') as file_:
        return tuple(line.strip() for line in file_)


class LightBeam(NamedTuple):
    """A light beam."""

    x: int
    y: int
    direction: tuple[int, int]

    @property
    def next_tile(self):
        """Return the next tile."""
        return self.x + self.direction[0], self.y + self.direction[1]


class Contraption:
    """A contraption that bounces light beams around."""

    def __init__(self, grid):
        self.grid = grid
        self.beams = set()

    @property
    def energized_tiles(self):
        """Return the tiles that are energized."""
        return {(x, y) for x, y, _ in self.beams}

    def energize(self, start=LightBeam(0, -1, RIGHT)):
        """Energize the contraption with a light beam."""
        queue = [start]
        while queue:
            beam = queue.pop()
            self.beams.add(beam)

            x, y = beam.next_tile
            if self._out_of_bounds(x, y):
                continue

            queue.extend(
                beam
                for direction in directions[beam.direction][self.grid[x][y]]
                if (beam := LightBeam(x, y, direction)) not in self.beams
            )

        self.beams.remove(start)
        return self

    def _out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= len(self.grid) or y >= len(self.grid[0])


def iter_configurations(grid):
    """Iterate over all initial beam configurations."""
    downward = (LightBeam(-1, j, DOWN) for j in range(len(grid[0])))
    upward = (LightBeam(len(grid), j, UP) for j in range(len(grid[0])))
    right = (LightBeam(i, -1, RIGHT) for i in range(len(grid)))
    left = (LightBeam(i, len(grid[0]), LEFT) for i in range(len(grid)))
    yield from chain(downward, upward, right, left)


def main():
    """Main program."""
    grid = parse('input')
    assert len(Contraption(grid).energize().energized_tiles) == 7242
    assert max(
        len(Contraption(grid).energize(beam).energized_tiles)
        for beam in iter_configurations(grid)
    ) == 7572


if __name__ == '__main__':
    main()
