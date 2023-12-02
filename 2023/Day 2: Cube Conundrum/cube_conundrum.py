"""Day 2: Cube Conundrum"""


import math
import re
from collections import defaultdict


def parse(filename):
    """Return a generator of game IDs and cube sets."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            game, cubes = line.split(':')
            game_id = parse_game_id(game)
            cube_sets = [
                parse_cube_set(cube_set)
                for cube_set in cubes.split(';')
            ]
            yield game_id, cube_sets


def parse_game_id(game):
    """Return the game ID."""
    return int(re.search(r'\d+', game).group())


def parse_cube_set(cube_set):
    """Return a dictionary of cube colors and their counts"""
    return {
        color: int(number)
        for number, color in re.findall(r'(\d+) (\w+)', cube_set)
    }


def iter_game_ids(games, bag):
    """Return a generator of game IDs that would have been possible
    given the bag.
    """
    for game_id, cube_sets in games:
        if is_possible(bag, cube_sets):
            yield game_id


def is_possible(bag, cube_sets):
    """Return True if the bag contains enough cubes for the cube sets,
    otherwise False.
    """
    return all(
        bag.get(color, 0) >= count
        for cube_set in cube_sets
        for color, count in cube_set.items()
    )


def iter_powers(games):
    """Return a generator of the power of the minimum set of cubes for
    each game.
    """
    for _, cube_sets in games:
        yield determine_power(cube_sets)


def determine_power(cube_sets):
    """Return the power of the minimum set of cubes for the game."""
    bag = defaultdict(int)
    for cube_set in cube_sets:
        for color, count in cube_set.items():
            bag[color] = max(bag[color], count)

    return math.prod(bag.values())


def main():
    """Main program."""
    games = list(parse('input'))
    assert sum(iter_game_ids(
        games,
        bag={'red': 12, 'green': 13, 'blue': 14},
    )) == 2528
    assert sum(iter_powers(games)) == 67363


if __name__ == '__main__':
    main()
