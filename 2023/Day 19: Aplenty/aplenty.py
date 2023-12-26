"""Day 19: Aplenty"""


import operator
import re
from math import prod


def parse(filename):
    """Parse the list of workflows and some part ratings."""
    with open(filename, 'r', encoding='utf-8') as file_:
        workflows, ratings = file_.read().split('\n\n')
        return (
            dict(
                parse_workflow(workflow)
                for workflow in workflows.splitlines()
            ),
            [
                parse_rating(rating)
                for rating in ratings.splitlines()
            ],
        )


def parse_workflow(workflow):
    """Return name and workflow object that evaluates the workflow."""
    def func(variables):
        for rule in rules:
            if (result := rule(variables)) is None:
                continue
            return result

        raise ValueError(f'Workflow {name} failed to process {variables}')

    if match := re.match(r'(\w+){(.*)}', workflow):
        name, raw_rules = match.groups()
        rules = [parse_rule(rule) for rule in raw_rules.split(',')]
        func.rules = rules
        return name, func

    raise ValueError(f'Invalid workflow: {workflow}')


def parse_rule(rule):
    """Return an object that evaluates the rule."""
    def func(variables):
        var = variables[operand1]
        if operators[operator_](var, int(operand2)):
            return return_value
        return None

    operators = {'>': operator.gt, '<': operator.lt}
    if match := re.match(r'(\w+)([><])(\d+):(\w+)', rule):
        operand1, operator_, operand2, return_value = match.groups()
        func.var = operand1
        func.value = int(operand2)
        func.operator = operator_
        func.return_value = return_value
        return func

    return lambda *_: rule


def parse_rating(rating):
    """Return a dictionary of rating of each part."""
    result = {}
    for part in rating.strip('{}').split(','):
        name, value = part.split('=')
        result[name] = int(value)

    return result


def iter_total_ratings(workflows, parts_ratings):
    """Iterate over the sum of accepted parts ratings."""
    for ratings in parts_ratings:
        name = 'in'
        while True:
            workflow = workflows[name]
            result = workflow(ratings)
            if result == 'A':
                yield ratings
                break

            if result == 'R':
                break

            name = result


def iter_ratings_combinations(workflows, min_rating=1, max_rating=4000):
    """Iterate over the number of all possible distinct combinations of
    each accepted ratings.
    """
    queue = [('in', {
        part: (min_rating, max_rating)
        for part in ('x', 'm', 'a', 's')
    })]
    while queue:
        result, ratings = queue.pop()
        if result == 'A':
            yield prod(b - a + 1 for a, b in ratings.values())
            continue

        if result == 'R':
            continue

        for rule in workflows[result].rules:
            try:
                operator_ = rule.operator
            except AttributeError:
                queue.append((rule(), ratings))
                break

            min_value, max_value = ratings[rule.var]
            if operator_ == '<':
                if max_value < rule.value:
                    queue.append((rule.return_value, ratings))
                    continue

                if min_value >= rule.value:
                    continue

                queue.append((
                    rule.return_value,
                    {**ratings, rule.var: (min_value, rule.value - 1)},
                ))
                ratings = {**ratings, rule.var: (rule.value, max_value)}

            elif operator_ == '>':
                if min_value > rule.value:
                    queue.append((rule.return_value, ratings))
                    continue

                if max_value <= rule.value:
                    continue

                queue.append((
                    rule.return_value,
                    {**ratings, rule.var: (rule.value + 1, max_value)},
                ))
                ratings = {**ratings, rule.var: (min_value, rule.value)}

            else:
                raise ValueError(f'Invalid operator: {operator_}')


def main():
    """Main program."""
    workflows, parts_ratings = parse('input')
    assert sum(
        sum(ratings.values())
        for ratings in iter_total_ratings(workflows, parts_ratings)
    ) == 374873
    assert sum(
        combinations
        for combinations in iter_ratings_combinations(workflows)
    ) == 122112157518711


if __name__ == '__main__':
    main()
