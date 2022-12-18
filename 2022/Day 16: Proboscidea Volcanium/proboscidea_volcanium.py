"""Day 16: Proboscidea Volcanium"""


from collections import deque
from functools import cache
from itertools import combinations


def parse(filename):
    """Return a dict of valve/neighbor-valves pairs and a dict of
    valve/flow rate pairs.
    """
    graph = {}
    rates = {}
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            words = line.split()
            valve = words[1]
            rate = int(words[4].split('=')[-1][:-1])
            to_valves = [v.strip(',') for v in words[9:]]
            graph[valve] = to_valves
            rates[valve] = rate

    return graph, rates


def bfs(graph, start, ends):
    """Return a dict of predecessors as a result of running
    breadth-first search to find shortest path from the start to all
    ends.
    """
    preds = {start: None}
    ends = set(ends)
    queue = deque([start])

    while ends:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor in preds:
                continue

            preds[neighbor] = node
            ends.discard(neighbor)
            queue.append(neighbor)

    return preds


def get_distances(graph, nodes):
    """Return a dict of distances between all nodes."""
    dists = {}
    for start in nodes:
        ends = nodes - {start}
        preds = bfs(graph, start, ends)
        dists[start] = {
            end: len(list(predecessors(preds, end)))
            for end in ends
        }

    return dists


def predecessors(preds, node):
    """Return an iterable of predecessors of the node."""
    while pred := preds[node]:
        yield pred
        node = pred


def most_pressure(graph, rates, minutes, start_valve='AA', workers=1):
    """Return the most pressure that can be released."""
    def _find_most(valves, workers):
        if workers < 1:
            return 0

        most = 0
        for partial_valves in combinations(valves, len(valves) // workers):
            partial_valves = frozenset(partial_valves)
            pressure1 = _do_find_most(start_valve, partial_valves, minutes)
            pressure2 = _find_most(valves - partial_valves, workers - 1)
            most = max(most, pressure1 + pressure2)

        return most

    @cache
    def _do_find_most(start_valve, valves, minutes):
        if minutes < 2:
            return 0

        most = 0
        for valve in valves:
            time = dists[start_valve][valve] + 1
            pressure = (
                (minutes - time)
                * rates[valve]
                + _do_find_most(valve, valves - {valve}, minutes - time)
            )
            most = max(most, pressure)

        return most

    valves = {valve for valve, rate in rates.items() if rate > 0}
    dists = get_distances(graph, valves | {start_valve})
    return _find_most(valves - {start_valve}, workers)


def main():
    """Main entry."""
    graph, rates = parse('input')
    assert most_pressure(graph, rates, minutes=30) == 1820
    assert most_pressure(graph, rates, minutes=26, workers=2) == 2602


if __name__ == '__main__':
    main()
