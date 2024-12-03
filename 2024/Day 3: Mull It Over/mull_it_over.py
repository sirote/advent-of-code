"""Day 3: Mull It Over"""


import re


def parse(filename):
    """Read the section of corrupted memory from the file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def tokenize1(memory):
    """Tokenize the memory version 1."""
    for m in re.finditer(r'(mul)\((\d{,3}),(\d{,3})\)', memory):
        yield m.groups()


def tokenize2(memory):
    """Tokenize the memory version 2."""
    token = re.compile(r'''(mul\(                    # mul() instruction
                           |do\(                     # do() instruction
                           |don't\()                 # don't() instruction
                           (?:(\d{,3}),(\d{,3}))?\)  # X and Y''', re.X)
    for m in token.finditer(memory):
        yield m[1][:-1], m[2], m[3]


def run(instructions, mul_enabled=True):
    """Run the program."""
    result = 0
    for instr in instructions:
        match instr:
            case 'mul', x, y:
                if mul_enabled:
                    result += int(x) * int(y)
            case 'do', _, _:
                mul_enabled = True
            case "don't", _, _:
                mul_enabled = False
            case _:
                raise ValueError(f'Invalid instruction: {instr}')

    return result


def test_example():
    """Test the example."""
    memory1 = parse('example1.txt')
    assert run(tokenize1(memory1)) == 161
    memory2 = parse('example2.txt')
    assert run(tokenize2(memory2)) == 48


def test_puzzle():
    """Test the puzzle."""
    memory = parse('input.txt')
    assert run(tokenize1(memory)) == 170807108
    assert run(tokenize2(memory)) == 74838033
