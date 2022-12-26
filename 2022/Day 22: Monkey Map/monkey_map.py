"""Day 22: Monkey Map"""


import re
from itertools import takewhile
from operator import itemgetter


def parse(filename):
    """Return a map of the board and description of the path."""
    with open(filename, 'r', encoding='utf-8') as file_:
        board_map = _parse_map(takewhile(lambda l: l.rstrip(), file_))
        path = _parse_path(file_)

    return board_map, path


def _parse_map(lines):
    board_map = {}
    for i, line in enumerate(lines):
        for j, tile in enumerate(line.rstrip()):
            if tile != ' ':
                board_map[i, j] = tile

    return board_map


def _parse_path(file_):
    return [
        (turn, int(tiles))
        for turn, tiles in re.findall(r'([LR]?)(\d+)', file_.read())
    ]


def move(board_map, path, find_wrap, position=None, direction=(0, 1)):
    """Return the last position and direction after moving according to
    the description of the path on the baord map.
    """
    directions = {
        'L': lambda i, j: (-j, i),
        'R': lambda i, j: (j, -i),
        '': lambda i, j: (i, j),
    }
    pos = position or min(board_map)

    for turn, tiles in path:
        direction = directions[turn](*direction)
        for _ in range(tiles):
            new_pos = pos[0] + direction[0], pos[1] + direction[1]
            if (tile := board_map.get(new_pos)) == '#':
                break

            if tile == '.':
                pos = new_pos
                continue

            new_pos, new_dir = find_wrap(pos, direction)
            if board_map[new_pos] == '#':
                break

            pos = new_pos
            direction = new_dir

    return pos, direction


def flat_wrap(board_map):
    """Return a function to find wrap position on a 2D map."""
    def wrap(pos, dir_):
        i, j = dir_
        if i == 0:
            points = (p for p in board_map if p[0] == pos[0])
            minmax = min if j == 1 else max
            return minmax(points, key=itemgetter(1)), dir_

        if j == 0:
            points = (p for p in board_map if p[1] == pos[1])
            minmax = min if i == 1 else max
            return minmax(points), dir_

        raise ValueError(f'Invalid position: {pos}')

    return wrap


def cube_wrap(board_map):
    """Return a function to find wrap position on a cube map."""
    def ceil(value):
        return (value + size) // size * size

    def floor(value):
        return value // size * size

    def wrap(pos, dir_):
        p_x, p_y = pos

        if dir_ == (0, 1):
            return _wrap(p_x, p_y, board_map)

        if dir_ == (0, -1):
            (p_x, p_y), (i, j) = _wrap(-p_x - 1, -p_y - 1, reverse_map)
            return (-p_x - 1, -p_y - 1), (-i, -j)

        if dir_ == (1, 0):
            (p_x, p_y), (i, j) = _wrap(-p_y - 1, p_x, rotate_left_map)
            return (p_y, -p_x - 1), (j, -i)

        if dir_ == (-1, 0):
            (p_x, p_y), (i, j) = _wrap(p_y, -p_x - 1, rotate_right_map)
            return (-p_y - 1, p_x), (-j, i)

        raise ValueError(f'Invalid direction: {dir_}')

    def _wrap(p_x, p_y, board_map):
        if (p_x, p_y + 1) in board_map:
            return (
                (p_x, p_y + 1),
                (0, 1),
            )
        if (p_x, p_y - 3 * size) in board_map:
            return (
                (p_x, p_y - 4 * size + 1),
                (0, 1),
            )
        if (p_x + size, p_y + 1) in board_map:
            return (
                (ceil(p_x), p_y + ceil(p_x) - p_x),
                (1, 0),
            )
        if (p_x - size, p_y + 1) in board_map:
            return (
                (floor(p_x) - 1, p_y + p_x - floor(p_x) + 1),
                (-1, 0),
            )
        if (p_x + 2 * size, p_y + 1) in board_map:
            return (
                (2 * ceil(p_x) + size - p_x - 1, p_y + size),
                (0, -1),
            )
        if (p_x - 2 * size, p_y + 1) in board_map:
            return (
                (2 * floor(p_x) - size - p_x - 1, p_y + size),
                (0, -1),
            )
        if (p_x + 3 * size, p_y + 1) in board_map:
            return (
                (ceil(p_x) + 3 * size - 1, p_y + p_x - floor(p_x) + 1),
                (-1, 0),
            )
        if (p_x - 3 * size, p_y + 1) in board_map:
            return (
                (floor(p_x) - 3 * size, p_y + ceil(p_x) - p_x),
                (1, 0),
            )
        if (p_x + size, p_y - 3 * size) in board_map:
            return (
                (ceil(p_x) + size - 1, p_y - 3 * size - ceil(p_x) + p_x + 1),
                (-1, 0),
            )
        if (p_x - size, p_y - 3 * size) in board_map:
            return (
                (floor(p_x) - size, p_y - 3 * size - p_x + floor(p_x)),
                (1, 0),
            )
        if (p_x + 2 * size, p_y - size) in board_map:
            return (
                (2 * ceil(p_x) + size - p_x - 1, p_y - size),
                (0, -1),
            )
        if (p_x - 2 * size, p_y - size) in board_map:
            return (
                (2 * floor(p_x) - size - p_x - 1, p_y - size),
                (0, -1),
            )
        if (p_x + 2 * size, p_y - 2 * size) in board_map:
            return (
                (
                    ceil(p_x) + 2 * size - 1,
                    p_y - 2 * size - ceil(p_x) + p_x + 1
                ),
                (-1, 0),
            )
        if (p_x - 2 * size, p_y - 2 * size) in board_map:
            return (
                (floor(p_x) - 2 * size, p_y - 2 * size - p_x + floor(p_x)),
                (1, 0),
            )

        raise ValueError(f'Invalid position: {(p_x, p_y)}')

    size = min(
        max(board_map)[0],
        max(board_map, key=itemgetter(1))[1],
    ) // 3 + 1
    reverse_map = {
        (-x - 1, -y - 1): tile
        for (x, y), tile in board_map.items()
    }
    rotate_right_map = {
        (y, -x - 1): tile
        for (x, y), tile in board_map.items()
    }
    rotate_left_map = {
        (-y - 1, x): tile
        for (x, y), tile in board_map.items()
    }
    return wrap


def get_password(position, direction):
    """Return the password."""
    directions = {
        (0, 1): 0,
        (1, 0): 1,
        (0, -1): 2,
        (-1, 0): 3,
    }
    i, j = position
    return (i + 1) * 1000 + 4 * (j + 1) + directions[direction]


def main():
    """Main entry."""
    board_map, path = parse('input')
    position, direction = move(board_map, path, flat_wrap(board_map))
    assert get_password(position, direction) == 29408

    position, direction = move(board_map, path, cube_wrap(board_map))
    assert get_password(position, direction) == 115311


if __name__ == '__main__':
    main()
