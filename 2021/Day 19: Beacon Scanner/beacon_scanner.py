"""Day 19: Beacon Scanner"""


from collections import defaultdict
from itertools import combinations, permutations, product, takewhile
from pathlib import Path
from typing import NamedTuple


PATH = Path(__file__).parent


# There are at least 12 beacons that both scanners detect within the
# overlap.
BEACON_COUNT = 12


class Point(NamedTuple):

    x: int
    y: int
    z: int

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(*(a + b for a, b in zip(self, other)))

        if isinstance(other, int):
            return Point(*(a + other for a in self))

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(*(a - b for a, b in zip(self, other)))

        if isinstance(other, int):
            return Point(*(a - other for a in self))

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(*(a * b for a, b in zip(self, other)))

        if isinstance(other, int):
            return Point(*(a * other for a in self))

        return NotImplemented

    def get_distance(self, other):
        return sum(abs(dist) for dist in self - other)

    def rotate(self):
        for point in permutations(self):
            yield Point(*point)


class Points:

    def __init__(self, points):
        self.points = points

    def __repr__(self):
        return f'Points({self.points})'

    def __len__(self):
        return len(self.points)

    def __iter__(self):
        return iter(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __hash__(self):
        return hash(tuple(self.points))

    def __eq__(self, other):
        return self.points == other.points

    def __add__(self, other):
        if isinstance(other, Points):
            return Points([a + b for a, b in zip(self, other)])

        if isinstance(other, Point):
            return Points([point + other for point in self])

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Points):
            return Points([a - b for a, b in zip(self, other)])

        if isinstance(other, Point):
            return Points([point - other for point in self])

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Points):
            return Points([a * b for a, b in zip(self, other)])

        if isinstance(other, Point):
            return Points([point * other for point in self])

        return NotImplemented

    def rotate(self):
        for points in zip(*(point.rotate() for point in self.points)):
            yield Points(points)


class BeaconScanners:

    def __init__(self, scanners):
        self.scanners = scanners
        self.distances = [
            self._get_distances(points)
            for points in scanners
        ]

    def get_map(self):
        """Return postions of scanners and beacons relative to the first
        scanner.
        """
        mapped_scanners = []
        mapped_beacons = set()
        ref_scanners = zip(
            [Point(0, 0, 0)],
            self.distances[0:1],
            self.scanners[0:1],
        )
        scanners = zip(self.distances[1:], self.scanners[1:])

        while scanners:
            new_ref_scanners = []
            for offset, ref_dists, ref_points in ref_scanners:
                mapped_scanners.append(offset)
                mapped_beacons.update(ref_points)
                _ref_scanners, scanners = self._get_map(
                    (ref_dists, sorted(ref_points)), scanners
                )
                new_ref_scanners.extend(_ref_scanners)

            if not new_ref_scanners:
                raise RuntimeError('Unable to map beacons')

            ref_scanners = new_ref_scanners

        for ref_scanner in ref_scanners:
            offset, _, points = ref_scanner
            mapped_scanners.append(offset)
            mapped_beacons.update(points)

        return mapped_scanners, mapped_beacons

    def _get_map(self, ref_scanner, scanners):
        ref_scanners = []
        remaining = []
        ref_dists, ref_points = ref_scanner

        for dists, points in scanners:
            try:
                offset, mapped_points = self._map_points(
                    ref_dists, dists, ref_points, points
                )
            except ValueError:
                remaining.append((dists, points))
            else:
                ref_scanners.append((
                    offset,
                    self._get_distances(mapped_points),
                    mapped_points
                ))

        return ref_scanners, remaining

    def _map_points(self, ref_dists, dists, ref_points, points):
        for ref_sub_point, sub_point in self._iter_sub_points(ref_dists, dists):
            for rot_sub_point, rot_points in zip(
                    self._rotate(sub_point), self._rotate(points)):
                offset = rot_sub_point - ref_sub_point
                transformed_points = [
                    rot_point - offset
                    for rot_point in sorted(rot_points)
                ]
                if self._match(ref_points, transformed_points):
                    return offset, transformed_points

        raise ValueError(f'Unable to map beacon positions: {points}')

    @staticmethod
    def _rotate(point):
        for rot_point in point.rotate():
            for i, j, k in product((1, -1), repeat=3):
                yield rot_point * Point(i, j, k)

    @staticmethod
    def _iter_sub_points(ref_dists, dists):
        visited = set()
        for ref_dist, ref_pairs in ref_dists.items():
            if not (sub_pairs := dists.get(ref_dist)):
                continue

            for ref_sub_point, _ in ref_pairs:
                for sub_pair in sub_pairs:
                    for sub_point in sub_pair:
                        if (ref_sub_point, sub_point) in visited:
                            continue

                        yield ref_sub_point, sub_point
                        visited.add((ref_sub_point, sub_point))

    @staticmethod
    def _match(ref_points, points):
        ref_points, points = map(iter, (ref_points, points))
        ref_point = next(ref_points, None)
        point = next(points, None)
        count = 0

        while ref_point and point:
            if ref_point == point:
                count += 1
                if count >= BEACON_COUNT:
                    return True

                ref_point = next(ref_points, None)
                point = next(points, None)
            elif ref_point < point:
                ref_point = next(ref_points, None)
            else:
                point = next(points, None)

        return False

    @staticmethod
    def _get_distances(points):
        dists = defaultdict(list)
        for point1, point2 in combinations(points, r=2):
            dist = point1.get_distance(point2)
            dists[dist].append((point1, point2))

        return dists


def parse(path):
    scanners = []
    with path.open(encoding='utf-8') as input_file:
        for line in input_file:
            if 'scanner' not in line:
                continue

            scanners.append(Points([
                Point(*(int(n) for n in line.split(',')))
                for line in takewhile(lambda l: l.strip(), input_file)
            ]))

    return scanners


def test_example():
    scanners, beacons = BeaconScanners(parse(PATH / 'example')).get_map()
    assert len(beacons) == 79
    assert max(
        scanner1.get_distance(scanner2)
        for scanner1, scanner2 in combinations(scanners, r=2)
    ) == 3621


def test_part1():
    _, beacons = BeaconScanners(parse(PATH / 'input')).get_map()
    assert len(beacons) == 385


def test_part2():
    scanners, _ = BeaconScanners(parse(PATH / 'input')).get_map()
    assert max(
        scanner1.get_distance(scanner2)
        for scanner1, scanner2 in combinations(scanners, r=2)
    ) == 10707
