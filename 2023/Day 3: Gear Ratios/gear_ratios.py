"""Day 3: Gear Ratios"""


def parse(filename):
    """Parse the engine schematic into a list of lines."""
    with open(filename, 'r', encoding='utf-8') as file_:
        return [line.strip() for line in file_]


def iter_part_numbers(engine_schematic):
    """Iterate over the part numbers."""
    lines = add_border(engine_schematic)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char not in '0123456789.':
                yield from iter_numbers(lines, i, j)


def iter_gear_ratio(engine_schematic):
    """Iterate over the gear ratios."""
    lines = add_border(engine_schematic)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '*':
                numbers = list(iter_numbers(lines, i, j))
                if len(numbers) == 2:
                    yield numbers[0] * numbers[1]


def iter_numbers(engine_schematic, row, col):
    """Iterate over the numbers adjacent to a symbol at the given
    row and column.
    """
    positions = set()
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if not engine_schematic[i][j].isdigit():
                continue

            while engine_schematic[i][j - 1].isdigit():
                j -= 1

            positions.add((i, j))

    for i, j in positions:
        digits = []
        while engine_schematic[i][j].isdigit():
            digits.append(engine_schematic[i][j])
            j += 1

        yield int(''.join(digits))


def add_border(engine_schematic):
    """Add a border to the engine schematic."""
    width = len(engine_schematic[0]) + 2
    return [
        '.' * width,
        *(f'.{line}.' for line in engine_schematic),
        '.' * width
    ]


def main():
    """Main program."""
    engine_schematic = parse('input')
    assert sum(iter_part_numbers(engine_schematic)) == 525119
    assert sum(iter_gear_ratio(engine_schematic)) == 76504829


if __name__ == '__main__':
    main()
