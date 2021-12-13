"""Day 13: Transparent Origami"""


import os


INPUT = os.path.join(os.path.dirname(__file__), 'input')


class TransparentOrigami:

    def __init__(self, coordinates):
        self.coordinates = set(coordinates)

    def __str__(self):
        max_x = max(x for x, _ in self.coordinates)
        max_y = max(y for _, y in self.coordinates)

        return '\n'.join(
            ''.join(
                '#' if (i, j) in self.coordinates else '.'
                for i in range(max_x + 1)
            )
            for j in range(max_y + 1)
        )

    def __len__(self):
        return len(self.coordinates)

    def fold(self, axis, value):
        if axis == 'x':
            self.fold_left(value)
        elif axis == 'y':
            self.fold_up(value)

    def fold_up(self, value):
        self.coordinates = {
            (x, y if y < value else 2 * value - y)
            for x, y in self.coordinates
        }

    def fold_left(self, value):
        self.coordinates = {
            (x if x < value else 2 * value - x, y)
            for x, y in self.coordinates
        }


def parse(filename):
    with open(filename, encoding='utf-8') as input_file:
        coordinates = []
        for line in input_file:
            if not line.strip():
                break

            coordinates.append(tuple(int(n) for n in line.split(',')))

        fold_instructions = []
        for line in input_file:
            axis, value = line.split('=')
            fold_instructions.append((axis[-1], int(value)))

        return coordinates, fold_instructions


def test_part1():
    coordinates, fold_instructions = parse(INPUT)
    origami = TransparentOrigami(coordinates)
    origami.fold(*fold_instructions[0])
    assert len(origami) == 735


def test_part2():
    coordinates, fold_instructions = parse(INPUT)
    origami = TransparentOrigami(coordinates)
    for instruction in fold_instructions:
        origami.fold(*instruction)

    assert str(origami) == (
        '#..#.####.###..####.#..#..##..#..#.####\n'
        '#..#.#....#..#....#.#.#..#..#.#..#....#\n'
        '#..#.###..#..#...#..##...#..#.#..#...#.\n'
        '#..#.#....###...#...#.#..####.#..#..#..\n'
        '#..#.#....#.#..#....#.#..#..#.#..#.#...\n'
        '.##..#....#..#.####.#..#.#..#..##..####'
    )
