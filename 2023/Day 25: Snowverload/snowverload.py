"""Day 25: Snowverload"""


from collections import defaultdict
from copy import deepcopy
from itertools import combinations
from math import prod


def parse(filename):
    """Parse a wiring diagram into a graph."""
    graph = defaultdict(set)
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            componet, others = line.strip().split(':')
            for other in others.split():
                other = other.strip()
                graph[componet].add(other)
                graph[other].add(componet)

    return graph


def find_paths(graph, start, end):
    """Return the number of paths between two nodes and their edges."""
    count = 0
    edges = set()
    while True:
        preds = {}
        queue = {start}
        while queue:
            node = queue.pop()
            if node == end:
                count += 1
                break

            neighbors = (
                neighbor
                for neighbor in graph[node]
                if (node, neighbor) not in edges
            )
            for neighbor in neighbors:
                if neighbor in preds:
                    continue

                preds[neighbor] = node
                queue.add(neighbor)
        else:
            return count, edges

        curr = node
        while curr != start:
            curr, prev = preds[curr], curr
            edges.add((curr, prev))


def disconnect(components, number):
    """Divide the components into two separate, disconnected groups."""
    graph = deepcopy(components)
    edges = None
    for start, end in combinations(graph, 2):
        count, _edges = find_paths(graph, start, end)
        if count != number:
            continue

        if edges:
            edges &= _edges
        else:
            edges = _edges

        if len(edges) == number:
            break

    for node1, node2 in edges:
        graph[node1].remove(node2)
        graph[node2].remove(node1)

    return _separate_groups(graph)


def _separate_groups(graph):
    """Return two groups of nodes in a graph."""
    start = next(iter(graph))
    visited = set()
    queue = [start]
    while queue:
        node = queue.pop()
        for neighbor in graph[node]:
            if neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append(neighbor)

    return visited, set(graph) - visited


def main():
    """Main program."""
    components = parse('input')
    assert prod(map(len, disconnect(components, 3))) == 583338


if __name__ == '__main__':
    main()
