import re
import sys
from utils.matrix import Matrix
from utils.point import Direction, Point

# Map for moving between cube faces, only works for cube with pattern like this:
#    [1][2]
#    [3]
# [5][4]
# [6]
CUBE_MAP: dict[tuple[Point, Point, Direction], tuple[Point, Point, Direction]] = {
    (Point(0, 50 * 2), Point(50 - 1, 50 * 2), Direction.UP): (Point(50, 50), Point(50, 50 * 2 - 1), Direction.RIGHT),  # 5 to 3
    (Point(50, 50), Point(50, 50 * 2 - 1), Direction.LEFT): (Point(0, 50 * 2), Point(50 - 1, 50 * 2), Direction.DOWN), # 3 to 5

    (Point(50, 50 * 3 - 1), Point(50 * 2 - 1, 50 * 3 - 1), Direction.DOWN): (Point(50 - 1, 50 * 3), Point(50 - 1, 50 * 4 - 1), Direction.LEFT), # 4 to 6
    (Point(50 - 1, 50 * 3), Point(50 - 1, 50 * 4 - 1), Direction.RIGHT): (Point(50, 50 * 3 - 1), Point(50 * 2 - 1, 50 * 3 - 1), Direction.UP),  # 6 to 4

    (Point(0, 50 * 4 - 1), Point(50 - 1, 50 * 4 - 1), Direction.DOWN): (Point(50 * 2, 0), Point(50 * 3 - 1, 0), Direction.DOWN), # 6 to 2
    (Point(50 * 2, 0), Point(50 * 3 - 1, 0), Direction.UP): (Point(0, 50 * 4 - 1), Point(50 - 1, 50 * 4 - 1), Direction.UP),     # 2 to 6

    (Point(0, 50 * 3), Point(0, 50 * 4 - 1), Direction.LEFT): (Point(50, 0), Point(50 * 2 - 1, 0), Direction.DOWN), # 6 to 1
    (Point(50, 0), Point(50 * 2 - 1, 0), Direction.UP): (Point(0, 50 * 3), Point(0, 50 * 4 - 1), Direction.RIGHT),  # 1 to 6

    (Point(50 * 2 - 1, 50 * 2), Point(50 * 2 - 1, 50 * 3 - 1), Direction.RIGHT): (Point(50 * 3 - 1, 50 - 1), Point(50 * 3 - 1, 0), Direction.LEFT), # 4 to 2
    (Point(50 * 3 - 1, 50 - 1), Point(50 * 3 - 1, 0), Direction.RIGHT): (Point(50 * 2 - 1, 50 * 2), Point(50 * 2 - 1, 50 * 3 - 1), Direction.LEFT), # 2 to 4

    (Point(50 * 2 - 1, 50), Point(50 * 2 - 1, 50 * 2 - 1), Direction.RIGHT): (Point(50 * 2, 50 - 1), Point(50 * 3 - 1, 50 - 1), Direction.UP),  # 3 to 2
    (Point(50 * 2, 50 - 1), Point(50 * 3 - 1, 50 - 1), Direction.DOWN): (Point(50 * 2 - 1, 50), Point(50 * 2 - 1, 50 * 2 - 1), Direction.LEFT), # 2 to 3

    (Point(0, 50 * 2), Point(0, 50 * 3 - 1), Direction.LEFT): (Point(50, 50 - 1), Point(50, 0), Direction.RIGHT), # 5 to 1
    (Point(50, 50 - 1), Point(50, 0), Direction.LEFT): (Point(0, 50 * 2), Point(0, 50 * 3 - 1), Direction.RIGHT), # 1 to 5
}

def get_cube_map_movement(position: Point, direction: Direction) -> tuple[Point, Direction]:
    for (start, end, required_direction), (destination_start, destination_end, destination_direction) in CUBE_MAP.items():
        if position.between_points_orthogonal(start, end) and direction == required_direction:
            distance = position.distance_orthogonal(start)
            new_point = destination_start.point_from_distance(destination_end, distance)
            return new_point, destination_direction

    raise ValueError(f"{position=} with {direction=} not in the cube map")

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

def move_step(matrix: Matrix[str], current_position: Point, direction: Direction, is_cube: bool) -> tuple[Point, Direction]:
    next_position = current_position + direction
    next_symbol = matrix.get_symbol(next_position) if matrix.in_bounds(next_position) else " "
    match next_symbol:
        case ".":
            return next_position, direction
        case "#":
            return current_position, direction
        case " ":
            if is_cube:
                new_position, new_direction = get_cube_map_movement(current_position, direction)
                return (new_position, new_direction) if matrix.get_symbol(new_position) == "." else (current_position, direction)

            match direction:
                case Direction.LEFT:
                    row = matrix.get_row(current_position.y)
                    index, symbol = next((matrix.width() - 1 - i, symbol) for i, symbol in enumerate(reversed(row)) if symbol != " ")
                    return Point(index, current_position.y) if symbol == "." else current_position, direction
                case Direction.RIGHT:
                    row = matrix.get_row(current_position.y)
                    index, symbol = next((i, symbol) for i, symbol in enumerate(row) if symbol != " ")
                    return Point(index, current_position.y) if symbol == "." else current_position, direction
                case Direction.UP:
                    column = matrix.get_column(current_position.x)
                    index, symbol = next((matrix.height() - 1 - i, symbol) for i, symbol in enumerate(reversed(column)) if symbol != " ")
                    return Point(current_position.x, index) if symbol == "." else current_position, direction
                case Direction.DOWN:
                    column = matrix.get_column(current_position.x)
                    index, symbol = next((i, symbol) for i, symbol in enumerate(column) if symbol != " ")
                    return Point(current_position.x, index) if symbol == "." else current_position, direction

    raise ValueError("Invalid direction of symbol")

def find_end_position(matrix: Matrix[str], starting_position: Point, path: list[str | int], is_cube: bool) -> tuple[Point, Direction]:
    current_direction = Direction.RIGHT
    current_position = starting_position

    for step in path:
        if isinstance(step, int):
            for _ in range(step):
                current_position, current_direction = move_step(matrix, current_position, current_direction, is_cube)
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

def calculate_position_points(position: Point, direction: Direction) -> int:
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

    return 1000 * (position.y + 1) + 4 * (position.x + 1) + direction_value

def silver_solution(lines: list[str]) -> int:
    matrix, starting_position, path = parse_input(lines)
    position, direction = find_end_position(matrix, starting_position, path, False)
    return calculate_position_points(position, direction)

def gold_solution(lines: list[str]) -> int:
    matrix, starting_position, path = parse_input(lines)
    position, direction = find_end_position(matrix, starting_position, path, True)
    return calculate_position_points(position, direction)
