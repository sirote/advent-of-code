"""Day 11: Monkey in the Middle"""


import heapq
import math
import re
from collections import deque
from itertools import islice, takewhile


def parse(filename):
    """Return an iterable of monkey id and object pairs."""
    with open(filename, 'r', encoding='utf-8') as file_:
        while (monkey := _parse(takewhile(lambda line: line.rstrip(), file_))):
            yield monkey


def _parse(lines):
    if not (lines := list(lines)):
        return None

    def __init__(self, items, divisor):
        self.count = 0
        self.items = deque(items)
        self.divisor = divisor

    monkey_id = re.search(r'\d+', lines[0]).group()
    items = _parse_items(lines[1])
    divisor = int(re.search(r'\d+', lines[3]).group())

    return monkey_id, type(
        'Monkey',
        (),
        dict(
            __init__=__init__,
            inspect=_parse_operation(lines[2]),
            test=_parse_test(lines[4:]),
        )
    )(items=items, divisor=divisor)


def _parse_items(line):
    return (int(item) for item in re.findall(r'\d+', line))


def _parse_operation(line):
    operator, value = re.search(r'new = old (.) (\w+)', line).groups()
    if operator == '+' and value == 'old':
        return lambda _, x: x + x

    if operator == '*' and value == 'old':
        return lambda _, x: x * x

    number = int(value)
    if operator == '+':
        return lambda _, x: x + number

    if operator == '*':
        return lambda _, x: x * number

    raise RuntimeError(f'Unknown operator: {operator}')


def _parse_test(lines):
    true_monkey = false_monkey = None
    for line in lines:
        monkey_id = re.search(r'\d+', line).group()
        line = line.lstrip()
        if line.startswith('If true:'):
            true_monkey = monkey_id
        elif line.startswith('If false:'):
            false_monkey = monkey_id

    return (
        lambda self, value:
        true_monkey if value % self.divisor == 0 else false_monkey
    )


def play(id_to_monkey, adjust_worry_level, rounds):
    """Play Monkey in the Middle."""
    iterable = _play(id_to_monkey, adjust_worry_level)
    num_inspects = next(islice(iterable, rounds - 1, rounds))
    return math.prod(heapq.nlargest(2, num_inspects))


def _play(id_to_monkey, adjust_worry_level):
    while True:
        for monkey in id_to_monkey.values():
            while items := monkey.items:
                item = items.popleft()
                monkey.count += 1
                worry_level = adjust_worry_level(monkey.inspect(item))
                monkey_id = monkey.test(worry_level)
                id_to_monkey[monkey_id].items.append(worry_level)

        yield [monkey.count for monkey in id_to_monkey.values()]


def relief(worry_level):
    """Return new worry level after relief."""
    return worry_level // 3


def get_adjust_func(monkeys):
    """Return a worry-level adjustment function."""
    lcm = math.lcm(*(monkey.divisor for monkey in monkeys))
    return lambda worry_level: worry_level % lcm


def main():
    """Main entry."""
    id_to_monkey = dict(parse('input'))
    assert play(id_to_monkey, relief, rounds=20) == 151312

    id_to_monkey = dict(parse('input'))
    adjust_worry_level = get_adjust_func(id_to_monkey.values())
    assert play(id_to_monkey, adjust_worry_level, rounds=10000) == 51382025916


if __name__ == '__main__':
    main()
