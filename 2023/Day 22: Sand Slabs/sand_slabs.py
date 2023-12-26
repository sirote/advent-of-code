"""Day 22: Sand Slabs"""


from collections import defaultdict


X, Y, Z = 0, 1, 2


def parse(filename):
    """Parse the snapshot represents the bricks."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            pos1, pos2 = line.strip().split('~')
            yield parse_position(pos1), parse_position(pos2)


def parse_position(position):
    """Return the position of the brick."""
    return tuple(int(x) for x in position.split(','))


def settle(bricks):
    """Return the settled positions of the bricks."""
    positions = sorted(bricks, key=lambda x: x[0][Z])
    settled_positions = []
    for curr in positions:
        for prev in settled_positions:
            if overlaps(curr, prev):
                z1 = prev[1][Z] + 1
                z2 = z1 + curr[1][Z] - curr[0][Z]
                curr = (
                    (curr[0][X], curr[0][Y], z1),
                    (curr[1][X], curr[1][Y], z2),
                )
                break
        else:
            curr = (
                (curr[0][X], curr[0][Y], 1),
                (curr[1][X], curr[1][Y], curr[1][Z] - curr[0][Z] + 1),
            )

        settled_positions.append(curr)
        settled_positions.sort(key=lambda x: x[1][Z], reverse=True)

    return settled_positions


def overlaps(brick1, brick2):
    """Return True if two bricks overlap in the x-y plane."""
    (x11, y11, _), (x12, y12, _) = brick1
    (x21, y21, _), (x22, y22, _) = brick2
    x_overlap = (
        x11 <= x21 <= x12 or x11 <= x22 <= x12
        or x21 <= x11 <= x22 or x21 <= x12 <= x22
    )
    y_overlap = (
        y21 <= y11 <= y22 or y21 <= y12 <= y22
        or y11 <= y21 <= y12 or y11 <= y22 <= y12
    )
    if x_overlap and y_overlap:
        return True
    return False


def get_support_info(positions):
    """Return the supporting and supported bricks for each brick."""
    supporting = defaultdict(set)
    supported = defaultdict(set)

    levels = defaultdict(list)
    for pos in positions:
        levels[pos[0][Z]].append(pos)

    for lower in positions:
        for upper in levels[lower[1][Z] + 1]:
            if overlaps(lower, upper):
                supporting[lower].add(upper)
                supported[upper].add(lower)

    return supporting, supported


def count_safely_disintegrated(bricks):
    """Return the number of bricks that can be safely disintegrated."""
    positions = settle(bricks)
    supporting, supported = get_support_info(positions)
    count = 0
    for pos in positions:
        if supported_bricks := supporting[pos]:
            if all(len(supported[brick]) > 1 for brick in supported_bricks):
                count += 1
        else:
            count += 1

    return count


def count_fell_bricks(bricks):
    """Return the sum of the number of other bricks that would fall."""
    positions = settle(bricks)
    supporting, supported = get_support_info(positions)

    def get_fell_bricks(start_brick):
        fell_bricks = set()
        visited = set()
        queue = [start_brick]
        while queue:
            brick = queue.pop()
            if brick in visited:
                continue

            visited.add(brick)

            for supported_brick in supporting[brick]:
                if (not supported[supported_brick]
                        - {start_brick}
                        - fell_bricks):
                    fell_bricks.add(supported_brick)
                    queue.append(supported_brick)

        return fell_bricks

    return sum(len(get_fell_bricks(pos)) for pos in positions)


def main():
    """Main program."""
    bricks = list(parse('input'))
    assert count_safely_disintegrated(bricks) == 409
    assert count_fell_bricks(bricks) == 61097


if __name__ == '__main__':
    main()
