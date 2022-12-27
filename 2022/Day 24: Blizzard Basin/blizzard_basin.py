"""Day 24: Blizzard Basin"""


from collections import defaultdict, deque
from functools import cache


def parse(filename):
    """Return the description of map of the valley and the blizzards."""
    tile_to_direction = {
        '^': 'up',
        'v': 'down',
        '<': 'left',
        '>': 'right',
    }
    blizzards = defaultdict(list)
    with open(filename, 'r', encoding='utf-8') as file_:
        line = next(file_)
        begin = (0, line.index('.'))
        i = j = 0

        for i, line in enumerate(file_, start=1):
            for j, tile in enumerate(line.rstrip()):
                if tile in ('^', 'v', '<', '>'):
                    direction = tile_to_direction[tile]
                    blizzards[direction].append((i, j))

        end = (i, line.index('.'))
        dimensions = i + 1, j + 1
        blizzards = {
            direction: frozenset(positions)
            for direction, positions in blizzards.items()
        }

    return begin, end, dimensions, blizzards


@cache
def next_state(height, width, up=(), down=(), left=(), right=()):
    """Return the next state of the valley and the blizzards."""
    return {
        'up': frozenset(((i - 2) % (height - 2) + 1, j) for i, j in up),
        'down': frozenset((i % (height - 2) + 1, j) for i, j in down),
        'left': frozenset((i, (j - 2) % (width - 2) + 1) for i, j in left),
        'right': frozenset((i, j % (width - 2) + 1) for i, j in right),
    }


def find_path(begin, end, dimensions, blizzards):
    """Return the shortest path to avoid the blizzards and reach the
    goal.
    """
    def canonical(node):
        pos, state = node
        return pos, tuple(state.items())

    def iter_children(node):
        pos, state = node
        new_state = next_state(height, width, **state)
        p_x, p_y = pos

        for i, j in (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0):
            new_pos = n_x, n_y = p_x + i, p_y + j
            if new_pos == end:
                yield new_pos, new_state
                break

            if (new_pos != begin
                    and (n_x <= 0 or n_x >= height - 1
                         or n_y <= 0 or n_y >= width - 1)):
                continue

            if all(new_pos not in blizzards
                   for blizzards in new_state.values()):
                yield new_pos, new_state

    def get_path(preds, end):
        pos, blizzards = end
        path = [(pos, dict(blizzards))]
        pred = preds[end]
        while pred:
            pos, blizzards = pred
            path.append((pos, dict(blizzards)))
            pred = preds[pred]

        return list(reversed(path))

    def bfs(start):
        queue = deque([start])
        preds = {canonical(start): None}
        while queue:
            node = queue.popleft()
            for child in iter_children(node):
                if (candidate := canonical(child)) in preds:
                    continue

                preds[candidate] = canonical(node)
                new_pos, _ = child
                if new_pos == end:
                    return get_path(preds, candidate)

                queue.append(child)

    height, width = dimensions
    return bfs((begin, blizzards))


def main():
    """Main entry."""
    begin, end, dimensions, blizzards = parse('input')
    path = find_path(begin, end, dimensions, blizzards)
    assert len(path) - 1 == 257

    paths = [path]
    paths.append(find_path(end, begin, dimensions, paths[-1][-1][-1]))
    paths.append(find_path(begin, end, dimensions, paths[-1][-1][-1]))
    assert sum(len(path) - 1 for path in paths) == 828


if __name__ == '__main__':
    main()
