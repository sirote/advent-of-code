"""Day 23: Unstable Diffusion"""


import math
from collections import defaultdict
from itertools import chain, cycle, islice


N, S, W, E = range(4)


def parse(filename):
    """Return a list Elf's positions."""
    with open(filename, 'r', encoding='utf-8') as file_:
        return [
            (i, j)
            for i, line in enumerate(file_)
            for j, tile in enumerate(line.rstrip())
            if tile == '#'
        ]


def simulate(positions):
    """Simulate the Elf's time-consuming process."""
    def get_neighbors(pos):
        p_x, p_y = pos
        return {
            (n_x, n_y)
            for i, j in (
                (-1, -1), (-1, 0), (-1, 1),
                (1, 1), (1, 0), (1, -1),
                (0, -1), (0, 1),
            )
            if (n_x := p_x + i, n_y := p_y + j) in positions
        }

    def get_proposal(pos, neighbors, dir_):
        p_x, p_y = pos
        for k in chain(directions[dir_:], directions[:dir_]):
            if all((p_x + i, p_y + j) not in neighbors for i, j in moves[k]):
                m_x, m_y = moves[k][1]
                return p_x + m_x, p_y + m_y

        return pos

    def get_positions(proposals):
        positions = set()
        for proposal, elves in proposals.items():
            if len(elves) == 1:
                positions.add(proposal)
            else:
                positions.update(elves)

        return positions

    moves = {
        N: ((-1, -1), (-1, 0), (-1, 1)),
        S: ((1, -1), (1, 0), (1, 1)),
        W: ((-1, -1), (0, -1), (1, -1)),
        E: ((-1, 1), (0, 1), (1, 1)),
    }
    directions = list(moves.keys())
    positions = set(positions)

    for direction in cycle(directions):
        proposals = defaultdict(list)
        for pos in positions:
            if not (neighbors := get_neighbors(pos)):
                proposals[pos].append(pos)
                continue

            proposal = get_proposal(pos, neighbors, direction)
            proposals[proposal].append(pos)

        positions = get_positions(proposals)
        yield positions


def count_empty_ground(positions):
    """Return the number of empty ground tiles that the smallest
    rectangle contains.
    """
    min_x = min_y = math.inf
    max_x = max_y = -math.inf
    for p_x, p_y in positions:
        min_x = min(min_x, p_x)
        min_y = min(min_y, p_y)
        max_x = max(max_x, p_x)
        max_y = max(max_y, p_y)

    return sum(
        (i, j) not in positions
        for i in range(min_x, max_x + 1)
        for j in range(min_y, max_y + 1)
    )


def find_end_round(positions):
    """Return the number of the first round where no Elf moves."""
    prev = None
    for round_, next_ in enumerate(simulate(positions), start=1):
        if next_ == prev:
            return round_
        prev = next_
    return math.inf


def main():
    """Main entry."""
    positions = parse('input')
    assert count_empty_ground(next(islice(simulate(positions), 9, 10))) == 3990
    assert find_end_round(positions) == 1057


if __name__ == '__main__':
    main()
