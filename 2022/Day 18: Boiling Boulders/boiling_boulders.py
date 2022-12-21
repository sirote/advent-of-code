"""Day 18: Boiling Boulders"""


from collections import deque
from operator import itemgetter


def parse(filename):
    """Return an iterable of lava droplet positions."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield tuple(int(i) for i in line.split(','))


def adjacents(position):
    """Return adjacent positions (connected side)."""
    adjacent = deque((1, 0, 0))
    for _ in range(3):
        yield tuple(i + j for i, j in zip(position, adjacent))
        yield tuple(i - j for i, j in zip(position, adjacent))
        adjacent.rotate()


def out_of_bound(position, min_pos, max_pos):
    """Wether the given position is out of bound."""
    return (
        any(a < b for a, b in zip(position, min_pos))
        or any(a > b for a, b in zip(position, max_pos))
    )


def get_min_position(positions):
    """Return the position next to the lowest position of lava
    droplet.
    """
    return tuple(
        min(positions, key=itemgetter(i))[i] - 1
        for i in range(3)
    )


def get_max_position(positions):
    """Return the position next to the highest position of lava
    droplet.
    """
    return tuple(
        max(positions, key=itemgetter(i))[i] + 1
        for i in range(3)
    )


def count_surface_area(positions):
    """Count the surface area of lava droplet."""
    positions = set(positions)
    return sum(
        adjacent not in positions
        for position in positions
        for adjacent in adjacents(position)
    )


def count_exterior_surface_area(positions):
    """Count the exterior surface area of lava droplet."""
    total = 0
    min_pos = get_min_position(positions)
    max_pos = get_max_position(positions)
    positions = set(positions)
    visited = set()

    queue = [min_pos]
    while queue:
        if (position := queue.pop()) in visited:
            continue

        visited.add(position)

        for adjacent in adjacents(position):
            if out_of_bound(adjacent, min_pos, max_pos):
                continue

            if adjacent in positions:
                total += 1
            else:
                queue.append(adjacent)

    return total


def main():
    """Main entry."""
    positions = list(parse('input'))
    assert count_surface_area(positions) == 4536
    assert count_exterior_surface_area(positions) == 2606


if __name__ == '__main__':
    main()
