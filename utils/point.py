from enum import Enum
import math

class Point2d:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{{{self.x}, {self.y}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other) -> "Point2d":
        if other is None:
            raise RuntimeError(f"Adding 'None' to 'Point2d' - {self}")

        if isinstance(other, Point2d):
            return Point2d(self.x + other.x, self.y + other.y)

        if isinstance(other, int):
            return Point2d(self.x + other, self.y + other)

        if isinstance(other, Direction):
            return Point2d(self.x + other.value.x, self.y + other.value.y)
        
        raise RuntimeError(f"Unrecognized variable added to 'Point2d' - {other}")
 
    def __sub__(self, other) -> "Point2d":
        if other is None:
            raise RuntimeError(f"Subtracting 'None' from 'Point2d' - {self}")

        if isinstance(other, Point2d):
            return Point2d(self.x - other.x, self.y - other.y)

        if isinstance(other, int):
            return Point2d(self.x - other, self.y - other)

        if isinstance(other, Direction):
            return Point2d(self.x - other.value.x, self.y - other.value.y)

        raise RuntimeError(f"Unrecognized variable subtracted from 'Point2d' - {other}")

    def __mul__(self, other):
        if isinstance(other, int):
            return Point2d(self.x * other, self.y * other)

        raise RuntimeError(f"Unrecognized variable multiplied with 'Point2d' - {other}")

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        if isinstance(other, Point2d):
            return self.x == other.x and self.y == other.y

        raise RuntimeError(f"Unrecognized variable compared to 'Point2d' - {other}")

    def copy(self) -> "Point2d":
        return Point2d(self.x, self.y)

    def abs(self) -> "Point2d":
        return Point2d(abs(self.x), abs(self.y))

    def in_bounds(self, width: int, height: int) -> bool:
        return self.x >= 0 and self.x < width and self.y >= 0 and self.y < height

class Point:
    x: int
    y: int
    z: int

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        if self.z == 0:
            return f"{{x={self.x}, y={self.y}}}"
        else:
            return f"{{x={self.x}, y={self.y}, z={self.z}}}"

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

        if isinstance(other, DirectionDiagonal):
            direction_point = other.value
            return Point(self.x + direction_point.x, self.y + direction_point.y, self.z + direction_point.z)

        if isinstance(other, DirectionOnlyDiagonal):
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

    def copy(self) -> "Point":
        return Point(self.x, self.y, self.z)

    def abs(self) -> "Point":
        return Point(abs(self.x), abs(self.y), abs(self.z))

    def get_neighbors_3d(self) -> list["Point"]:
        return [self + point for point in DIRECTIONS_3D]

    def between_points_orthogonal(self, point1: "Point", point2: "Point") -> bool:
        if point1.x == point2.x: # vertical
            return self.x == point1.x and (point1.y <= self.y <= point2.y or point1.y >= self.y >= point2.y)
        if point1.y == point2.y: # horizontal
            return self.y == point1.y and (point1.x <= self.x <= point2.x or point1.x >= self.x >= point2.x)

        raise RuntimeError(f"Points {point1} and {point2} are diagonal")

    def distance_orthogonal(self, point: "Point") -> int:
        if self.x == point.x: # vertical
            return abs(self.y - point.y)
        if self.y == point.y: # horizontal
            return abs(self.x - point.x)

        raise RuntimeError(f"Points {self} and {point} are diagonal")

    def point_from_distance(self, end: "Point", distance: int) -> "Point":
        if self.x == end.x: # vertical
            y_value = self.y + distance if self.y < end.y else self.y - distance
            return Point(self.x, y_value)
        if self.y == end.y: # horizontal
            x_value = self.x + distance if self.x < end.x else self.x - distance
            return Point(x_value, self.y)

        raise RuntimeError(f"Points {self} and {end} are diagonal")

    def in_bounds_2d(self, width: int, height: int) -> bool:
        return self.x >= 0 and self.x < width and self.y >= 0 and self.y < height

    # def between_points_ratio(self, start: "Point", end: "Point") -> float:
    #     if start.x == end.x: # vertical
    #         total_length = end.y - start.y
    #         length_to_point = self.y - start.y
    #         return length_to_point / total_length
    #     if start.y == end.y: # horizontal
    #         total_length = end.x - start.x
    #         length_to_point = self.x - start.x
    #         return length_to_point / total_length

    #     raise RuntimeError(f"Points {start} and {end} are diagonal")

    # @staticmethod
    # def between_points_point(start: "Point", end: "Point", ratio: float) -> "Point":
    #     if start.x == end.x: # vertical
    #         y_value = round(start.y + (ratio * (end.y - start.y)))
    #         return Point(start.x, y_value)
    #     if start.y == end.y: # horizontal
    #         x_value = round(start.x + (ratio * (end.x - start.x)))
    #         return Point(start.x, x_value)

    #     raise RuntimeError(f"Points {start} and {end} are diagonal")

INVALID_POINT = Point(-1, -1, -1)

DIRECTIONS_3D = [
    Point(1, 0, 0),
    Point(-1, 0, 0),
    Point(0, 1, 0),
    Point(0, -1, 0),
    Point(0, 0, 1),
    Point(0, 0, -1),
]

class Direction(Enum):
    NONE = Point(0, 0)
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)

    def __str__(self) -> str:
        return f"{{{self.name}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __mul__(self, other):
        if isinstance(other, int):
            return self.value * other

        raise RuntimeError(f"Unrecognized variable multiplied with 'Direction' - {other}")

    @staticmethod
    def valid_directions() -> list["Direction"]:
        return [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]

    @staticmethod
    def from_character(char: str) -> "Direction":
        match char:
            case "^":
                return Direction.UP
            case ">":
                return Direction.RIGHT
            case "v":
                return Direction.DOWN
            case "<":
                return Direction.LEFT
            case _:
                return Direction.NONE

class DirectionDiagonal(Enum):
    NONE = Point(0, 0)
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    UP_LEFT = Point(-1, -1)
    UP_RIGHT = Point(1, -1)
    DOWN_LEFT = Point(-1, 1)
    DOWN_RIGHT = Point(1, 1)

    def __str__(self) -> str:
        return f"{{{self.name}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __mul__(self, other):
        if isinstance(other, int):
            return self.value * other

        raise RuntimeError(f"Unrecognized variable multiplied with Direction - {other}")

class DirectionOnlyDiagonal(Enum):
    NONE = Point(0, 0)
    UP_LEFT = Point(-1, -1)
    UP_RIGHT = Point(1, -1)
    DOWN_LEFT = Point(-1, 1)
    DOWN_RIGHT = Point(1, 1)

    def __str__(self) -> str:
        return f"{{{self.name}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __mul__(self, other):
        if isinstance(other, int):
            return self.value * other

        raise RuntimeError(f"Unrecognized variable multiplied with Direction - {other}")

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
