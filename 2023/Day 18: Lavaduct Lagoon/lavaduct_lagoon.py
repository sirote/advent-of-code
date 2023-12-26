"""Day 18: Lavaduct Lagoon"""


from itertools import cycle, islice


DIRECTIONS = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0),
}


def parse(filename):
    """Parse the dig plan into a list of tuples
    (direction, amount, color).
    """
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            direction, amount, color = line.strip().split()
            yield direction, int(amount), color.strip('()')


def parse_corlor_code(code):
    """Parse the color code into a instruction parameters."""
    digit_to_direction = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    hex_str, direction = code[1:6], code[6]
    return digit_to_direction[direction], int(hex_str, 16)


def parse_instructions(instructions):
    """Parse the instructions into a list of points."""
    x, y = 0, 0
    points = []
    for direction, amount in instructions:
        i, j = DIRECTIONS[direction]
        x += i * amount
        y += j * amount
        points.append((x, y))

    return points


def calculate_perimeter(points):
    """Calculate the perimeter of a polygon."""
    return sum(
        abs(x1 - x2) + abs(y1 - y2)
        for (x1, y1), (x2, y2) in zip(points, islice(cycle(points), 1, None))
    )


def calculate_area(points):
    """Calculate the area of a polygon using the shoelace formula."""
    return abs(sum(
        x1 * y2 - x2 * y1
        for (x1, y1), (x2, y2) in zip(points, islice(cycle(points), 1, None))
    )) / 2


def measure_cubic_meters(instructions):
    """Measure the cubic meters of the lagoon.

    Using Pick's theorem:
        A = i + b / 2 - 1

    where:
        A is the area of the lagoon
        i is the number of points inside the lagoon
        b is the number of points on the boundary of the lagoon

    lagoon cubic meters is i + b which equals to A + b / 2 + 1
    """
    points = parse_instructions(instructions)
    area = calculate_area(points)
    perimeter = calculate_perimeter(points)
    return int(area + perimeter / 2 + 1)


def main():
    """Main program."""
    dig_plan = list(parse('input'))
    assert measure_cubic_meters(
        (direction, amount)
        for direction, amount, _ in dig_plan
    ) == 40745
    assert measure_cubic_meters(
        parse_corlor_code(color_code)
        for _, _, color_code in dig_plan
    ) == 90111113594927


if __name__ == '__main__':
    main()
