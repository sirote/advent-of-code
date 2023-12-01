"""Day 1: Trebuchet?!"""


import re
from itertools import chain


def parse(filename):
    """Return an iterator of each elf's items' Calories"""
    with open(filename, 'r', encoding='utf-8') as file_:
        yield from file_


def iter_calibration_values(lines, mapping=None):
    """Return an iterator of the calibration values."""
    return (find_calibration_value(line, mapping) for line in lines)


def find_calibration_value(line, mapping=None):
    """Return the calibration value for a line."""
    forward_mapping = mapping or {}
    backward_mapping = {k[::-1]: v for k, v in forward_mapping.items()}
    first = find_digit(line, forward_mapping)
    last = find_digit(line[::-1], backward_mapping)
    return int(f'{first}{last}')


def find_digit(line, mapping):
    """Return the first digit in a line."""
    if match := re.search('|'.join(chain((r'\d',), mapping)), line):
        value = match.group()
        return str(mapping.get(value, value))

    raise RuntimeError(f'No digit found in {line}')


def main():
    """Main entry."""
    assert sum(iter_calibration_values(parse('input1'))) == 54239
    assert sum(iter_calibration_values(parse('input2'), mapping={
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    })) == 55343


if __name__ == "__main__":
    main()
