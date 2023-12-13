"""Day 12: Hot Springs"""


import re
from functools import cache


def parse(filename):
    """Parse records of spring conditions and contiguous groups of
    damaged springs.
    """
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            spring_conditions, damaged_groups = line.split()
            yield spring_conditions, [
                int(group)
                for group in damaged_groups.split(',')
            ]


def count_arrangement(conditions, groups, folds=1):
    """Count the number of possible arrangements."""
    conditions, groups = unfold(conditions, groups, folds)
    return _count(re.sub(r'\.+', '.', conditions), tuple(groups))


def unfold(conditions, groups, n=1):
    """Unfold a record of spring conditions and contiguous groups of
    damaged springs.
    """
    return '?'.join([conditions] * n), groups * n


@cache
def _count(conditions, groups):
    if not groups:
        return 0 if '#' in conditions else 1

    if conditions.count('#') + conditions.count('?') < sum(groups):
        return 0

    group, *groups = groups
    pattern = re.compile(rf'[.?][#?]{{{group}}}[.?]')
    conditions = f'.{conditions.strip(".")}.'

    count = 0
    for i, char in enumerate(conditions):
        sub_conditions = conditions[i:]
        if pattern.match(sub_conditions):
            count += _count(sub_conditions[group + 2:], tuple(groups))

        if char == '#':
            break

    return count


def main():
    """Main program."""
    records = list(parse('input'))
    assert sum(
        count_arrangement(*record, folds=1)
        for record in records
    ) == 7732
    assert sum(
        count_arrangement(*record, folds=5)
        for record in records
    ) == 4500070301581


if __name__ == '__main__':
    main()
