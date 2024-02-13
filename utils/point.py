from enum import Enum
import math

class Point:
    x: int
    y: int
    z: int

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"{{Point: x={self.x}, y={self.y}, z={self.z}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __add__(self, other) -> "Point":
        if other is None:
            raise RuntimeError(f"Adding None to Point - {self}")

        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)

        if isinstance(other, int):
            return Point(self.x + other, self.y + other, self.z + other)

        if isinstance(other, Direction):
            direction_point = other.value
            return Point(self.x + direction_point.x, self.y + direction_point.y, self.z + direction_point.z)

        raise RuntimeError(f"Unrecognized variable added to Point - {other}")

    def __sub__(self, other) -> "Point":
        if other is None:
            raise RuntimeError(f"Adding None to Point - {self}")

        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)

        if isinstance(other, int):
            return Point(self.x - other, self.y - other, self.z - other)

        if isinstance(other, Direction):
            direction_point = other.value
            return Point(self.x - direction_point.x, self.y - direction_point.y, self.z - direction_point.z)

        raise RuntimeError(f"Unrecognized variable added to Point - {other}")

    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other, self.z * other)

        raise RuntimeError(f"Unrecognized variable multiplied with Point - {other}")

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.z == other.z

        raise RuntimeError(f"Unrecognized variable compared to Point - {other}")

    def abs(self) -> "Point":
        return Point(abs(self.x), abs(self.y), abs(self.z))

INVALID_POINT = Point(-1, -1, -1)

class Direction(Enum):
    NONE = Point(0, 0)
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)

    def __mul__(self, other):
        if isinstance(other, int):
            return self.value * other

        raise RuntimeError(f"Unrecognized variable multiplied with Direction - {other}")

    @staticmethod
    def valid_directions() -> list["Direction"]:
        return [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]

def shoelace_area(vertices: list[Point]) -> float:
    n = len(vertices)
    area = 0.0

    for i in range(n):
        j = (i + 1) % n
        area += vertices[i].x * vertices[j].y
        area -= vertices[j].x * vertices[i].y

    area = abs(area) / 2
    return area

def reverse_direction(direction: Direction) -> Direction:
    match direction:
        case Direction.RIGHT:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.RIGHT
        case Direction.UP:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.UP
        case Direction.NONE:
            return Direction.NONE

def generate_2d_intersection(line1_start: Point, line1_end: Point, line2_start: Point, line2_end: Point) -> tuple[float, float]:
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    x1, x2 = line1_start.x, line1_end.x
    y1, y2 = line1_start.y, line1_end.y

    x3, x4 = line2_start.x, line2_end.x
    y3, y4 = line2_start.y, line2_end.y

    try:
        px = ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
        py = ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
    except ZeroDivisionError:
        return (math.inf, math.inf)

    return (px, py)
