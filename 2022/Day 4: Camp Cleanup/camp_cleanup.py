"""Day 4: Camp Cleanup"""


def parse(filename):
    """Return an iterator of assignment pairs."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            section1, section2 = line.rstrip().split(',')
            yield _parse_section(section1), _parse_section(section2)


def _parse_section(section):
    lower, upper = section.split('-')
    return int(lower), int(upper)


def fully_contains(section1, section2):
    """Whether section1 fully containers section2."""
    return section1[0] <= section2[0] and section1[1] >= section2[1]


def overlaps(section1, section2):
    """Whether section1 overlaps with section2."""
    return section1[1] >= section2[0] and section1[0] <= section2[1]


def count_fully_contain_assignments(assignments):
    """Return the number of assignment pairs that one range fully
    contain the other.
    """
    return sum(
        fully_contains(*assignment)
        or fully_contains(*reversed(assignment))
        for assignment in assignments
    )


def count_overlap_assignments(assignments):
    """Return the number of assignment pairs that the ranges overlap."""
    return sum(overlaps(*assignment) for assignment in assignments)


def main():
    """Main entry."""
    assignments = list(parse('input'))
    assert count_fully_contain_assignments(assignments) == 515
    assert count_overlap_assignments(assignments) == 883


if __name__ == '__main__':
    main()
