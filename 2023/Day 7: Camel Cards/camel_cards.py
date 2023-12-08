"""Day 7: Camel Cards"""


from collections import Counter


TYPES = (
    (1, 1, 1, 1, 1),   # High card
    (1, 1, 1, 2),      # One pair
    (1, 2, 2),         # Two pairs
    (1, 1, 3),         # Three of a kind
    (2, 3),            # Full house
    (1, 4),            # Four of a kind
    (5,),              # Five of a kind
)


def parse(filename):
    """Parse the Camel Cards file."""
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            hand, bid = line.split()
            yield hand, int(bid)


def type_(hand):
    """Return the type of the hand."""
    counts = tuple(sorted(Counter(hand).values()))
    return TYPES.index(counts)


def ord_(hand, order='23456789TJQKA'):
    """Return the ordinal of the hand."""
    return tuple(order.index(card) for card in hand)


def rule1(hand):
    """Return the representation of the hand strength."""
    return type_(hand), ord_(hand)


def rule2(hand):
    """Return the representation of the hand strength."""
    new_hand = hand
    if 'J' in hand:
        if counts := Counter(hand.replace('J', '')):
            card, _ = counts.most_common(1)[0]
            new_hand = hand.replace('J', card)
        else:
            new_hand = 'AAAAA'

    return type_(new_hand), ord_(hand, 'J23456789TQKA')


def total_winnings(hands, rule):
    """Return the total winnings of the given set of hands."""
    return sum(
        hands[hand] * rank
        for rank, hand in enumerate(sorted(hands, key=rule), 1)
    )


def main():
    """Main program."""
    hands = dict(parse('input'))
    assert total_winnings(hands, rule1) == 250474325
    assert total_winnings(hands, rule2) == 248909434


if __name__ == '__main__':
    main()
