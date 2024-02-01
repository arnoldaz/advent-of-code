from utils.matrix import Matrix
from utils.point import INVALID_POINT, Direction, Point, reverse_direction

def parse_input(lines: list[str]) -> tuple[Matrix[str], Point]:
    matrix = Matrix(lines, str)
    return matrix, matrix.find_first_character_instance("S") or INVALID_POINT

def get_starting_direction(matrix: Matrix[str], start: Point) -> Direction:
    if matrix.get_symbol(start + Direction.UP) in ("|", "F", "7"):
        return Direction.UP

    if matrix.get_symbol(start + Direction.DOWN) in ("|", "L", "J"):
        return Direction.DOWN

    if matrix.get_symbol(start + Direction.LEFT) in ("-", "F", "L"):
        return Direction.LEFT

    if matrix.get_symbol(start + Direction.RIGHT) in ("-", "J", "7"):
        return Direction.RIGHT

    return Direction.NONE

def get_next_location(symbol: str, incoming_direction: Direction) -> Direction:
    match symbol:
        case "|":
            if incoming_direction == Direction.UP:
                return Direction.UP
            if incoming_direction == Direction.DOWN:
                return Direction.DOWN
        case "-":
            if incoming_direction == Direction.LEFT:
                return Direction.LEFT
            if incoming_direction == Direction.RIGHT:
                return Direction.RIGHT
        case "L":
            if incoming_direction == Direction.LEFT:
                return Direction.UP
            if incoming_direction == Direction.DOWN:
                return Direction.RIGHT
        case "J":
            if incoming_direction == Direction.RIGHT:
                return Direction.UP
            if incoming_direction == Direction.DOWN:
                return Direction.LEFT
        case "7":
            if incoming_direction == Direction.RIGHT:
                return Direction.DOWN
            if incoming_direction == Direction.UP:
                return Direction.LEFT
        case "F":
            if incoming_direction == Direction.LEFT:
                return Direction.DOWN
            if incoming_direction == Direction.UP:
                return Direction.RIGHT
        case "S":
            return Direction.NONE

    raise RuntimeError("Impossible to reach with valid input")

def get_start_char_replacement(first_segment_direction: Direction, final_segment_direction: Direction) -> str:
    match first_segment_direction, final_segment_direction:
        case (Direction.UP, Direction.DOWN) | (Direction.DOWN, Direction.UP):
            return "|"
        case (Direction.LEFT, Direction.RIGHT) | (Direction.RIGHT, Direction.LEFT):
            return "-"
        case (Direction.UP, Direction.RIGHT) | (Direction.RIGHT, Direction.UP):
            return "L"
        case (Direction.UP, Direction.LEFT) | (Direction.LEFT, Direction.UP):
            return "J"
        case(Direction.DOWN, Direction.LEFT) | (Direction.LEFT, Direction.DOWN):
            return "7"
        case (Direction.DOWN, Direction.RIGHT) | (Direction.RIGHT, Direction.DOWN):
            return "F"

    raise RuntimeError("Impossible to reach with valid input")

def get_pipe_path(matrix: Matrix[str], start: Point) -> dict[Point, str]:
    current_direction = get_starting_direction(matrix, start)
    current_location = start + current_direction

    first_segment_direction = current_direction
    final_path: dict[Point, str] = {}
    while True:
        symbol = matrix.get_symbol(current_location) or ""
        final_path[current_location] = symbol

        new_direction = get_next_location(symbol, current_direction)
        current_location += new_direction
        if current_location == start:
            final_path[current_location] = get_start_char_replacement(first_segment_direction, reverse_direction(new_direction))
            break

        current_direction = new_direction

    return final_path

def calculate_internal_tile_count(matrix: Matrix[str], pipe_path: dict[Point, str]) -> int:
    internal_tile_count = 0
    for y in range( matrix.height()):
        winding_number = 0
        for x in range(matrix.width()):
            char = pipe_path.get(Point(x, y), ".")
            match char:
                case "." if winding_number % 4 == 2:
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

def silver_solution(lines: list[str]) -> int:
    matrix, starting_point = parse_input(lines)
    return len(get_pipe_path(matrix, starting_point)) // 2

def gold_solution(lines: list[str]) -> int:
    matrix, starting_point = parse_input(lines)
    pipe_path = get_pipe_path(matrix, starting_point)
    return calculate_internal_tile_count(matrix, pipe_path)
