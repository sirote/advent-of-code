"""Day 23: A Long Walk"""


from collections import defaultdict
from itertools import chain


LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)


def parse(filename):
    """Parse the map of the hiking trails."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield line.strip()


def get_starting_position(map_):
    """Get the starting position."""
    for i, char in enumerate(map_[0]):
        if char == '.':
            return 0, i

    raise ValueError('No starting position found.')


def get_ending_position(map_):
    """Get the ending position."""
    for i, char in enumerate(map_[-1]):
        if char == '.':
            return len(map_) - 1, i

    raise ValueError('No ending position found.')


def iter_intersections(map_):
    """Iterate over all intersections in the map."""
    start = get_starting_position(map_)
    visited = set()
    queue = [start]
    while queue:
        pos = queue.pop()
        if pos in visited:
            continue

        visited.add(pos)
        positions = list(iter_next_positions(map_, pos))
        if len(positions) > 2:
            yield pos

        queue.extend(positions)


def iter_next_positions(map_, pos, forbid=None, slopes=None):
    """Iterate over all possible next positions."""
    x, y = pos
    forbid = forbid or {}
    slopes = slopes or {}
    if direction := slopes.get(map_[x][y]):
        dx, dy = direction
        yield x + dx, y + dy
    else:
        for direction in (LEFT, RIGHT, UP, DOWN):
            dx, dy = direction
            nx, ny = x + dx, y + dy

            in_bounds = 0 <= nx < len(map_) and 0 <= ny < len(map_[0])
            if not in_bounds:
                continue

            forest = map_[nx][ny] == '#'
            forbidden = map_[nx][ny] == forbid.get(direction)
            if forest or forbidden:
                continue

            yield nx, ny


def build_graph(map_, intersections, forbid=None, slopes=None):
    """Build a graph of the map by connecting all intersections."""
    graph = defaultdict(list)
    for intersection in intersections:
        for next_pos in iter_next_positions(
                map_, intersection, forbid, slopes):
            visited = {intersection, next_pos}
            dest, dist = _dfs(map_, next_pos, visited, intersections)
            graph[intersection].append((dest, dist))

    return graph


def _dfs(map_, pos, visited, destinations):
    dist = 1
    while True:
        for next_pos in iter_next_positions(map_, pos):
            if next_pos in visited:
                continue

            visited.add(next_pos)
            dist += 1
            if next_pos in destinations:
                return next_pos, dist

            pos = next_pos


def count_steps(map_, forbid=None, slopes=None):
    """Count the number of steps in the longest hike."""
    start = get_starting_position(map_)
    end = get_ending_position(map_)
    intersections = set(chain((start, end), iter_intersections(map_)))
    graph = build_graph(map_, intersections, forbid, slopes)

    longest = 0
    queue = [(0, start, set())]
    while queue:
        dist, pos, visited = queue.pop()
        if pos in visited:
            continue

        visited.add(pos)
        for next_pos, next_dist in graph[pos]:
            new_dist = dist + next_dist
            if next_pos == end:
                longest = max(longest, new_dist)
            else:
                queue.append((new_dist, next_pos, set(visited)))

    return longest


def main():
    """Main program."""
    map_ = list(parse('input'))
    assert count_steps(
        map_,
        forbid={LEFT: '>', RIGHT: '<', UP: 'v', DOWN: '^'},
        slopes={'<': LEFT, '>': RIGHT, '^': UP, 'v': DOWN}
    ) == 1998
    assert count_steps(
        map_,
        forbid={},
        slopes={},
    ) == 6434


if __name__ == '__main__':
    main()
