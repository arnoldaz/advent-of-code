from enum import Enum
from typing import Optional
import uuid
import sys

sys.setrecursionlimit(2 ** 30)

with open("input.txt") as file:
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

class Path:
    id: uuid.UUID
    steps: set[Point]
    current_position: Point
    previous_position: Point

    def __init__(self, start_position: Point):
        self.id = uuid.uuid1()
        self.steps = set([start_position])
        self.current_position = start_position
        self.previous_position = Point(-1, -1)

    def __str__(self):
        return f"{{Path: steps={len(self.steps)}, curr_pos={self.current_position}, prev_pos={self.previous_position}}}"

    def __repr__(self):
        return self.__str__()

    def take_step(self, new_position: Point):
        self.steps.add(new_position)
        self.previous_position = self.current_position
        self.current_position = new_position

    def get_path_length(self) -> int:
        return len(self.steps)
    
    def copy(self):
        new_path = Path(self.current_position)
        new_path.steps = self.steps.copy()
        new_path.previous_position = self.previous_position

        return new_path

def get_initial_data(lines: list[str]) -> tuple[Matrix, Point, Point]:
    matrix = Matrix(lines)
    matrix_data = matrix.get_data()

    first_line = matrix_data[0]
    last_line = matrix_data[-1]

    start_position = Point()
    end_position = Point()

    for x, char in enumerate(first_line):
        if char == ".":
            start_position = Point(x, 0)
            break

    for x, char in enumerate(last_line):
        if char == ".":
            end_position = Point(x, matrix.height() - 1)
            break

    return (matrix, start_position, end_position)

def calculate_paths_recursive(paths: list[Path], matrix: Matrix, end_position: Point, ignore_directions: bool, finished_path_lengths: list[int]):
    for path in paths[:]:
        if path.current_position == end_position:
            continue

        neighbors = matrix.get_neighbors(path.current_position)
        possible_movements: list[Point] = []

        for neighbor in neighbors:
            neighbor_position, neighbor_direction = neighbor
            symbol = matrix.get_symbol(neighbor_position)
            
            if symbol == "#":
                continue
            if not ignore_directions:
                if symbol == "<" and neighbor_direction != Direction.Left:
                    continue
                if symbol == ">" and neighbor_direction != Direction.Right:
                    continue
                if symbol == "v" and neighbor_direction != Direction.Down:
                    continue
                if symbol == "^" and neighbor_direction != Direction.Up:
                    continue
            if neighbor_position in path.steps:
                continue

            possible_movements.append(neighbor_position)

        # print(f"{i=} path moves to {possible_movements=} {path.current_position=} {path.get_path_length()=}")

        match len(possible_movements):
            case 0:
                for j, path_to_delete in enumerate(paths):
                    if path_to_delete.id == path.id and path.current_position != end_position:
                        paths.pop(j)
                        break
                continue
            case 1:
                for path_to_step in paths:
                    if path_to_step.id == path.id:
                        path_to_step.take_step(possible_movements[0])
                        break
            case _:
                for j, path_to_delete in enumerate(paths):
                    if path_to_delete.id == path.id:
                        paths.pop(j)
                        break
                
                for move in possible_movements:
                    cloned_path = path.copy()
                    cloned_path.take_step(move)
                    paths.append(cloned_path)

    if any(path.current_position != end_position for path in paths):
        removed_path_indexes: list[int] = []
        for f, path in enumerate(paths):
            if path.current_position == end_position:
                removed_path_indexes.append(f)

        for item in sorted(removed_path_indexes, reverse=True):
            length = paths[item].get_path_length()
            finished_path_lengths.append(length)
            print(f"Found new ending with length {length}")
            del paths[item]
        
        # Print for progress reporting
        if paths[0].get_path_length() % 250 == 0:
            print(f"Paths {len(paths)} has length {paths[0].get_path_length()}")

        calculate_paths_recursive(paths, matrix, end_position, ignore_directions, finished_path_lengths)

def calculate_max_path_length(matrix: Matrix, start_position: Point, end_position: Point, ignore_directions: bool) -> int:
    all_paths = [Path(start_position)]
    finished_path_lengths: list[int] = []

    calculate_paths_recursive(all_paths, matrix, end_position, ignore_directions, finished_path_lengths)

    for path in all_paths:
        print(f"Length: {path.get_path_length() - 1}")

    if len(all_paths) > 0:
        finished_path_lengths += [path.get_path_length() for path in all_paths]

    print(f"{finished_path_lengths=}")

    return max(finished_path_lengths) - 1

_matrix, _start_position, _end_position = get_initial_data(lines)
_max_path_length = calculate_max_path_length(_matrix, _start_position, _end_position, True)
print(f"{_max_path_length=}")