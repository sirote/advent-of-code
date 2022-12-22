"""Day 20: Grove Positioning System"""


from collections import deque
from dataclasses import dataclass


def parse(filename):
    """Return a tuple of numbers containing the grove's coordinates."""
    with open(filename, 'r', encoding='utf-8') as file_:
        return tuple(int(number) for number in file_.readlines())


@dataclass
class Number:
    """A special type of number used in mixing process."""

    number: int
    index: int

    def __int__(self):
        return self.number


def decrypt(numbers, key=1, rounds=1):
    """Decrypt the list of numbers."""
    mixed = mix(numbers, key, rounds)
    zero_index = mixed.index(0)
    return sum(
        mixed[(zero_index + nth) % len(numbers)]
        for nth in (1000, 2000, 3000)
    )


def mix(numbers, key, rounds):
    """Mix the numbers."""
    divisor = len(numbers) - 1
    numbers = deque(
        Number(number * key, index)
        for index, number in enumerate(numbers)
    )

    for _ in range(rounds):
        for index in range(len(numbers)):
            if numbers[0].index != index:
                _rotate(numbers, index)

            number = numbers.popleft()
            index = int(number) % divisor
            numbers.insert(index, number)

    return [int(n) for n in numbers]


def _rotate(numbers, index):
    for i, number in enumerate(numbers):
        if number.index == index:
            numbers.rotate(-i)
            break


def main():
    """Main entry."""
    numbers = parse('input')
    assert decrypt(numbers) == 4426
    assert decrypt(numbers, key=811589153, rounds=10) == 8119137886612


if __name__ == '__main__':
    main()
