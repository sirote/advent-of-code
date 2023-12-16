"""Day 14: Parabolic Reflector Dish"""


from itertools import groupby


DIRECTIONS = {
    'N': (-1, 0),
    'W': (0, -1),
    'S': (1, 0),
    'E': (0, 1),
}

SORT_KEYS = {
    'N': lambda r: r[0],
    'W': lambda r: r[1],
    'S': lambda r: -r[0],
    'E': lambda r: -r[1],
}


def parse(filename):
    """Parse the input file containing the dish layout."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield line.strip()


class ParabolicReflectorDish:
    """Parabolic reflector dish."""

    def __init__(self, dish):
        self.rounds, self.cubes, self.size = self._parse_dish(dish)

    def tilt(self, direction):
        """Tilt the dish in a given direction."""
        new_rounds = set()
        i, j = DIRECTIONS[direction]
        key = SORT_KEYS[direction]
        for _, row in groupby(sorted(self.rounds, key=key), key=key):
            for x, y in row:
                while True:
                    point = x + i, y + j
                    if (self._out_of_bounds(point)
                            or point in self.cubes
                            or point in new_rounds):
                        new_rounds.add((x, y))
                        break

                    x, y = point

        self.rounds = new_rounds
        return self

    def spin_cycle(self):
        """Tilt the dish in all directions from north to east."""
        for direction in 'NWSE':
            self.tilt(direction)
        return self

    def total_load(self):
        """Get the load on the north support beams."""
        return sum(self.size[0] - x for x, _ in self.rounds)

    def _out_of_bounds(self, point):
        height, width = self.size
        x, y = point
        return x < 0 or x >= height or y < 0 or y >= width

    @staticmethod
    def _parse_dish(dish):
        cubes = set()
        rounds = set()
        for i, row in enumerate(dish):
            for j, char in enumerate(row):
                if char == 'O':
                    rounds.add((i, j))
                elif char == '#':
                    cubes.add((i, j))

        return rounds, cubes, (len(dish), len(dish[0]))


def total_load(dish, cycles):
    """Get the total load on the north support beams after running the
    spin cycle for a given number of cycles.
    """
    results = []
    for _ in range(cycles):
        results.append(dish.spin_cycle().rounds)
        if pairs := find_repeat(results):
            i, j = pairs
            index = (cycles - i - 1) % (j - i + 1) + i
            dish.rounds = results[index]
            return dish.total_load()

    return dish.total_load()


def find_repeat(results):
    """Find the first repeated result."""
    last = results[-1]
    for i in range(len(results) - 2, len(results) // 2, -1):
        if last == results[i]:
            j = len(results) - 1
            k = i
            while results[j] == results[k]:
                j -= 1
                if j == i:
                    return k, j
                k -= 1

            break

    return None


def main():
    """Main program."""
    raw_dish = list(parse('input'))
    assert ParabolicReflectorDish(raw_dish).tilt('N').total_load() == 110090
    assert total_load(ParabolicReflectorDish(raw_dish), cycles=10**9) == 95254


if __name__ == '__main__':
    main()
