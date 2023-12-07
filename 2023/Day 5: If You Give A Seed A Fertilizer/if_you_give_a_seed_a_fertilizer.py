"""Day 5: If You Give A Seed A Fertilizer"""


import re
from typing import NamedTuple


class MapEntry(NamedTuple):
    """A map entry."""

    dest: int
    src: int
    length: int

    @property
    def end(self):
        """Get the end of the map entry."""
        return self.src + self.length


class Range(NamedTuple):
    """A range of seeds."""

    start: int
    length: int

    @property
    def end(self):
        """Get the end of the range."""
        return self.start + self.length


def parse(filename):
    """Parse the almanac and return the seeds and maps."""
    seeds = []
    maps = {}
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            if not line.strip():
                continue

            if line.startswith('seeds'):
                seeds.extend(parse_seeds(line))
            else:
                src, dest = parse_map_keys(line)
                maps[src] = (dest, parse_map(file_))

    return seeds, maps


def parse_seeds(line):
    """Parse the seeds from the line."""
    _, _, seeds = line.partition(':')
    return (int(seed) for seed in seeds.split())


def parse_map_keys(line):
    """Parse the map keys from the line."""
    if matches := re.match(r'(\w+)-to-(\w+)', line):
        return matches.groups()

    raise ValueError(f'Invalid map line: {line}')


def parse_map(file_):
    """Parse the map from the file."""
    map_ = []
    while (line := next(file_, '').strip()):
        dest_number, src_number, length = line.split()
        map_.append(MapEntry(int(dest_number), int(src_number), int(length)))

    return map_


def get_map_function(map_):
    """Get the map function from the map."""
    def map_func(range_):
        ranges = [range_]
        for entry in map_:
            remains = []
            for r in ranges:
                if ((start := max(r.start, entry.src))
                        < (end := min(r.end, entry.end))):
                    yield Range(entry.dest + start - entry.src, end - start)

                if (start := r.start) < (end := min(r.end, entry.src)):
                    remains.append(Range(start, end - start))

                if (start := max(r.start, entry.end)) < (end := r.end):
                    remains.append(Range(start, end - start))

            ranges = remains

        yield from ranges

    return map_func


def find_lowest_location_number(ranges, maps):
    """Find the lowest location number from the seed ranges and maps."""
    return min(_find_lowest_location_number(range_, maps) for range_ in ranges)


def _find_lowest_location_number(range_, maps):
    key = 'seed'
    ranges = [range_]
    while key != 'location':
        key, map_ = maps[key]
        map_func = get_map_function(map_)
        ranges = [r for range_ in ranges for r in map_func(range_)]

    return min(range_.start for range_ in ranges)


def main():
    """Main program."""
    seeds, maps = parse('input')
    assert find_lowest_location_number(
        [Range(start, 1) for start in seeds],
        maps,
    ) == 218513636
    assert find_lowest_location_number(
        [Range(start, length) for start, length in zip(*([iter(seeds)] * 2))],
        maps,
    ) == 81956384


if __name__ == '__main__':
    main()
