"""Day 1: Calorie Counting"""


import heapq


def parse(filename):
    """Return an iterator of each elf's items' Calories"""
    with open(filename, 'r', encoding='utf-8') as file_:
        elf = []
        for line in file_:
            if line := line.strip():
                elf.append(int(line))
            else:
                yield elf
                elf = []

    yield elf


def sum_of_top_calories(elves, n_largest):
    """Find the total of Calories from the top Elves carrying the most
    Calories.
    """
    return sum(heapq.nlargest(n_largest, (sum(elf) for elf in elves)))


def main():
    """Main entry."""
    elves = list(parse('input'))
    assert sum_of_top_calories(elves, n_largest=1) == 70374
    assert sum_of_top_calories(elves, n_largest=3) == 204610


if __name__ == '__main__':
    main()
