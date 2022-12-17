"""Day 15: Beacon Exclusion Zone."""


import math
import re


def parse(filename):
    """Return an iterable of sensor and beacon coordinates."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            s_x, s_y, b_x, b_y = re.findall(r'-?\d+', line)
            yield (int(s_x), int(s_y)), (int(b_x), int(b_y))


def distance(point1, point2):
    """Return Manhattan distance of two points."""
    s_x, s_y = point1
    t_x, t_y = point2
    return abs(s_x - t_x) + abs(s_y - t_y)


def merge_ranges(ranges, new_range):
    """Return new ranges that merge existing ranges with the new
    range.
    """
    new_ranges = []
    lower2, upper2 = new_range

    for lower1, upper1 in ranges:
        if overlaps(lower1, upper1, lower2, upper2):
            lower2, upper2 = min(lower1, lower2), max(upper1, upper2)
        else:
            new_ranges.append((lower1, upper1))

    new_ranges.append((lower2, upper2))
    return new_ranges


def overlaps(lower1, upper1, lower2, upper2):
    """Whether two ranges are overlapped."""
    return upper1 >= lower2 - 1 and upper2 >= lower1 - 1


def find_row_coverage(data, row, min_=-math.inf, max_=math.inf):
    """Return row coverage as a list of ranges."""
    coverage = []
    for sensor, beacon in data:
        dist = distance(sensor, beacon)
        s_x, s_y = sensor
        d_x = dist - abs(s_y - row)
        if d_x > 0:
            lower, upper = s_x - d_x, s_x + d_x
            if lower <= max_ and upper >= min_:
                coverage = merge_ranges(coverage, (lower, upper))

    return coverage


def count_non_beacon_positions(data, row):
    """Return number of positions cannot contain a beacon."""
    position_count = sum(
        upper - lower + 1
        for lower, upper in find_row_coverage(data, row)
    )
    beacon_count = len({
        (b_x, b_y)
        for _, (b_x, b_y) in data
        if b_y == row
    })
    return position_count - beacon_count


def find_tuning_frequency(data, min_, max_):
    """Return the distress beacon's signal's tuning frequency."""
    for row in range(max_):
        coverage = find_row_coverage(data, row, min_=min_, max_=max_)
        if len(coverage) > 1:
            _, upper = coverage[0]
            return 4000000 * (upper + 1) + row

    raise RuntimeError('Unable to find the tunning frequency')


def main():
    """Main entry."""
    data = list(parse('input'))
    assert count_non_beacon_positions(data, row=2000000) == 5299855
    assert find_tuning_frequency(data, min_=0, max_=4000000) == 13615843289729


if __name__ == '__main__':
    main()
