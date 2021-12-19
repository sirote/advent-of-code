"""Day 18: Snailfish"""


from copy import deepcopy
from itertools import combinations, zip_longest, tee
from pathlib import Path
from typing import NamedTuple, Union


PATH = Path(__file__).parent


LEFT = 0
RIGHT = 1

SPLIT_POINT = 10
EXPLODE_DEPTH = 4


class Node(NamedTuple):

    depth: int
    parent: list
    value: Union[int, list]
    side: int

    def is_root(self):
        return self.parent[RIGHT] is None

    def is_pair(self):
        return isinstance(self.value, list)

    def is_left(self):
        return self.side == LEFT

    def is_right(self):
        return self.side == RIGHT

    def update(self, new_value):
        self.parent[self.side] = new_value


class Number:

    def __init__(self, number):
        self.number = self._reduce(deepcopy(number))

    def __repr__(self):
        return self.number.__repr__()

    def __eq__(self, other):
        return self.number == other.number

    def __add__(self, other):
        return Number(self._reduce([self.number, other.number]))

    def __radd__(self, other):
        if other == 0:
            return self
        return Number(self._reduce([other.number, self.number]))

    @property
    def magnitude(self):
        while True:
            for _, node, _ in self._traverse(self.number):
                if node.is_pair():
                    left, right = node.value
                    value = 3 * left + 2 * right
                    if node.is_root():
                        return value
                    node.update(value)

        return 0

    def _reduce(self, number):
        while True:
            if self._explode(number) or self._split(number):
                continue
            break

        return number

    def _explode(self, number):
        for prev, curr, next_ in self._traverse(number):
            if curr.depth == EXPLODE_DEPTH and curr.is_pair():
                curr.update(0)
                if curr.is_right():
                    self._add_to_parent(curr, LEFT)
                    if next_:
                        self._add_to_side(next_, curr.value[RIGHT], LEFT)
                else:
                    self._add_to_parent(curr, RIGHT)
                    if prev:
                        self._add_to_side(prev, curr.value[LEFT], RIGHT)
                break
        else:
            return False
        return True

    def _add_to_parent(self, node, side):
        value = node.value[side]
        if isinstance(pair := node.parent[side], int):
            node.parent[side] += value
        else:
            node = next(self._dfs(pair, reverse=node.is_left()))
            node.parent[1 - side] += value

    @staticmethod
    def _add_to_side(node, value, side):
        if node.is_pair():
            node.value[side] += value
        else:
            node.update(node.value + value)

    def _split(self, number):
        for node in self._dfs(number):
            if node.value >= SPLIT_POINT:
                node.update([split := node.value // 2, node.value - split])
                break
        else:
            return False
        return True

    @classmethod
    def _traverse(cls, number):
        def is_leaf(node):
            return (
                isinstance(node, int)
                or isinstance(node[LEFT], int)
                and isinstance(node[RIGHT], int)
            )

        first, second = tee(cls._dfs(number, is_leaf=is_leaf))
        next(second, None)
        prev = None
        for curr, next_ in zip_longest(first, second):
            yield prev, curr, next_
            prev = curr

    @staticmethod
    def _dfs(number, reverse=False, is_leaf=None):
        is_leaf = is_leaf or (lambda node: isinstance(node, int))
        queue = [(depth := 0, [number, None], LEFT)]
        while queue:
            depth, parent, side = queue.pop()
            node = parent[side]
            if is_leaf(node):
                yield Node(depth, parent, node, side)
            else:
                depth += 1
                if reverse:
                    queue.append((depth, node, LEFT))
                    queue.append((depth, node, RIGHT))
                else:
                    queue.append((depth, node, RIGHT))
                    queue.append((depth, node, LEFT))


def parse(path):
    with path.open(encoding='utf-8') as input_file:
        for line in input_file:
            yield eval(line)


def test_explode_with_no_regular_number_to_its_left():
    number = Number([[[[[9, 8], 1], 2], 3], 4])
    assert number == Number([[[[0, 9], 2], 3], 4])


def test_explode_with_no_regular_number_to_its_right():
    number = Number([7, [6, [5, [4, [3, 2]]]]])
    assert number == Number([7, [6, [5, [7, 0]]]])


def test_explode():
    number = Number([[6, [5, [4, [3, 2]]]], 1])
    assert number == Number([[6, [5, [7, 0]]], 3])


def test_explode_twice():
    number = Number([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    assert number == Number([[3, [2, [8, 0]]], [9, [5, [7, 0]]]])


def test_addition():
    number = sum((Number(n) for n in parse(PATH / 'example1')))
    assert number == Number([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])


def test_four_additions():
    number = sum((Number(n) for n in parse(PATH / 'example2')))
    assert number == Number([[[[1, 1], [2, 2]], [3, 3]], [4, 4]])


def test_five_additions():
    number = sum((Number(n) for n in parse(PATH / 'example3')))
    assert number == Number([[[[3, 0], [5, 3]], [4, 4]], [5, 5]])


def test_six_additions():
    number = sum((Number(n) for n in parse(PATH / 'example4')))
    assert number == Number([[[[5, 0], [7, 4]], [5, 5]], [6, 6]])


def test_example():
    number = sum((Number(n) for n in parse(PATH / 'example5')))
    assert number == Number([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]])


def test_magnitude():
    assert Number([[1, 2], [[3, 4], 5]]).magnitude == 143
    assert Number([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]).magnitude == 1384
    assert Number([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]).magnitude == 445
    assert Number([[[[3, 0], [5 ,3]], [4, 4]], [5, 5]]).magnitude == 791
    assert Number([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]).magnitude == 1137
    assert Number([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]).magnitude == 3488


def test_final_example():
    number = sum((Number(n) for n in parse(PATH / 'example6')))
    assert number == Number([[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]])
    assert number.magnitude == 4140


def test_final_example_largest_magnitude():
    assert max(
        max(
            sum((Number(a), Number(b))).magnitude,
            sum((Number(b), Number(a))).magnitude,
        )
        for a, b in combinations(parse(PATH / 'example6'), r=2)
    ) == 3993


def test_part1():
    number = sum((Number(n) for n in parse(PATH / 'input')))
    assert number.magnitude == 3734


def test_part2():
    assert max(
        max(
            sum((Number(a), Number(b))).magnitude,
            sum((Number(b), Number(a))).magnitude,
        )
        for a, b in combinations(parse(PATH / 'input'), r=2)
    ) == 4837
