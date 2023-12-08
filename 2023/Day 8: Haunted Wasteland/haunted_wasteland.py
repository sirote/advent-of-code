"""Day 8: Haunted Wasteland"""


import math
import re
from itertools import cycle


def parse(filename):
    """Parse map file and return a pair of instructions and network."""
    with open(filename, 'r', encoding='utf-8') as file_:
        instructions = next(file_).strip()
        network = {
            match.group(1): (match.group(2), match.group(3))
            for line in file_
            if (match := re.match(r'(\w+) = \((\w+), (\w+)\)', line))
        }

    return instructions, network


def navigate(instructions, network, start):
    """Iterate over nodes by navigating the network."""
    node = start
    for instruction in cycle(instructions):
        yield node
        node = network[node]['LR'.index(instruction)]


def count_steps(*navigators, ends):
    """Count steps to simultaneously reach the end node for all
    navigators.
    """
    return math.lcm(*(
        next(step for step, node in enumerate(navigator) if ends(node))
        for navigator in navigators
    ))


def main():
    """Main program."""
    instructions, network = parse('input')
    assert count_steps(
        navigate(instructions, network, start='AAA'),
        ends=lambda n: n == 'ZZZ',
    ) == 16343
    assert count_steps(
        *(
            navigate(instructions, network, start=start)
            for start in (node for node in network if node.endswith('A'))
        ),
        ends=lambda n: n.endswith('Z'),
    ) == 15299095336639


if __name__ == '__main__':
    main()
