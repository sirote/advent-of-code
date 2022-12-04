"""Day 3: Rucksack Reorganization"""


def parse(filename):
    """Return an iterator of contents of each rucksack."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield line.rstrip()


def get_priority(item):
    """Return a priority of a given item."""
    if item.islower():
        return ord(item) - ord('a') + 1
    return ord(item) - ord('A') + 27


def find_common_item_type(*groups):
    """Return the common item type among the given groups."""
    group, *groups = (set(group) for group in groups)
    return group.intersection(*groups).pop()


def sum_priorities(items):
    """Return the sum of the priorities of the given items."""
    return sum(get_priority(item) for item in items)


def find_error_items(rucksacks):
    """Return an iterator of the item types that appear in both
    compartments of each rucksack.
    """
    for items in rucksacks:
        size = len(items) // 2
        yield find_common_item_type(items[:size], items[size:])


def find_badge_items(rucksacks):
    """Return an iterator of the item types that carried by all three
    Elves.
    """
    for offset in range(0, len(rucksacks), 3):
        groups = rucksacks[offset: offset+3]
        yield find_common_item_type(*groups)


def main():
    """Main entry."""
    rucksacks = list(parse('input'))
    assert sum_priorities(find_error_items(rucksacks)) == 8109
    assert sum_priorities(find_badge_items(rucksacks)) == 2738


if __name__ == '__main__':
    main()
