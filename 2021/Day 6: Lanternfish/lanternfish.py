"""Day 6: Lanternfish"""


import os
from collections import Counter


INPUT = os.path.join(os.path.dirname(__file__), 'input')


def parse(filename):
    with open(filename, encoding='utf-8') as input_file:
        return (int(number) for number in input_file.read().split(','))


def simulate(data, days, cycle=7, start_timer=8):
    """Simulate lanternfish over specified number of days and return
    number of lanternfish.
    """
    timers = Counter(data)
    for _ in range(days):
        new_timers = Counter()
        for timer, counts in timers.items():
            if timer < cycle:
                new_timer = (timer - 1) % cycle
                new_timers[new_timer] += counts
                if new_timer == cycle - 1:
                    new_timers[start_timer] += counts
            else:
                new_timer = timer - 1
                new_timers[new_timer] += counts

        timers = new_timers

    return sum(timers.values())


def test_part1():
    assert simulate(parse(INPUT), 80) == 388739


def test_part2():
    assert simulate(parse(INPUT), 256) == 1741362314973
