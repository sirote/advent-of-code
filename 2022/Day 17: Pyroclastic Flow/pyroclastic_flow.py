"""Day 17: Pyroclastic Flow"""


from itertools import cycle


SYMBOL_TO_SHAPE = {
    '-': lambda h: (
        (3, h + 4),
        (4, h + 4),
        (5, h + 4),
        (6, h + 4),
    ),
    '+': lambda h: (
        (3, h + 5),
        (4, h + 4),
        (4, h + 5),
        (4, h + 6),
        (5, h + 5),
    ),
    'j': lambda h: (
        (3, h + 4),
        (4, h + 4),
        (5, h + 4),
        (5, h + 5),
        (5, h + 6),
    ),
    'l': lambda h: (
        (3, h + 4),
        (3, h + 5),
        (3, h + 6),
        (3, h + 7),
    ),
    'o': lambda h: (
        (3, h + 4),
        (3, h + 5),
        (4, h + 4),
        (4, h + 5),
    ),
}


def parse(filename):
    """Return an iterable of jet patterns."""
    with open(filename, 'r', encoding='utf-8') as file_:
        yield from file_.read().rstrip()


def rock_factory():
    """Return a function to create falling rocks."""
    symbols = cycle(SYMBOL_TO_SHAPE.keys())

    def create_rock(height):
        return SYMBOL_TO_SHAPE[next(symbols)](height)

    return create_rock


def find_repetition(data):
    """Return a tuple of indices of the first and second rows that are
    the beginning of repetition.
    """
    num_types = len(SYMBOL_TO_SHAPE)
    num_rows = len(data)
    top_row = [h - data[-1][0] for h in data[-1]]

    for j in range(num_rows - num_types - 1, num_rows // 2, -num_types):
        i = 2 * j - num_rows + 1
        middle_row = [h - data[j][0] for h in data[j]]
        bottom_row = [h - data[i][0] for h in data[i]]

        if top_row != middle_row or top_row != bottom_row:
            continue

        rep1 = (
            [b - a for a, b in zip(data[i], item)]
            for item in data[i + 1: j]
        )

        rep2 = (
            [b - a for a, b in zip(data[j], item)]
            for item in data[j + 1: num_rows - 1]
        )

        if all(r1 == r2 for r1, r2 in zip(rep1, rep2)):
            return i, j

    return None


def calculate_height(first, second, heights, remaining_rocks):
    """Calculate the tower height using repetition data."""
    repeat_height = max(heights[second]) - max(heights[first])
    divisor = second - first
    num_rocks = remaining_rocks + 1
    return (
        (num_rocks // divisor + 2) * repeat_height
        + max(heights[first + num_rocks % divisor - 1])
    )


def simulate(jet_patterns, num_rocks):
    """Simulate falling rocks and return the height after `num_rocks`
    rocks have stopped falling.
    """
    moves = {
        '>': lambda rock: tuple((i + 1, j) for i, j in rock),
        '<': lambda rock: tuple((i - 1, j) for i, j in rock),
        'V': lambda rock: tuple((i, j - 1) for i, j in rock),
    }
    width = 7
    heights = [0] * width
    chamber = set((i, 0) for i in range(1, 8))
    create_rock = rock_factory()
    jet_patterns = cycle(jet_patterns)
    history = []

    while num_rocks:
        history.append(tuple(heights))
        if repetition := find_repetition(history):
            return calculate_height(*repetition, history, num_rocks)

        rock = create_rock(max(heights))

        for jet_pattern in jet_patterns:
            moved_rock = moves[jet_pattern](rock)
            if (not (set(moved_rock) & chamber)
                    and moved_rock[0][0] > 0
                    and moved_rock[-1][0] <= width):
                rock = moved_rock

            moved_rock = moves['V'](rock)
            if (not (set(moved_rock) & chamber)
                    and min(j for _, j in moved_rock) > 0):
                rock = moved_rock
            else:
                chamber.update(rock)
                num_rocks -= 1
                for i, j in rock:
                    heights[i - 1] = max(heights[i - 1], j)
                break

    return max(heights)


def main():
    """Main entry."""
    jet_patterns = list(parse('input'))
    assert simulate(jet_patterns, num_rocks=2022) == 3186
    assert simulate(jet_patterns, num_rocks=1000000000000) == 1566376811584


if __name__ == '__main__':
    main()
