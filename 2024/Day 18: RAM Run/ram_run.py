"""Day 18: RAM Run"""


from collections import deque


def parse(filename):
    """Parse the input file and return a list of tuples representing a
    list of bytes.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return [tuple(map(int, line.split(','))) for line in f]


def simulate(byte_positions, end):
    """Simulate the falling bytes onto the memory space and return the
    minimum number of steps needed to reach the exit.
    """
    bytes_ = set(byte_positions)
    queue = deque([((0, 0), 0)])
    visited = set()

    while queue:
        pos, steps = queue.popleft()
        if pos == end:
            return steps

        if pos in visited:
            continue

        visited.add(pos)

        x, y = pos
        for m, n in (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1):
            if m < 0 or n < 0 or m > end[0] or n > end[1]:
                continue

            if (m, n) in bytes_:
                continue

            queue.append(((m, n), steps + 1))

    return None


def search_byte(bytes_, end):
    """Search for the first byte that is blocking the exit and return
    it.
    """
    lo = 0
    mid = len(bytes_) // 2
    hi = len(bytes_)

    while lo != mid:
        if simulate(bytes_[:mid], end) is None:
            hi = mid
            mid = (lo + mid) // 2
        else:
            lo = mid
            mid = (mid + hi) // 2

    return bytes_[mid]


def test_example():
    """Test the example."""
    bytes_ = parse('example.txt')
    assert simulate(bytes_[:12], (6, 6)) == 22
    assert search_byte(bytes_, (6, 6)) == (6, 1)


def test_puzzle():
    """Test the puzzle."""
    bytes_ = parse('input.txt')
    assert simulate(bytes_[:1024], (70, 70)) == 344
    assert search_byte(bytes_, (70, 70)) == (46, 18)
