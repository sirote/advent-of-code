"""Day 7: No Space Left On Device"""


from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass
class File:
    """An object represents a file in the filesystem."""

    name: str
    parent: File = None
    size: int = 0
    files: dict = field(default_factory=dict)

    def is_dir(self):
        """Whether this is a directory."""
        return self.size == 0


class State(Enum):
    """States of a parser in the parse function."""

    COMMAND = auto()
    LS_OUTPUT = auto()


def parse(filename):
    """Parse terminal output into a directory tree."""
    root = curr = File(name='/')
    state = State.COMMAND

    def _do_cd(directory):
        nonlocal curr, state
        state = State.COMMAND
        if directory == '..':
            curr = curr.parent
        elif directory == '/':
            curr = root
        else:
            if file_ := curr.files.get(directory):
                curr = file_
            else:
                raise FileNotFoundError('Direcoty {directory} does not exist')

    def _do_ls():
        nonlocal state
        state = State.LS_OUTPUT

    def _parse_ls_output(name, value):
        file_ = File(name=name, parent=curr)
        if value != 'dir':
            file_.size = int(value)
        curr.files[file_.name] = file_

    with open(filename, 'r', encoding='utf-8') as output:
        for line in output:
            tokens = line.rstrip().split()
            if tokens[0] == '$':
                command = locals()[f'_do_{tokens[1]}']
                if len(tokens) > 2:
                    command(*tokens[2:])
                else:
                    command()
            elif state == State.LS_OUTPUT:
                _parse_ls_output(name=tokens[1], value=tokens[0])

    return root


def walk(root):
    """Generate the file and its total size in a directory tree by
    walking the tree bottom-up.

    The total size of a directory is the sum of the sizes of the files
    it contains, directly or indirectly.
    """
    if not root.is_dir():
        yield root.size, root
        return

    total = 0
    for child in root.files.values():
        for size, file_ in walk(child):
            yield size, file_
            total += file_.size

    yield total, root


def sum_directories(tree, max_size):
    """Return the sum of the total sizes of directories with a total
    size of at most `max_size`.
    """
    return sum(
        size
        for size, file_ in walk(tree)
        if file_.is_dir() and size <= max_size
    )


def find_directory(tree, need_space, total_disk=70000000):
    """Return the smallest directory and its size that, if deleted,
    would free up enough space on the filesystem.
    """
    size_infos = list(filter(lambda d: d[1].is_dir(), walk(tree)))
    used = max(size_infos)[0]
    excess = need_space + used - total_disk
    return min(size_info for size_info in size_infos if size_info[0] >= excess)


def main():
    """Main entry."""
    tree = parse('input')
    assert sum_directories(tree, max_size=100000) == 1350966
    assert find_directory(tree, 30000000)[0] == 6296435


if __name__ == '__main__':
    main()
