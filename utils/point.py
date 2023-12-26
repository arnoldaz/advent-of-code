from enum import Enum

class Point:
    x: int
    y: int
    z: int

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{{Point: x={self.x}, y={self.y}, z={self.z}}}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        
        if isinstance(other, int):
            return Point(self.x + other, self.y + other, self.z + other)
        
        raise Exception(f"Unrecognized variable added to Point - {other}")

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.z == other.z
        
        raise Exception(f"Unrecognized variable compared to Point - {other}")

class Direction(Enum):
    Default = Point(0, 0)
    Up = Point(0, -1)
    Right = Point(1, 0)
    Down = Point(0, 1)
    Left = Point(-1, 0)

def shoelace_area(vertices: list[Point]) -> float:
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i].x * vertices[j].y
        area -= vertices[j].x * vertices[i].y
    area = abs(area) / 2
    return area

def invert_direction(direction: Direction) -> Direction:
    match direction:
        case Direction.Right:
            return Direction.Left
        case Direction.Left:
            return Direction.Right
        case Direction.Up:
            return Direction.Down
        case Direction.Down:
            return Direction.Up
        case Direction.Default:
            return Direction.Default
