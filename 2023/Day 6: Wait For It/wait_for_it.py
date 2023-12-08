"""Day 6: Wait For It"""


import math


def parse(filename):
    """Parse input file and return time and distance."""
    time = distance = None
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            if line.startswith('Time:'):
                time = parse_value(line)
            elif line.startswith('Distance:'):
                distance = parse_value(line)

    return time, distance


def parse_value(line):
    """Return time/distance value from a line."""
    return line.split(':', 1)[1].strip()


def count_wins(time, distance):
    """Return number of ways you can beat the record in a race.

    formula:

      -t^2 + (time)t - (distance) = 0
    """
    lower, upper = solve_quadratic(-1, time, -distance)
    return math.ceil(upper) - math.ceil(lower)


def solve_quadratic(a, b, c):
    """Solve quadratic equation."""
    temp = math.sqrt(b ** 2 - 4 * a * c)
    root1 = (-b + temp) / (2 * a)
    root2 = (-b - temp) / (2 * a)
    return root1, root2


def main():
    """Main entry point."""
    time, distance = parse('input')
    assert math.prod(
        count_wins(int(time), int(distance))
        for time, distance in zip(time.split(), distance.split())
    ) == 2374848
    assert count_wins(
        int(time.replace(' ', '')),
        int(distance.replace(' ', ''))
    ) == 39132886


if __name__ == '__main__':
    main()
