"""Day 25: Full of Hot Air"""


SNAFU_TO_VALUE = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
VALUE_TO_SNAFU = {v: k for k, v in SNAFU_TO_VALUE.items()}


def parse(filename):
    """Return an iterable of a list of all of the fuel requirements."""
    with open(filename, 'r', encoding='utf-8') as files:
        for line in files:
            yield line.rstrip()


def to_dec(number):
    """Convert the decimal number to SNAFU number."""
    value = 0
    for digit in number:
        value = value * 5 + SNAFU_TO_VALUE[digit]
    return value


def to_snafu(number):
    """Convert the SNAFU number to decimal number."""
    snafu = ''
    while number:
        if (digit := number % 5) > 2:
            digit = number % -5
            number -= digit

        number //= 5
        snafu = f'{VALUE_TO_SNAFU[digit]}{snafu}'

    return snafu


def main():
    """Main entry."""
    numbers = parse('input')
    total = sum(to_dec(number) for number in numbers)
    assert to_snafu(total) == '2=20---01==222=0=0-2'


if __name__ == '__main__':
    main()
