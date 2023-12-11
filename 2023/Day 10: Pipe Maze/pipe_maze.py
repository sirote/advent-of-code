"""Day 10: Pipe Maze"""


from itertools import groupby


NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)

direction_to_pipes = {
    NORTH: {'|', '7', 'F', 'S'},
    SOUTH: {'|', 'L', 'J', 'S'},
    WEST: {'-', 'L', 'F', 'S'},
    EAST: {'-', 'J', '7', 'S'},
}

pipe_to_directions = {
    'S': (NORTH, SOUTH, WEST, EAST),
    '|': (NORTH, SOUTH),
    '-': (WEST, EAST),
    'L': (NORTH, EAST),
    'J': (NORTH, WEST),
    '7': (WEST, SOUTH),
    'F': (SOUTH, EAST),
}

border_pipes = {
    'F': 'J',
    'L': '7',
}

closed_pairs = {
    ('F', '7'),
    ('L', 'J'),
}


def parse(filename):
    """Parse the pipe maze into a grid."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield line.strip()


def iter_loop_tiles(maze):
    """Iterate over the tiles of the loop in the maze."""
    prev = None
    start = curr = find_start(maze)
    yield start

    while True:
        x, y = curr
        pipe = maze[x][y]
        for direction in pipe_to_directions[pipe]:
            i, j = direction
            next_ = x + i, y + j

            if next_ == prev:
                continue

            if next_ == start:
                return

            next_pipe = maze[next_[0]][next_[1]]
            if next_pipe in direction_to_pipes[direction]:
                prev = curr
                yield (curr := next_)
                break


def find_start(maze):
    """Find the start position of the maze."""
    for i, row in enumerate(maze):
        for j, tile in enumerate(row):
            if tile == 'S':
                return i, j

    raise ValueError('No start found')


def count_enclosed_tiles(loop_tiles, maze):
    """Count the number of tiles enclosed by the loop."""
    count = 0
    for _, tiles in groupby(sorted(loop_tiles), key=lambda tile: tile[0]):
        borders = iter_borders(tiles, maze)
        for left in borders:
            _, (l_x, l_y) = left
            if right := next(borders, None):
                (r_x, r_y), _ = right
                if (maze[l_x][l_y], maze[r_x][r_y]) in closed_pairs:
                    continue

                count += r_y - l_y - 1

    return count


def iter_borders(tiles, maze):
    """Iterate over the borders of the tiles."""
    positions = filter(lambda p: maze[p[0]][p[1]] != '-', tiles)
    for x, y in positions:
        if (pipe := maze[x][y]) in border_pipes:
            try:
                n_x, n_y = next(positions)
            except StopIteration as error:
                raise ValueError('Invalid loop') from error

            if maze[n_x][n_y] == border_pipes[pipe]:
                yield (x, y), (n_x, n_y)
            else:
                yield (x, y), (x, y)
                yield (n_x, n_y), (n_x, n_y)
        else:
            yield (x, y), (x, y)


def main():
    """Main program."""
    maze = list(parse('input'))
    loop_tiles = list(iter_loop_tiles(maze))
    assert len(loop_tiles) // 2 == 7066
    assert count_enclosed_tiles(loop_tiles, maze) == 401


if __name__ == '__main__':
    main()
