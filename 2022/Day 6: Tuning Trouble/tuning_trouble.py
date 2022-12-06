"""Day 6: Tuning Trouble"""


def parse(filename):
    """Return an iterator of datastream."""
    with open(filename, 'r', encoding='utf-8') as file_:
        yield from (char for line in file_ for char in line.rstrip())


def find_marker(datastream, width):
    """Return the end position of marker."""
    for start, _ in enumerate(datastream):
        end = start + width
        if len(set(datastream[start: end])) == width:
            return end

    raise RuntimeError('Marker was not found')


def find_start_of_packet_marker(datastream):
    """Return the end position of start-of-packet marker."""
    return find_marker(datastream, 4)


def find_start_of_message_marker(datastream):
    """Return the end position of start-of-message marker."""
    return find_marker(datastream, 14)


def main():
    """Main entry."""
    datastream = list(parse('input'))
    assert find_start_of_packet_marker(datastream) == 1707
    assert find_start_of_message_marker(datastream) == 3697


if __name__ == '__main__':
    main()
