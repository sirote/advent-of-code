"""Day 4: Scratchcards"""


from collections import defaultdict, namedtuple


Card = namedtuple('Card', 'number winning_numbers my_numbers')


def parse(filename):
    """Parse the input file containing the scratchcards into an iterable
    of tuples of the card number, the winning numbers and the numbers on
    the card.
    """
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            card_number, numbers = line.split(':')
            winning_numbers, my_numbers = numbers.split('|')
            yield Card(
                int(card_number.split(' ', 1)[-1]),
                set(winning_numbers.split()),
                set(my_numbers.split()),
            )


def iter_points(cards):
    """Iterate over the points for each card."""
    for card in cards:
        yield calculate_points(card)


def calculate_points(card):
    """Calculate the points for a single card."""
    if (matches := len(card.winning_numbers & card.my_numbers)) > 0:
        return 2 ** (matches - 1)
    return 0


def iter_instances(cards):
    """Iterate over the instances for each card."""
    instances = defaultdict(int)
    for card in cards:
        instances[card.number] += 1
        yield instances[card.number]

        matches = len(card.winning_numbers & card.my_numbers)
        for i in range(1, matches + 1):
            instances[card.number + i] += instances[card.number]


def main():
    """Main entry point."""
    cards = list(parse('input'))
    assert sum(iter_points(cards)) == 21821
    assert sum(iter_instances(cards)) == 5539496


if __name__ == '__main__':
    main()
