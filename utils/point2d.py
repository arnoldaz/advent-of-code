from enum import Enum

class Point2d:
    def __init__(self, x: int, y: int):
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

        if isinstance(other, Direction2d):
            return Point2d(self.x + other.value.x, self.y + other.value.y)

        raise RuntimeError(f"Unrecognized variable added to 'Point2d' - {other}")

    def __sub__(self, other) -> "Point2d":
        if other is None:
            raise RuntimeError(f"Subtracting 'None' from 'Point2d' - {self}")

        if isinstance(other, Point2d):
            return Point2d(self.x - other.x, self.y - other.y)

        if isinstance(other, int):
            return Point2d(self.x - other, self.y - other)

        if isinstance(other, Direction2d):
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
        return 0 <= self.x < width and 0 <= self.y < height

    def get_neighbors(self, width: int, height: int, include_diagonal: bool = False, exclude_orthogonal: bool = False) -> list["Point2d"]:
        return [
            neighbor
            for direction in Direction2d.get_all_directions(include_diagonal, exclude_orthogonal)
            if (neighbor := self + direction).in_bounds(width, height)
        ]

    def get_neighbors_with_directions(self, width: int, height: int, include_diagonal: bool = False, exclude_orthogonal: bool = False) -> list[tuple["Point2d", "Direction2d"]]:
        return [
            (neighbor, direction)
            for direction in Direction2d.get_all_directions(include_diagonal, exclude_orthogonal)
            if (neighbor := self + direction).in_bounds(width, height)
        ]

    def get_neighbors_no_bounds(self, include_diagonal: bool = False, exclude_orthogonal: bool = False) -> list["Point2d"]:
        return [
            self + direction
            for direction in Direction2d.get_all_directions(include_diagonal, exclude_orthogonal)
        ]

    @staticmethod
    def manhattan_distance(point1: "Point2d", point2: "Point2d") -> int:
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)

class Direction2d(Enum):
    NONE = Point2d(0, 0)

    UP = Point2d(0, -1)
    RIGHT = Point2d(1, 0)
    DOWN = Point2d(0, 1)
    LEFT = Point2d(-1, 0)

    UP_RIGHT = Point2d(1, -1)
    UP_LEFT = Point2d(-1, -1)
    DOWN_RIGHT = Point2d(1, 1)
    DOWN_LEFT = Point2d(-1, 1)

    def __str__(self) -> str:
        return f"{{{self.name}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __mul__(self, other):
        if isinstance(other, int):
            return self.value * other

        raise RuntimeError(f"Direction '{self}' multiplied with unknown variable '{other}'")

    @staticmethod
    def get_all_directions(include_diagonal: bool = False, exclude_orthogonal: bool = False) -> list["Direction2d"]:
        if not include_diagonal and not exclude_orthogonal:
            return [Direction2d.UP, Direction2d.RIGHT, Direction2d.DOWN, Direction2d.LEFT]

        if include_diagonal and not exclude_orthogonal:
            return [Direction2d.UP, Direction2d.RIGHT, Direction2d.DOWN, Direction2d.LEFT,
                    Direction2d.UP_RIGHT, Direction2d.UP_LEFT, Direction2d.DOWN_RIGHT, Direction2d.DOWN_LEFT]

        if include_diagonal and exclude_orthogonal:
            return [Direction2d.UP_RIGHT, Direction2d.UP_LEFT, Direction2d.DOWN_RIGHT, Direction2d.DOWN_LEFT]

        return []

    @staticmethod
    def from_character(char: str) -> "Direction2d":
        match char:
            case "^":
                return Direction2d.UP
            case ">":
                return Direction2d.RIGHT
            case "v":
                return Direction2d.DOWN
            case "<":
                return Direction2d.LEFT
            case "U":
                return Direction2d.UP
            case "R":
                return Direction2d.RIGHT
            case "D":
                return Direction2d.DOWN
            case "L":
                return Direction2d.LEFT
            case _:
                raise RuntimeError(f"Character '{char}' is not convertable to Direction2d")

    def to_character(self) -> str:
        match self:
            case Direction2d.UP:
                return "U"
            case Direction2d.RIGHT:
                return "R"
            case Direction2d.DOWN:
                return "D"
            case Direction2d.LEFT:
                return "L"
            case Direction2d.NONE:
                return "N"
            case _:
                raise RuntimeError(f"Direction2d '{self}' is not convertable to character")

    def reverse(self) -> "Direction2d":
        match self:
            case Direction2d.UP:
                return Direction2d.DOWN
            case Direction2d.RIGHT:
                return Direction2d.LEFT
            case Direction2d.DOWN:
                return Direction2d.UP
            case Direction2d.LEFT:
                return Direction2d.RIGHT
            case Direction2d.UP_RIGHT:
                return Direction2d.DOWN_LEFT
            case Direction2d.UP_LEFT:
                return Direction2d.DOWN_RIGHT
            case Direction2d.DOWN_RIGHT:
                return Direction2d.UP_LEFT
            case Direction2d.DOWN_LEFT:
                return Direction2d.UP_RIGHT
            case _:
                raise RuntimeError(f"Direction2d '{self}' is not reversable")

    def turn_right(self) -> "Direction2d":
        match self:
            case Direction2d.UP:
                return Direction2d.RIGHT
            case Direction2d.RIGHT:
                return Direction2d.DOWN
            case Direction2d.DOWN:
                return Direction2d.LEFT
            case Direction2d.LEFT:
                return Direction2d.UP
            case _:
                raise RuntimeError(f"Direction2d '{self}' turn right is not supported")

    def turn_left(self) -> "Direction2d":
        match self:
            case Direction2d.UP:
                return Direction2d.LEFT
            case Direction2d.RIGHT:
                return Direction2d.UP
            case Direction2d.DOWN:
                return Direction2d.RIGHT
            case Direction2d.LEFT:
                return Direction2d.DOWN
            case _:
                raise RuntimeError(f"Direction2d '{self}' turn left is not supported")
