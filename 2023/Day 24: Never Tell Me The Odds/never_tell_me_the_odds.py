"""Day 24: Never Tell Me The Odds"""


import math
from itertools import combinations, product
from typing import NamedTuple


X, Y, Z = range(3)


class Hailstone(NamedTuple):
    """Hailstone object."""

    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    def __str__(self):
        return f'{self.position} @ {self.velocity}'

    @property
    def position(self):
        """The position of the hailstone."""
        return self.px, self.py, self.pz

    @property
    def velocity(self):
        """The velocity of the hailstone."""
        return self.vx, self.vy, self.vz

    def add_velocity(self, dvx, dvy, dvz):
        """Return a new hailstone with added velocity."""
        return Hailstone(
            self.px,
            self.py,
            self.pz,
            self.vx + dvx,
            self.vy + dvy,
            self.vz + dvz,
        )

    def get_xtime(self, x):
        """Return the time at which the hailstone will be at x."""
        if self.vx == 0 or x is None:
            return math.inf
        return (x - self.px) / self.vx

    def get_ytime(self, y):
        """Return the time at which the hailstone will be at y."""
        if self.vy == 0 or y is None:
            return math.inf
        return (y - self.py) / self.vy

    def get_ztime(self, z):
        """Return the time at which the hailstone will be at z."""
        if self.vz == 0 or z is None:
            return math.inf
        return (z - self.pz) / self.vz

    def collide_time(self, other):
        """Return the time at which two hailstones will collide."""
        xy = self.xy_intersect(other)
        xz = self.xz_intersect(other)
        yz = self.yz_intersect(other)

        times = list(filter(lambda t: t != math.inf, (
            self.get_xtime(xy[0]),
            self.get_xtime(xz[0]),
            self.get_ytime(yz[0]),
        )))

        if (
            times
            and all(round(t1) == round(t2) for t1, t2 in zip(times, times[1:]))
        ):
            return round(times[0])

        return math.inf

    def xy_intersect(self, other):
        """Return the intersection of the XY plane of two hailstones."""
        return self._plane_intersect(
            (self.px, self.py),
            (other.px, other.py),
            (self.vx, self.vy),
            (other.vx, other.vy),
        )

    def xz_intersect(self, other):
        """Return the intersection of the XZ plane of two hailstones."""
        return self._plane_intersect(
            (self.px, self.pz),
            (other.px, other.pz),
            (self.vx, self.vz),
            (other.vx, other.vz),
        )

    def yz_intersect(self, other):
        """Return the intersection of the YZ plane of two hailstones."""
        return self._plane_intersect(
            (self.py, self.pz),
            (other.py, other.pz),
            (self.vy, self.vz),
            (other.vy, other.vz),
        )

    @staticmethod
    def _plane_intersect(pos1, pos2, vel1, vel2):
        e = vel1[Y] * vel2[X]
        f = vel1[X] * vel2[Y]
        if e == f:
            return None, None

        a = vel1[Y] * pos1[X]
        b = vel1[X] * pos1[Y]
        c = vel2[Y] * pos2[X]
        d = vel2[X] * pos2[Y]
        x = ((a - b) * vel2[X] - (c - d) * vel1[X]) / (e - f)
        y = ((a - b) * vel2[Y] - (c - d) * vel1[Y]) / (e - f)

        return x, y


def parse(filename):
    """Parse lines of hailstones' positions and velocities."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            position, velocity = line.strip().split('@')
            yield Hailstone(
                *(int(p) for p in position.split(',')),
                *(int(v) for v in velocity.split(',')),
            )


def count_xy_intersections(hailstones, bounds):
    """Count the number of intersections occur within the test area in
    the XY plane.
    """
    count = 0
    min_, max_ = bounds
    for h1, h2 in combinations(hailstones, 2):
        x, y = h1.xy_intersect(h2)
        if x is None or y is None:
            continue

        if (h1.get_xtime(x) < 0
                or h1.get_ytime(y) < 0
                or h2.get_xtime(x) < 0
                or h2.get_ytime(y) < 0):
            continue

        if min_ <= x <= max_ and min_ <= y <= max_:
            count += 1

    return count


def find_rock(hailstones):
    """Return the rock that perfectly collides with every hailstone."""
    min_vx = min_vy = min_vz = math.inf
    max_vx = max_vy = max_vz = -math.inf
    for hailstone in hailstones:
        min_vx = min(min_vx, hailstone.vx)
        min_vy = min(min_vy, hailstone.vy)
        min_vz = min(min_vz, hailstone.vz)
        max_vx = max(max_vx, hailstone.vx)
        max_vy = max(max_vy, hailstone.vy)
        max_vz = max(max_vz, hailstone.vz)

    (px, py), (vx, vy) = find_xy_collision(
        hailstones,
        (min_vx, max_vx),
        (min_vy, max_vy),
    )
    (_, pz), (_, vz) = find_xz_collision(
        hailstones,
        (vx, vx + 1),
        (min_vz, max_vz),
    )
    return Hailstone(px, py, pz, vx, vy, vz)


def find_xy_collision(hailstones, vx_bound, vy_bound):
    """Return the collision position and velocity in the XY plane."""
    (i, j, _), (x, y) = _find_plane_collision(
        hailstones,
        func_name='xy_intersect',
        range_=product(_get_range(*vx_bound), _get_range(*vy_bound), range(1)),
    )
    return (x, y), (i, j)


def find_xz_collision(hailstones, vx_bound, vz_bound):
    """Return the collision position and velocity in the XZ plane."""
    (i, _, k), (x, z) = _find_plane_collision(
        hailstones,
        func_name='xz_intersect',
        range_=product(_get_range(*vx_bound), range(1), _get_range(*vz_bound)),
    )
    return (x, z), (i, k)


def _get_range(min_, max_):
    error = max((max_ - min_) * 5 // 100, 10)
    return range(min_ - error, max_ + error)


def _find_plane_collision(hailstones, func_name, range_):
    candidates = dict(
        _iter_plane_intersections(
            hailstones,
            func_name,
            range_,
        )
    )
    if len(candidates) == 1:
        return candidates.popitem()

    return _choose_candidate(
        hailstones,
        func_name,
        candidates,
    )


def _iter_plane_intersections(hailstones, func_name, range_):
    for i, j, k in range_:
        h = [h.add_velocity(-i, -j, -k) for h in hailstones[:3]]

        intersection1 = getattr(h[0], func_name)(h[1])
        if intersection1 == (None, None):
            continue

        intersection2 = getattr(h[0], func_name)(h[2])
        if intersection2 == (None, None):
            continue

        if intersection1 == intersection2:
            yield (i, j, k), intersection1


def _choose_candidate(hailstones, func_name, candidates):
    h0 = hailstones[0]
    for h1 in hailstones[3:]:
        _candidates = {}
        for (i, j, k), (x, y) in candidates.items():
            _h0 = h0.add_velocity(-i, -j, -k)
            _h1 = h1.add_velocity(-i, -j, -k)

            intersection = getattr(_h0, func_name)(_h1)
            if intersection == (None, None):
                continue

            if intersection == (x, y):
                _candidates[i, j, k] = (x, y)

        if len(_candidates) == 1:
            return _candidates.popitem()

        candidates = _candidates

    raise ValueError('A collision candidate was not found.')


def main():
    """Main program."""
    hailstones = list(parse('input'))
    assert count_xy_intersections(
        hailstones,
        bounds=(2 * 10**14, 4 * 10**14),
    ) == 16665
    assert int(sum(find_rock(hailstones).position)) == 769840447420960


if __name__ == '__main__':
    main()
