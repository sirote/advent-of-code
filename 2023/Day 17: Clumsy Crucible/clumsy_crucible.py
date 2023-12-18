"""Day 17: Clumsy Crucible"""


from heapq import heappush, heappop
from typing import NamedTuple


START = (0, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)

MOVES = {
    START: (RIGHT, LEFT, UP, DOWN),
    RIGHT: (RIGHT, UP, DOWN),
    LEFT: (LEFT, UP, DOWN),
    UP: (UP, LEFT, RIGHT),
    DOWN: (DOWN, LEFT, RIGHT),
}

TILES = {
    RIGHT: '>',
    LEFT: '<',
    UP: '^',
    DOWN: 'v',
}


class Crucible(NamedTuple):
    """A Clumsy Crucible."""

    position: tuple[int, int]
    direction: tuple[int, int]
    straight: int

    def move(self, city_map):
        """Return the next possible crucibles from current position."""
        for direction in MOVES[self.direction]:
            position = (
                self.position[0] + direction[0],
                self.position[1] + direction[1],
            )
            if city_map.out_of_bounds(position):
                continue

            # Can move at most three blocks in the same direction before
            # it must turn
            straight = self.straight + 1 if direction == self.direction else 0
            if straight == 3:
                continue

            yield Crucible(position, direction, straight)


class UltraCrucible(Crucible):
    """An Ultra Clumsy Crucible."""

    def move(self, city_map):
        """Return the next possible crucibles from current position."""
        for direction in MOVES[self.direction]:
            position = (
                self.position[0] + direction[0],
                self.position[1] + direction[1],
            )
            if city_map.out_of_bounds(position):
                continue

            # Need to move a minimum of four blocks in the same
            # direction
            if (self.direction != START
                    and direction != self.direction
                    and self.straight < 3):
                continue

            # Need to move a minimum of four blocks before it can stop
            # at the end
            if (position == city_map.end
                    and (direction != self.direction
                         or self.straight < 2)):
                continue

            # Can move a maximum of ten consecutive blocks without
            # turning
            straight = self.straight + 1 if direction == self.direction else 0
            if straight == 10:
                continue

            yield UltraCrucible(position, direction, straight)


class CityMap:
    """A map of the city with the heat loss at each position."""

    def __init__(self, city_map):
        self.city_map = city_map

    @property
    def start(self):
        """The start position."""
        return 0, 0

    @property
    def end(self):
        """The end position."""
        return len(self.city_map) - 1, len(self.city_map[0]) - 1

    def out_of_bounds(self, position):
        """Return True if the position is out of bounds."""
        x, y = position
        return (
            x < 0
            or y < 0
            or x >= len(self.city_map)
            or y >= len(self.city_map[0])
        )

    def heat_loss(self, position):
        """Return the heat loss at the given position."""
        return self.city_map[position[0]][position[1]]

    def draw(self, crucibles=()):
        """Draw the crucibles on the map."""
        pos_to_direction = {
            position: TILES.get(direction)
            for position, direction, _ in crucibles
        }
        for i, row in enumerate(self.city_map):
            for j, cell in enumerate(row):
                cell = pos_to_direction.get((i, j)) or cell
                print(cell, end='')
            print()


def parse(filename):
    """Parse the city map into a grid of integers."""
    with open(filename, 'r', encoding='utf-8') as file_:
        return tuple(tuple(map(int, line.strip())) for line in file_)


def find_path(city_map, crucible_type=Crucible):
    """Find the path with the minimum heat loss."""
    data = list(dijkstra(city_map, crucible_type))
    curr, _, heat_loss = data[-1]
    predecessors = {curr: prev for curr, prev, _ in data}
    crucibles = []
    while curr:
        crucibles.append(curr)
        curr = predecessors[curr]

    return reversed(crucibles), heat_loss


def dijkstra(city_map, crucible_type):
    """Iterate over the subsolutions to the path using Dijkstra's
    algorithm.
    """
    visited = set()
    queue = [(0, crucible_type(city_map.start, START, 0), None)]
    while queue:
        heat_loss, crucible, prev_crucible = heappop(queue)
        if crucible in visited:
            continue

        yield crucible, prev_crucible, heat_loss
        visited.add(crucible)

        if crucible.position == city_map.end:
            return

        for next_crucible in crucible.move(city_map):
            heappush(queue, (
                heat_loss + city_map.heat_loss(next_crucible.position),
                next_crucible,
                crucible,
            ))

    raise ValueError('No path found')


def main():
    """Main program."""
    city_map = CityMap(parse('input'))
    _, heat_loss = find_path(city_map, Crucible)
    assert heat_loss == 755
    _, heat_loss = find_path(city_map, UltraCrucible)
    assert heat_loss == 881


if __name__ == '__main__':
    main()
