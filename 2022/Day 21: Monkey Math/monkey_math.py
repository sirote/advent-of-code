"""Day 21: Monkey Math"""


import operator as op
from collections import deque


OPS = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.floordiv,
}
INVERT_OPS = {
    op.add: op.sub,
    op.sub: op.add,
    op.mul: op.floordiv,
    op.floordiv: op.mul,
}


def parse(filename):
    """Return a dict of monkey/job pairs."""
    riddle = {}
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            monkey, job = line.split(':')
            try:
                number = int(job)
            except ValueError:
                left, operator, right = job.strip().split()
                riddle[monkey] = [OPS[operator], left, right]
            else:
                riddle[monkey] = [number]

    return riddle


def iter_dfs(riddle, root='root'):
    """Iterative depth-first search."""
    queue = [root]
    while queue:
        monkey = queue.pop()
        if isinstance(monkey, str):
            queue.extend(riddle[monkey])
        else:
            yield monkey


def find_root_yell(riddle):
    """Return the monkey named root will yell."""
    return _find_monkey_yell(riddle, 'root').pop()


def find_humn_yell(riddle):
    """Return the number you will yell to pass root's equality test."""
    riddle['humn'] = [object()]
    _, monkey1, monkey2 = riddle['root']
    result1 = _find_monkey_yell(riddle, monkey1)
    result2 = _find_monkey_yell(riddle, monkey2)

    if len(result1) == 1:
        result = result1[0]
        stack = result2
    else:
        result = result2[0]
        stack = result1

    stack = deque(stack)
    while len(stack) > 1:
        operator = stack.pop()
        if isinstance(stack[-1], int):
            number = stack.pop()
            if operator in (op.sub, op.floordiv):
                result, number = number, result
            else:
                operator = INVERT_OPS[operator]
        else:
            number = stack.popleft()
            operator = INVERT_OPS[operator]

        result = operator(result, number)

    return result


def _find_monkey_yell(riddle, monkey):
    stack = []
    for op_or_number in iter_dfs(riddle, monkey):
        if isinstance(op_or_number, int):
            stack.append(op_or_number)
        else:
            number1 = stack.pop()
            number2 = stack.pop()
            try:
                stack.append(op_or_number(number1, number2))
            except TypeError:
                stack.extend((number2, number1, op_or_number))

    return stack


def main():
    """Main entry."""
    riddle = parse('input')
    assert find_root_yell(riddle) == 82225382988628
    assert find_humn_yell(riddle) == 3429411069028


if __name__ == '__main__':
    main()
