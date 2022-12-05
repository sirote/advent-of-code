"""Day 5: Supply Stacks"""


import copy
import re
from collections import namedtuple
from itertools import takewhile


Step = namedtuple('Step', ['move', 'from_', 'to'])


def parse(filename):
    """Return a dict of stacks and a list of procedure."""
    with open(filename, 'r', encoding='utf-8') as file_:
        return _parse_stacks(file_), _parse_procedure(file_)


def _parse_stacks(file_):
    lines = list(takewhile(lambda line: line.strip(), file_))
    indices = [
        index
        for index, char in enumerate(lines.pop())
        if char.isdigit()
    ]
    stacks = [[] for _ in indices]

    for line in reversed(lines):
        for i, index in enumerate(indices):
            if (crate := line[index]) != ' ':
                stacks[i].append(crate)

    return stacks


def _parse_procedure(file_):
    return [
        Step._make(int(n) for n in re.findall(r'\d+', step))
        for line in file_
        if (step := line.strip())
    ]


def get_tos(stacks):
    """Return crate on top of each stack."""
    return ''.join(stack[-1] for stack in stacks)


def rearrange_9000(stacks, procedure):
    """Rrearrange stacks of crates with CrateMover 9000."""
    stacks = copy.deepcopy(stacks)
    for step in procedure:
        for _ in range(step.move):
            stacks[step.to - 1].append(stacks[step.from_ - 1].pop())
    return stacks


def rearrange_9001(stacks, procedure):
    """Rrearrange stacks of crates with CrateMover 9001."""
    stacks = copy.deepcopy(stacks)
    for step in procedure:
        stacks[step.to - 1].extend(stacks[step.from_ - 1][-step.move:])
        del stacks[step.from_ - 1][-step.move:]
    return stacks


def main():
    """Entry point"""
    stacks, procedure = parse('input')
    assert get_tos(rearrange_9000(stacks, procedure)) == 'FJSRQCFTN'
    assert get_tos(rearrange_9001(stacks, procedure)) == 'CJVLJQPHS'


if __name__ == '__main__':
    main()
