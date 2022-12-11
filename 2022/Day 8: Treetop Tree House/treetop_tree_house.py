"""Day 8: Treetop Tree House"""


def parse(filename):
    """Return the tree grid."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield list(line.rstrip())


def visible_trees(trees):
    """Return a set of positions of visible trees from outside the
    grid.
    """
    rows, columns = len(trees), len(trees[0])
    top_left = _visible_trees(trees, (0, rows), (0, columns), 1)
    bottom_right = _visible_trees(trees, (rows - 1, -1), (columns - 1, -1), -1)
    return top_left | bottom_right


def _visible_trees(trees, row_range, col_range, step):
    row_start, row_stop = row_range
    col_start, col_stop = col_range

    h_visible = set()
    h_max = [chr(0)] * len(trees[0])

    v_visible = set()
    v_max = [chr(0)] * len(trees)

    for i in range(row_start, row_stop, step):
        for j in range(col_start, col_stop, step):
            tree = trees[i][j]
            if tree > h_max[i]:
                h_visible.add((i, j))
                h_max[i] = tree

            if tree > v_max[j]:
                v_visible.add((i, j))
                v_max[j] = tree

    return h_visible | v_visible


def scenic_scores(trees):
    """Return an iterable of the scenic scores of each tree in the
    grid.
    """
    rows, cols = len(trees), len(trees[0])
    yield from (
        _horizontal_score(trees, (i, j), range(j - 1, -1, -1))
        * _horizontal_score(trees, (i, j), range(j + 1, cols, 1))
        * _vertical_score(trees, (i, j), range(i - 1, -1, -1))
        * _vertical_score(trees, (i, j), range(i + 1, rows, 1))
        for i in range(1, rows - 1)
        for j in range(1, cols - 1)
    )


def _horizontal_score(trees, pos, indices):
    return _score(trees[pos[0]][pos[1]], (trees[pos[0]][j] for j in indices))


def _vertical_score(trees, pos, indices):
    return _score(trees[pos[0]][pos[1]], (trees[i][pos[1]] for i in indices))


def _score(tree, trees):
    score = 0
    for other_tree in trees:
        if tree > other_tree:
            score += 1
        else:
            score += 1
            break

    return score


def main():
    """Main entry."""
    trees = list(parse('input'))
    assert len(visible_trees(trees)) == 1688
    assert max(scenic_scores(trees)) == 410400


if __name__ == '__main__':
    main()
