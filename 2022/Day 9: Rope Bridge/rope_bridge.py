"""Day 9: Rope Bridge"""


def parse(filename):
    """Return an iterable of direction-moves pairs."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            direction, moves = line.rstrip().split()
            yield direction, int(moves)


def track_tail(motions, knots):
    """Retrun an iterable of positions of the tail."""
    directions = {
        'R': lambda x, y: (x, y + 1),
        'L': lambda x, y: (x, y - 1),
        'U': lambda x, y: (x - 1, y),
        'D': lambda x, y: (x + 1, y),
    }
    for direction, moves in motions:
        for _ in range(moves):
            h_pos, *tails = knots
            knots = [h_pos := directions[direction](*h_pos)]
            for t_pos in tails:
                h_pos = _move_tail(h_pos, t_pos)
                knots.append(h_pos)
            yield h_pos


def _move_tail(h_pos, t_pos):
    h_x, h_y = h_pos
    t_x, t_y = t_pos
    d_x = d_y = 0

    if abs(h_x - t_x) > 1 or abs(h_y - t_y) > 1:
        d_x = (h_x > t_x) - (h_x < t_x)
        d_y = (h_y > t_y) - (h_y < t_y)

    return t_x + d_x, t_y + d_y


def main():
    """Entry point"""
    motions = list(parse('input'))
    assert len(set(track_tail(motions, [(0, 0)] * 2))) == 6011
    assert len(set(track_tail(motions, [(0, 0)] * 10))) == 2419


if __name__ == '__main__':
    main()
