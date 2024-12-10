"""Day 9: Disk Fragmenter"""


from dataclasses import dataclass
from itertools import chain, islice, pairwise, repeat, zip_longest


@dataclass(order=True)
class FileBlock:
    """A file block."""
    index: int
    size: int
    id: int = None


def parse(filename):
    """Parse the disk map into a list of integers."""
    with open(filename, 'r', encoding='utf-8') as f:
        return [int(n) for n in f.read().strip()]


def block_defragment(disk_map):
    """Defragment the disk at file block level."""
    blocks = _block_expand(disk_map)
    i = 0
    j = len(blocks) - 1

    while True:
        while blocks[i] is not None:
            i += 1
        while blocks[j] is None:
            j -= 1

        if i >= j:
            break

        blocks[i], blocks[j] = blocks[j], blocks[i]

    return blocks


def _block_expand(disk_map):
    file_sizes = islice(disk_map, 0, None, 2)
    free_sizes = islice(disk_map, 1, None, 2)
    return [
        id
        for i, (file_size, free_size) in enumerate(
            zip_longest(file_sizes, free_sizes, fillvalue=0)
        )
        for id in chain(repeat(i, file_size), repeat(None, free_size))
    ]


def file_defragment(disk_map):
    """Defragment the disk at file level."""
    file_blocks, free_blocks = _file_expand(disk_map)
    last_index = file_blocks[-1].index + file_blocks[-1].size

    for file_block in reversed(file_blocks):
        for free_block in free_blocks:
            if file_block.index <= free_block.index:
                break
            if file_block.size > free_block.size:
                continue

            file_block.index = free_block.index
            free_block.index += file_block.size
            free_block.size -= file_block.size

    file_blocks.append(FileBlock(last_index, 0))

    return [
        id
        for lblock, rblock in pairwise(sorted(file_blocks))
        for id in chain(
            repeat(lblock.id, lblock.size),
            repeat(None, rblock.index - lblock.index - lblock.size),
        )
    ]


def _file_expand(disk_map):
    index = 0
    file_blocks = []
    file_sizes = islice(disk_map, 0, None, 2)
    free_blocks = []
    free_sizes = islice(disk_map, 1, None, 2)

    for i, (file_size, free_size) in enumerate(
            zip_longest(file_sizes, free_sizes, fillvalue=0)):
        file_blocks.append(FileBlock(index, file_size, i))
        index += file_size
        free_blocks.append(FileBlock(index, free_size))
        index += free_size

    return file_blocks, free_blocks


def checksum(blocks):
    """Calculate the checksum."""
    return sum(i * n for i, n in enumerate(blocks) if n is not None)


def test_example():
    """Test the example."""
    disk_map = parse('example.txt')
    assert checksum(block_defragment(disk_map)) == 1928
    assert checksum(file_defragment(disk_map)) == 2858


def test_puzzle():
    """Test the puzzle."""
    disk_map = parse('input.txt')
    assert checksum(block_defragment(disk_map)) == 6366665108136
    assert checksum(file_defragment(disk_map)) == 6398065450842
