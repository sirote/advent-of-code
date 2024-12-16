"""Day 15: Warehouse Woes"""


from typing import NamedTuple, Set


class PushWall(Exception):
    """Exception raised when the robot pushes the wall."""


class Position(NamedTuple):
    """Position in the warehouse."""

    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, int):
            return Position(self.x * other, self.y * other)
        raise NotImplementedError


UP = Position(-1, 0)
DOWN = Position(1, 0)
LEFT = Position(0, -1)
RIGHT = Position(0, 1)


class Movements:
    """Movements of the robot."""

    directions = {
        '^': UP,
        'v': DOWN,
        '<': LEFT,
        '>': RIGHT,
    }

    def __init__(self, movements):
        self.movements = movements

    def __iter__(self):
        for direction in self.movements:
            yield self.directions[direction]

    def __str__(self):
        return self.movements


class Warehouse(NamedTuple):
    """The warehouse."""

    robot: Position
    boxes: Set[Position]
    walls: Set[Position]
    width: int
    height: int

    def gps_coordinate(self):
        """Calculate the Goods Positioning System (GPS) coordinate."""
        return sum(100 * x + y for x, y in self.boxes)

    def move(self, direction):
        """Move the robot in the warehouse."""
        pos = robot = self.robot + direction

        while pos in self.boxes:
            pos += direction

        if pos in self.walls:
            return self

        if pos == robot:
            return self._replace(robot=robot)

        return self._replace(robot=robot, boxes=self.boxes - {robot} | {pos})

    def draw(self):
        """Draw the warehouse."""
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == self.robot:
                    print('@', end='')
                elif (i, j) in self.boxes:
                    print('O', end='')
                elif (i, j) in self.walls:
                    print('#', end='')
                else:
                    print('.', end='')
            print()


class SecondWarehouse(Warehouse):
    """The 2nd warehouse."""

    def __new__(cls, robot, boxes, walls, width, height):
        return super().__new__(
            cls,
            robot=Position(robot.x, robot.y * 2),
            boxes={Position(x, y * 2) for x, y in boxes},
            walls={Position(x, y * 2) for x, y in walls},
            width=width * 2,
            height=height,
        )

    def move(self, direction):
        """Move the robot in the warehouse."""
        return {
            UP: lambda: self._vertical_move(UP),
            DOWN: lambda: self._vertical_move(DOWN),
            LEFT: lambda: self._horizontal_move(self.robot + LEFT * 2, LEFT),
            RIGHT: lambda: self._horizontal_move(self.robot + RIGHT, RIGHT),
        }[direction]()

    def _horizontal_move(self, pos, direction):
        boxes = set()
        while pos in self.boxes:
            boxes.add(pos)
            pos += direction * 2

        if pos in self.walls:
            return self

        return self._replace(
            robot=self.robot + direction,
            boxes=self.boxes - boxes | {box + direction for box in boxes},
        )

    def _vertical_move(self, direction):
        boxes = set()
        queue = [self.robot]
        while queue:
            pos = queue.pop()
            try:
                if box := self._push(pos, direction):
                    boxes.add(box)
                    queue.extend((box, box + RIGHT))
            except PushWall:
                return self

        return self._replace(
            robot=self.robot + direction,
            boxes=self.boxes - boxes | {box + direction for box in boxes},
        )

    def _push(self, pos, direction):
        if (pos1 := pos + direction) in self.boxes:
            return pos1

        if (pos2 := pos + direction + LEFT) in self.boxes:
            return pos2

        if pos1 in self.walls or pos2 in self.walls:
            raise PushWall

        return None

    def draw(self):
        """Draw the 2nd warehouse."""
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == self.robot:
                    print('@', end='')
                elif (i, j) in self.boxes:
                    print('[', end='')
                elif (i, j) in self.walls:
                    print('#', end='')
                elif (i, j - 1) in self.boxes:
                    print(']', end='')
                elif (i, j - 1) in self.walls:
                    print('#', end='')
                else:
                    print('.', end='')
            print()


def parse(filename, warehouse_cls=Warehouse):
    """Parse the input file and return the warehouse and movements."""
    with open(filename, 'r', encoding='utf-8') as f:
        top, bottom = f.read().strip().split('\n\n')

    warehouse_map = top.splitlines()
    robot = None
    boxes = set()
    walls = set()

    for i, line in enumerate(warehouse_map):
        for j, cell in enumerate(line):
            if cell == '@':
                robot = Position(i, j)
            elif cell == 'O':
                boxes.add(Position(i, j))
            elif cell == '#':
                walls.add(Position(i, j))

    warehouse = warehouse_cls(
        robot=robot,
        boxes=boxes,
        walls=walls,
        width=len(warehouse_map[0]),
        height=len(warehouse_map),
    )
    movements = Movements(''.join(bottom.splitlines()))

    return warehouse, movements


def predict(warehouse, movements):
    """Predict the motion of the robot and boxes in the warehouse."""
    for direction in movements:
        warehouse = warehouse.move(direction)
    return warehouse


def test_example():
    """Test the example."""
    warehouse = predict(*parse('example1.txt'))
    assert warehouse.gps_coordinate() == 2028

    warehouse = predict(*parse('example2.txt'))
    assert warehouse.gps_coordinate() == 10092

    warehouse = predict(*parse('example2.txt', warehouse_cls=SecondWarehouse))
    assert warehouse.gps_coordinate() == 9021


def test_puzzle():
    """Test the puzzle."""
    warehouse = predict(*parse('input.txt'))
    assert warehouse.gps_coordinate() == 1438161

    warehouse = predict(*parse('input.txt', warehouse_cls=SecondWarehouse))
    assert warehouse.gps_coordinate() == 1437981
