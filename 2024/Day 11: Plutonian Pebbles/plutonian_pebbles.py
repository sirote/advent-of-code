"""Day 11: Plutonian Pebbles"""


from functools import cache


def parse(filename):
    """Read the input file and return a list of the numbers engraved on
    the stones.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip().split(' ')


@cache
def count(stone, blinks):
    """Return the number of stones after blinking the given number of
    times.
    """
    if blinks == 0:
        return 1

    if stone == '0':
        return count('1', blinks - 1)

    if len(stone) % 2 == 0:
        offset = len(stone) // 2
        return (
            count(stone[:offset], blinks - 1)
            + count(str(int(stone[offset:])), blinks - 1)
        )

    return count(str(int(stone) * 2024), blinks - 1)


def test_example():
    """Test the example."""
    stones = parse('example.txt')
    assert sum(count(stone, 25) for stone in stones) == 55312


def test_puzzle():
    """Test the puzzle."""
    stones = parse('input.txt')
    assert sum(count(stone, 25) for stone in stones) == 202019
    assert sum(count(stone, 75) for stone in stones) == 239321955280205
