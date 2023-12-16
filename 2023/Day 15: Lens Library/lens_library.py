"""Day 15: Lens Library"""


def parse(filename):
    """Parse the initialization sequence into a list of strings."""
    with open(filename, 'r', encoding='utf-8') as file_:
        return file_.read().strip().split(',')


def hash_(string):
    """Hash a string into a single number in the range 0 to 255."""
    value = 0
    for char in string:
        value = (value + ord(char)) * 17 % 256

    return value


def hashmap(sequence):
    """Perform the Holiday ASCII String Helper Manual Arrangement
    Procedure.
    """
    boxes = [{} for _ in range(256)]
    for step in sequence:
        label, focal_length = parse_step(step)
        box = boxes[hash_(label)]

        if focal_length is None:
            box.pop(label, None)
        else:
            box[label] = int(focal_length)

    return boxes


def parse_step(step):
    """Parse a single step of the HASHMAP."""
    if '=' in step:
        return step.split('=')

    if step.endswith('-'):
        return step[:-1], None

    raise ValueError(f'Invalid step: {step}')


def focusing_power(boxes):
    """Calculate the focusing power of the resulting lens
    configuration.
    """
    return sum(
        number * slot * focal_length
        for number, box in enumerate(boxes, start=1)
        for slot, focal_length in enumerate(box.values(), start=1)
    )


def main():
    """Main program."""
    sequence = parse('input')
    assert sum(hash_(string) for string in sequence) == 522547
    assert focusing_power(hashmap(sequence)) == 229271


if __name__ == '__main__':
    main()
