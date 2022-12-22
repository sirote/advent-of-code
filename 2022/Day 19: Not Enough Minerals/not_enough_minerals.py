"""Day 19: Not Enough Minerals"""


import re
from contextlib import suppress
from collections import defaultdict, namedtuple
from functools import cache
from math import prod
from operator import attrgetter


def parse(filename):
    """Return an iterable of blueprints as dict of robot and resource
    costs.
    """
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            yield _parse_blueprint(re.finditer(
                r'Each (\w+) robot costs ([^.]*).',
                line,
            ))


def _parse_blueprint(matches):
    blueprint = defaultdict(dict)
    for match in matches:
        robot, costs = match.groups()
        for cost, resource in re.findall(r'(\d+) (\w+)', costs):
            blueprint[robot][resource] = int(cost)

    return blueprint


class NotEnoughMinerals(Exception):
    """Raise when not enough minerals to build a robot."""


class RobotFactory:
    """An object represents robot factory."""

    def __init__(self, blueprint):
        self.blueprint = blueprint

    def get_max_costs(self):
        """Return maximum costs to build any robot per resource type."""
        max_costs = defaultdict(int)
        for costs in self.blueprint.values():
            for resource, cost in costs.items():
                max_costs[resource] = max(cost, max_costs[resource])

        return Resources()._replace(**max_costs)

    def build(self, robot, resources):
        """Build the specified robot and return the remaining
        resources.
        """
        remainings = {}
        for resource, cost in self.blueprint[robot].items():
            if (remaining := getattr(resources, resource) - cost) < 0:
                raise NotEnoughMinerals(resource)

            remainings[resource] = remaining

        return resources._replace(**remainings)


class Robots(namedtuple('Robots', 'ore, clay, obsidian, geode',
                        defaults=[1, 0, 0, 0])):
    """An object reprents number of robots per resource type."""

    def add(self, robot):
        """Increase number of `robot` by 1."""
        return self._replace(**{robot: getattr(self, robot) + 1})

    def collect(self):
        """Return resources collected by each robot type."""
        return Resources._make(robot * 1 for robot in self)


class Resources(namedtuple('Resources', 'ore, clay, obsidian, geode',
                           defaults=[0, 0, 0, 0])):
    """An object reprents number of resources per type."""

    def __add__(self, other):
        return Resources._make(a + b for a, b in zip(self, other))


def run(blueprint, minutes):
    """Run the blueprint for the given minutes."""
    @cache
    def _run(robots, resources, minutes):
        if not minutes:
            return resources

        collected = robots.collect()

        # greedy algorithm: always build geode-cracking robot and
        # obsidian-collecting robot when there are enough resources
        for robot in 'geode', 'obsidian':
            try:
                remaining = robot_factory.build(robot, resources)
            except NotEnoughMinerals:
                pass
            else:
                return _run(
                    robots.add(robot),
                    remaining + collected,
                    minutes - 1,
                )

        posibilities = []
        for robot in 'clay', 'ore':
            with suppress(NotEnoughMinerals):
                remaining = robot_factory.build(robot, resources)
                posibilities.append(_run(
                    robots.add(robot),
                    remaining + collected,
                    minutes - 1,
                ))

        if resources.ore < max_costs.ore:
            posibilities.append(_run(
                robots,
                resources + collected,
                minutes - 1,
            ))

        return max(posibilities, key=attrgetter('geode'))

    robot_factory = RobotFactory(blueprint)
    max_costs = robot_factory.get_max_costs()
    return _run(Robots(), Resources(), minutes)


def get_quality_levels(blueprints, minutes):
    """Return an iterable of the quality levels of blueprints."""
    result = (run(blueprint, minutes=minutes) for blueprint in blueprints)
    for id_, resources in enumerate(result, start=1):
        yield id_ * resources.geode


def find_largest_geodes(blueprints, minutes):
    """Return an interable of the largest number of geodes that could be
    open.
    """
    for blueprint in blueprints:
        resources = run(blueprint, minutes=minutes)
        yield resources.geode


def main():
    """Main entry."""
    blueprints = list(parse('input'))
    assert sum(get_quality_levels(blueprints, minutes=24)) == 1177
    assert prod(find_largest_geodes(blueprints[:3], minutes=32)) == 62744


if __name__ == '__main__':
    main()
