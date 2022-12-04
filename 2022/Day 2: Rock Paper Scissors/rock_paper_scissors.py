"""Day 2: Rock Paper Scissors."""


DRAW, WIN, LOSE = range(3)
OUTCOME_SCORES = {
    DRAW: 3,
    WIN: 6,
    LOSE: 0,
}
SHAPE_SCORES = {
    'A': 1,
    'B': 2,
    'C': 3,
}


def parse(filename):
    """Parse the strategy guide."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield line.strip().split()


def win(shape):
    """Return the shape that wins the given shape."""
    return _get_shape(shape, offset=1)


def draw(shape):
    """Return the shape that gives a draw to the given shape."""
    return shape


def lose(shape):
    """Return the shape that lose to the given shape."""
    return _get_shape(shape, offset=-1)


def _get_shape(shape, offset):
    return chr(ord('A') + (ord(shape) - ord('A') + offset) % 3)


def calculate_score(rounds):
    """Return the sum of scores for each round."""
    return sum(
        OUTCOME_SCORES[(ord(you) - ord(opponent)) % 3]
        + SHAPE_SCORES[you]
        for opponent, you in rounds
    )


def score(rounds, guide):
    """Return total score using the given strategy guide."""
    return calculate_score(
        (opponent, guide[you](opponent))
        for opponent, you in rounds
    )


def main():
    """Main entry."""
    rounds = list(parse('input'))

    guide1 = {'X': lambda _: 'A', 'Y': lambda _: 'B', 'Z': lambda _: 'C'}
    assert score(rounds, guide1) == 11449

    guide2 = {'X': lose, 'Y': draw, 'Z': win}
    assert score(rounds, guide2) == 13187


if __name__ == '__main__':
    main()
