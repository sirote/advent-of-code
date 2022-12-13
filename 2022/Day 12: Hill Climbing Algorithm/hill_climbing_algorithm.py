"""Day 12: Hill Climbing Algorithm"""


from collections import deque


def parse(filename):
    """Return an iterable of rows of a heightmap."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield line.rstrip()


def find_path(heightmap, *start):
    """Return a path as a list of positions from start to end."""
    preds, end = _bfs(heightmap, *start)
    path = [end]
    while (pred := preds[end]):
        path.append(pred)
        end = pred

    return list(reversed(path))


def _bfs(heightmap, *start):
    max_x = len(heightmap)
    max_y = len(heightmap[0])

    queue = deque([(*s, 'a') for s in start])
    preds = {s: None for s in start}

    while queue:
        pos_x, pos_y, curr_height = queue.popleft()
        max_height = chr(ord(curr_height) + 1)

        for d_x, d_y in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_x = pos_x + d_x
            new_y = pos_y + d_y

            if (_out_of_bound(new_x, new_y, max_x, max_y)
                    or (new_x, new_y) in preds
                    or (new_height := heightmap[new_x][new_y]) > max_height
                    or new_height == 'E' and curr_height < 'y'):
                continue

            preds[new_x, new_y] = pos_x, pos_y
            if new_height == 'E':
                return preds, (new_x, new_y)

            queue.append((new_x, new_y, new_height))

    raise RuntimeError(f'Path not found: {start}')


def _out_of_bound(pos_x, pos_y, height, width):
    return pos_x < 0 or pos_x >= height or pos_y < 0 or pos_y >= width


def positions(heightmap, height):
    """Return an iterable of positions for a given height."""
    yield from (
        (i, j)
        for i, row in enumerate(heightmap)
        for j, value in enumerate(row)
        if value in height
    )


def main():
    """Main entry."""
    heightmap = list(parse('input'))
    assert len(find_path(heightmap, *positions(heightmap, 'S'))) - 1 == 361
    assert len(find_path(heightmap, *positions(heightmap, 'Sa'))) - 1 == 354


if __name__ == '__main__':
    main()
