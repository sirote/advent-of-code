"""Day 25: Sea Cucumber"""


from pathlib import Path


PATH = Path(__file__).parent

EAST = '>'
SOUTH = 'v'
EMPTY = '.'


class SeaCucumber:

    def __init__(self, data):
        self._data = data
        self._iterator = iter(self)
        self.steps = 0

    def __repr__(self):
        return '\n'.join(''.join(row) for row in self._data)

    def __iter__(self):
        while True:
            data = []
            south_herd = []
            for i, row in enumerate(self._data):
                data.append(['.'] * len(row))
                for j, char in enumerate(row):
                    if char == EAST:
                        k = (j + 1) % len(row)
                        if self._data[i][k] == EMPTY:
                            data[i][j] = EMPTY
                            data[i][k] = EAST
                        else:
                            data[i][j] = EAST
                    elif char == SOUTH:
                        south_herd.append((i, j))
                        data[i][j] = SOUTH

            moves = [
                (i, j, k)
                for i, j in south_herd
                if data[k := (i + 1) % len(data)][j] == EMPTY
            ]

            for i, j, k in moves:
                data[i][j] = EMPTY
                data[k][j] = SOUTH

            self.steps += 1
            if self._data == data:
                return

            self._data = data
            yield self

    def __next__(self):
        return next(self._iterator)


def parse(path):
    with path.open(encoding='utf-8') as input_file:
        return [list(line.rstrip()) for line in input_file]


def test_example1():
    sea_cucumber = SeaCucumber(parse(PATH / 'example1'))
    for _ in range(2):
        next(sea_cucumber)
    assert str(sea_cucumber) == '...>>>.>.>.'


def test_example2():
    sea_cucumber = SeaCucumber(parse(PATH / 'example2'))
    for _ in range(1):
        next(sea_cucumber)
    assert str(sea_cucumber) == (
        '..........\n'
        '.>........\n'
        '..v....v>.\n'
        '..........'
    )


def test_example3():
    sea_cucumber = SeaCucumber(parse(PATH / 'example3'))
    for _ in range(4):
        next(sea_cucumber)
    assert str(sea_cucumber) == (
        '>......\n'
        '..v....\n'
        '..>.v..\n'
        '.>.v...\n'
        '...>...\n'
        '.......\n'
        'v......'
    )


def test_example4():
    sea_cucumber = SeaCucumber(parse(PATH / 'example4'))
    for _ in sea_cucumber:
        pass
    assert sea_cucumber.steps == 58


def test_input():
    sea_cucumber = SeaCucumber(parse(PATH / 'input'))
    for _ in sea_cucumber:
        pass
    assert sea_cucumber.steps == 441
