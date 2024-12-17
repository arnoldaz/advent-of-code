# pylint: disable=unused-argument

from utils.matrix import Matrix
from utils.point import INVALID_POINT, Direction, Point


def parse_input(lines: list[str]):
    empty_line = lines.index("")
    
    grid = Matrix[str](lines[:empty_line], str)
    direction_string = "".join(lines[empty_line:])
    
    directions: list[Direction] = []
    for direction in direction_string:
        match direction:
            case "^":
                directions.append(Direction.UP)
            case "v":
                directions.append(Direction.DOWN)
            case ">":
                directions.append(Direction.RIGHT)
            case "<":
                directions.append(Direction.LEFT)
            case _:
                raise ValueError("no way bueno")

    return grid, directions

def move(grid: Matrix[str], current_position: Point, direction: Direction) -> Point:
    next_position = current_position + direction
    next_symbol = grid.get_symbol(next_position)

    match next_symbol:
        case ".":
            grid.set_symbol(next_position, "@")
            grid.set_symbol(current_position, ".")
            return next_position
        case "#":
            return current_position
        case "O":
            #            @OOO.#
            further_position = next_position + direction
            further_symbol = grid.get_symbol(further_position)
            while True:
                match further_symbol:
                    case "O":
                        further_position += direction
                        further_symbol = grid.get_symbol(further_position)
                        continue
                    case ".":
                        grid.set_symbol(further_position, "O")
                        grid.set_symbol(next_position, "@")
                        grid.set_symbol(current_position, ".")
                        return next_position
                    case "#":
                        return current_position

    return INVALID_POINT

def calculate_points(grid: Matrix[str]) -> int:
    boxes = grid.find_all_character_instances("O")
    
    result = 0
    for box in boxes:
        result += box.y * 100 + box.x

    return result

def silver_solution(lines: list[str]) -> int:
    grid, directions = parse_input(lines)
    starting_point = grid.find_first_character_instance("@")

    # print("START=========================================")
    # grid.print()
    # i = 1

    current_point = starting_point
    for direction in directions:
        # print(f"MOVE {i} DIRECTION {direction} =========================================")
        # i+=1
        current_point = move(grid, current_point, direction)
        # grid.print()

    return calculate_points(grid)

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
