"""Day 10: Cathode-Ray Tube"""


def parse(filename):
    """Return an iterable of opcode-value pairs."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            opcode, _, value = line.rstrip().partition(' ')
            yield opcode, int(value) if value else None


def run(instructions):
    """Return an iterable of register value in each cycle."""
    register = 1
    for opcode, number in instructions:
        if opcode == 'addx':
            yield register
            yield register
            register += number
        else:   # noop
            yield register


def signal_strength(instructions):
    """Compute signal strength."""
    return sum(
        cycle * value
        for cycle, value in enumerate(run(instructions), start=1)
        if cycle % 40 == 20
    )


def draw(instructions):
    """Draw pixels on the CRT screen."""
    width, height = 40, 6
    pixels = {
        pos
        for pos, value in enumerate(run(instructions))
        if abs(value - pos % width) <= 1
    }
    for i in range(height):
        yield ''.join(
            '#' if j + i * width in pixels else '.'
            for j in range(width)
        )


def main():
    """Main entry."""
    instructions = list(parse('input'))
    assert signal_strength(instructions) == 13920
    assert list(draw(instructions)) == [
        '####..##..#....#..#.###..#....####...##.',
        '#....#..#.#....#..#.#..#.#....#.......#.',
        '###..#....#....####.###..#....###.....#.',
        '#....#.##.#....#..#.#..#.#....#.......#.',
        '#....#..#.#....#..#.#..#.#....#....#..#.',
        '####..###.####.#..#.###..####.#.....##..',
    ]


if __name__ == '__main__':
    main()
