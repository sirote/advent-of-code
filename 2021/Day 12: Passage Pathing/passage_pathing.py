"""Day 12: Passage Pathing"""


import os
from collections import defaultdict


INPUT = os.path.join(os.path.dirname(__file__), 'input')


class PassagePathing:

    def __init__(self, filename):
        self.filename = filename

    def find_all(self, should_visit=None, start='start', end='end'):
        """Return a list of distinct paths that start at `start`, end at
        `end`.
        """
        should_visit = should_visit or (lambda node, path: node not in path)
        return self._find_all(self._parse(), start, end, should_visit)

    def _find_all(self, graph, start, end, should_visit, path=()):
        path = path + (start,)
        if start == end:
            return [path]

        return [
            new_path
            for node in graph[start] if should_visit(node, path)
            for new_path in self._find_all(
                graph, node, end, should_visit, path
            )
        ]

    def _parse(self):
        graph = defaultdict(list)
        with open(self.filename, encoding='utf-8') as input_file:
            for line in input_file:
                cave1, cave2 = line.rstrip().split('-')
                if cave1 == 'end' or cave2 == 'start':
                    cave1, cave2 = cave2, cave1

                graph[cave1].append(cave2)
                if cave1 != 'start' and cave2 != 'end':
                    if cave1.isupper() and cave2.isupper():
                        raise ValueError(f'Invalid line: {line}')
                    graph[cave2].append(cave1)

        return graph


def test_part1():
    def should_visit(cave, path):
        return cave.isupper() or cave not in path

    assert len(PassagePathing(INPUT).find_all(should_visit)) == 3369


def test_part2():
    def should_visit(cave, path):
        return (
            cave.isupper()
            or cave not in path
            or visit_small_cave_once(path)
        )

    def visit_small_cave_once(path):
        visited = set()
        for cave in path:
            if cave.isupper():
                continue
            if cave in visited:
                return False
            visited.add(cave)
        return True

    assert len(PassagePathing(INPUT).find_all(should_visit)) == 85883
