# pylint: disable=unused-argument

import re
import sys
from utils.matrix import Matrix
from utils.point import Direction, Point

def parse_input(lines: list[str]) -> tuple[Matrix[str], Point, list[str | int]]:
    matrix_lines = lines[:-2]
    width = max(len(line) for line in matrix_lines)
    padded_lines = [line.ljust(width) for line in matrix_lines]
    matrix = Matrix[str](padded_lines, str)

    starting_position_x = next(i for i, symbol in enumerate(matrix_lines[0]) if symbol == ".")
    starting_position = Point(starting_position_x, 0)

    path_string = lines[-1]
    path_pattern = r"(\d+|[A-Z])"
    path_moves: list[str] = re.findall(path_pattern, path_string)
    converted_path_moves = [int(step) if step.isnumeric() else step for step in path_moves]

    return matrix, starting_position, converted_path_moves

def move_step(matrix: Matrix[str], current_position: Point, direction: Direction) -> Point:
    next_position = current_position + direction
    next_symbol = matrix.get_symbol(next_position) if matrix.in_bounds(next_position) else " "
    match next_symbol:
        case ".":
            return next_position
        case "#":
            return current_position
        case " ":
            match direction:
                case Direction.LEFT:
                    row = matrix.get_row(current_position.y)
                    index, symbol = next((matrix.width() - 1 - i, symbol) for i, symbol in enumerate(reversed(row)) if symbol != " ")
                    return Point(index, current_position.y) if symbol == "." else current_position
                case Direction.RIGHT:
                    row = matrix.get_row(current_position.y)
                    index, symbol = next((i, symbol) for i, symbol in enumerate(row) if symbol != " ")
                    return Point(index, current_position.y) if symbol == "." else current_position
                case Direction.UP:
                    column = matrix.get_column(current_position.x)
                    index, symbol = next((matrix.height() - 1 - i, symbol) for i, symbol in enumerate(reversed(column)) if symbol != " ")
                    return Point(current_position.x, index) if symbol == "." else current_position
                case Direction.DOWN:
                    column = matrix.get_column(current_position.x)
                    index, symbol = next((i, symbol) for i, symbol in enumerate(column) if symbol != " ")
                    return Point(current_position.x, index) if symbol == "." else current_position

    raise ValueError("Invalid direction of symbol")

def find_end_position(matrix: Matrix[str], starting_position: Point, path: list[str | int]) -> tuple[Point, Direction]:
    current_direction = Direction.RIGHT
    current_position = starting_position

    for step in path:
        if isinstance(step, int):
            for _ in range(step):
                current_position = move_step(matrix, current_position, current_direction)
        else:
            match current_direction:
                case Direction.LEFT:
                    current_direction = Direction.DOWN if step == "L" else Direction.UP
                case Direction.RIGHT:
                    current_direction = Direction.UP if step == "L" else Direction.DOWN
                case Direction.UP:
                    current_direction = Direction.LEFT if step == "L" else Direction.RIGHT
                case Direction.DOWN:
                    current_direction = Direction.RIGHT if step == "L" else Direction.LEFT


    return current_position, current_direction

def silver_solution(lines: list[str]) -> int:
    matrix, starting_position, path = parse_input(lines)
    position, direction = find_end_position(matrix, starting_position, path)

    match direction:
        case Direction.LEFT:
            direction_value = 2
        case Direction.RIGHT:
            direction_value = 0
        case Direction.UP:
            direction_value = 3
        case Direction.DOWN:
            direction_value = 1
        case _:
            direction_value = sys.maxsize

    return 1000 * (position.y + 1) + 4 * (position.x + 1)  + direction_value

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
