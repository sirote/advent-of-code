"""Day 23: LAN Party"""


from collections import defaultdict
from itertools import combinations


def parse(filename):
    """Parse the input file into a dictionary of connections."""
    connections = defaultdict(set)
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            a, b = line.strip().split('-')
            connections[a].add(b)
            connections[b].add(a)

    return connections


def find_group3(connections):
    """Find sets of three computers that are all connected to each
    other.
    """
    for a, b, c in combinations(connections, 3):
        if (a in connections[b]
                and b in connections[c]
                and c in connections[a]):
            yield a, b, c


def find_largest(connections):
    """the largest set of computers that are all connected to each
    other.
    """
    max_clique = []

    for u, group in connections.items():
        clique = [u]
        for v in group:
            if all(v in connections[w] for w in clique if w != u):
                clique.append(v)

        max_clique = max(max_clique, clique, key=len)

    return max_clique


def to_password(clique):
    """Convert a clique to a password."""
    return ','.join(sorted(clique))


def test_example():
    """Test the example."""
    connections = parse('example.txt')
    assert sum(
        any(x.startswith('t') for x in group)
        for group in find_group3(connections)
    ) == 7
    assert to_password(find_largest(connections)) == 'co,de,ka,ta'


def test_puzzle():
    """Test the puzzle."""
    connections = parse('input.txt')
    assert sum(
        any(x.startswith('t') for x in group)
        for group in find_group3(connections)
    ) == 1330
    assert to_password(
        find_largest(connections)
    ) == 'hl,io,ku,pk,ps,qq,sh,tx,ty,wq,xi,xj,yp'
