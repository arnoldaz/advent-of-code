from enum import Enum
from typing import Optional

FILE_NAME = "input.txt"
PATH_ONLY_FILE_NAME = "path-" + FILE_NAME
with open(FILE_NAME) as file:
    lines = [line.rstrip() for line in file]

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
    Default = 0
    Up = 1
    Down = 2
    Left = 3
    Right = 4

class Matrix:
    _data: list[list[str]]

    def __init__(self, data: list[str]):
        assert len(data) > 0 and len(data[0]) > 0
        self._data = [list(string) for string in data]

    def height(self) -> int:
        return len(self._data)

    def width(self) -> int:
        return len(self._data[0])

    def get_data(self) -> list[list[str]]:
        return self._data

    def get_symbol(self, position: Point) -> Optional[str]:
        return self._data[position.y][position.x] if self.in_bounds(position) else None

    def in_bounds(self, position: Point) -> bool:
        return 0 <= position.x < self.width() and 0 <= position.y < self.height()

    def get_neighbors(self, position: Point) -> list[tuple[Point, Direction]]:
        return [(position + direction.value, direction) for direction in Direction if direction != Direction.Default and self.in_bounds(position + direction.value)]

    def find_first_character_instance(self, character_to_find: str) -> Optional[Point]:   
        for y, line in enumerate(self.get_data()):
            for x, char in enumerate(line):
                if char == character_to_find:
                    return Point(x, y)

def get_initial_data(lines: list[str]) -> tuple[Matrix, Point]:
    matrix = Matrix(lines)

    start = matrix.find_first_character_instance("S")
    if not start:
        start = Point(-1, -1)

    return (matrix, start)

def get_pipe_path(matrix: Matrix, start: Point) -> list[Point]:
    data = matrix.get_data()
    current = start
    direction = Direction.Default

    # top
    if direction == Direction.Default and current.y - 1 >= 0:
        symbol = data[current.y - 1][current.x]
        if symbol == "|" or symbol == "F" or symbol == "7":
            direction = Direction.Up
            current = Point(current.x, current.y - 1)

    # bot
    if direction == Direction.Default and current.y + 1 <= matrix.height():
        symbol = data[current.y + 1][current.x]
        if symbol == "|" or symbol == "L" or symbol == "J":
            direction = Direction.Down
            current = Point(current.x, current.y + 1)

    # left
    if direction == Direction.Default and current.x - 1 >= 0:
        symbol = data[current.y][current.x - 1]
        if symbol == "-" or symbol == "J" or symbol == "7":
            direction = Direction.Left
            current = Point(current.x - 1, current.y)
            
    # right
    if direction == Direction.Default and current.x + 1 <= matrix.width():
        symbol = data[current.y][current.x + 1]
        if symbol == "-" or symbol == "F" or symbol == "L":
            direction = Direction.Right
            current = Point(current.x + 1, current.y)

    final_path = []

    while True:
        symbol = matrix.get_symbol(current)
        if not symbol:
            raise Exception("Something is very wrong")

        final_path.append(current)
        
        match symbol:
            case "|":
                if direction == Direction.Up:
                    current = Point(current.x, current.y - 1)
                    direction = Direction.Up
                elif direction == Direction.Down:
                    current = Point(current.x, current.y + 1)
                    direction = Direction.Down
            case "-":
                if direction == Direction.Left:
                    current = Point(current.x - 1, current.y)
                    direction = Direction.Left
                elif direction == Direction.Right:
                    current = Point(current.x + 1, current.y)
                    direction = Direction.Right
            case "L":
                if direction == Direction.Left:
                    current = Point(current.x, current.y - 1)
                    direction = Direction.Up
                elif direction == Direction.Down:
                    current = Point(current.x + 1, current.y)
                    direction = Direction.Right
            case "J":
                if direction == Direction.Right:
                    current = Point(current.x, current.y - 1)
                    direction = Direction.Up
                elif direction == Direction.Down:
                    current = Point(current.x - 1, current.y)
                    direction = Direction.Left
            case "7":
                if direction == Direction.Right:
                    current = Point(current.x, current.y + 1)
                    direction = Direction.Down
                elif direction == Direction.Up:
                    current = Point(current.x - 1, current.y)
                    direction = Direction.Left
            case "F":
                if direction == Direction.Left:
                    current = Point(current.x, current.y + 1)
                    direction = Direction.Down
                elif direction == Direction.Up:
                    current = Point(current.x + 1, current.y)
                    direction = Direction.Right
            case ".":
                print("Impossible to find non-path character")
            case "S":
                break

    return final_path

def write_only_path_file(matrix: Matrix, path: list[Point], start: Point):
    # Manually set starting char replacement
    START_CHAR_REPLACEMENT = "|"

    with open(PATH_ONLY_FILE_NAME, "w") as file:
        for y, line in enumerate(matrix.get_data()):
            write_line: list[str] = []
            for x, char in enumerate(line):
                point = Point(x, y)
                if point == start:
                    write_line.append(START_CHAR_REPLACEMENT)
                elif point in path:
                    write_line.append(char)
                else:
                    write_line.append(".")
            file.write("".join(write_line) + "\n")

def calculate_internal_tile_count(clean_matrix: Matrix) -> int:
    internal_tile_count = 0

    for line in clean_matrix.get_data():
        winding_number = 0
        for char in line:
            match char:
                case ".":
                    if winding_number % 4 == 2:
                        internal_tile_count += 1
                case "F":
                    winding_number += 1
                case "J":
                    winding_number += 1
                case "L":
                    winding_number -= 1
                case "7":
                    winding_number -= 1
                case "-":
                    pass
                case "|":
                    winding_number += 2
    
    return internal_tile_count

_matrix, _start = get_initial_data(lines)
_path = get_pipe_path(_matrix, _start)

# Run only once
# write_only_path_file(_matrix, _path, _start)

with open(PATH_ONLY_FILE_NAME) as file:
    clean_lines = [line.rstrip() for line in file]

_clean_matrix, _ = get_initial_data(clean_lines)

print(f"{len(_path) // 2=}")
print(f"{calculate_internal_tile_count(_clean_matrix)=}")
