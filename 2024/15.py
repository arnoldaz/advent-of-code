import sys

from utils.grid import Grid
from utils.point2d import Direction2d, Point2d

def parse_input(lines: list[str], is_gold: bool) -> tuple[Grid[str], list[Direction2d], Point2d]:
    empty_line = lines.index("")

    if not is_gold:
        grid = Grid[str](lines[:empty_line])
    else:
        grid_lines = lines[:empty_line]
        for i, line in enumerate(grid_lines):
            grid_lines[i] = line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        grid = Grid[str](grid_lines)

    directions = [Direction2d.from_character(direction) for direction in "".join(lines[empty_line:])]
    starting_point = grid.find_first_character_instance("@")

    return grid, directions, starting_point

def move(grid: Grid[str], current_position: Point2d, direction: Direction2d) -> Point2d:
    next_position = current_position + direction
    next_symbol = grid.get_symbol(next_position)

    def push_large_box_vertical(pair_symbol_direction: Direction2d):
        pair_symbol_position = next_position + pair_symbol_direction

        if pair_symbol_direction == Direction2d.LEFT:
            saved_further_positions = [[pair_symbol_position, next_position]]
            further_positions = [pair_symbol_position + direction, next_position + direction]
        else:
            saved_further_positions = [[next_position, pair_symbol_position]]
            further_positions = [next_position + direction, pair_symbol_position + direction]

        while True:
            if grid.get_symbol(further_positions[-1]) == "[":
                further_positions.append(further_positions[-1] + Direction2d.RIGHT)
            if grid.get_symbol(further_positions[0]) == "]":
                further_positions.insert(0, further_positions[0] + Direction2d.LEFT)
            saved_further_positions.append([x for x in further_positions if grid.get_symbol(x) != "."])

            if any(grid.get_symbol(x) == "#" for x in further_positions):
                return current_position
            if all(grid.get_symbol(x) == "." for x in further_positions):
                saved_further_positions.pop()
                for saved_line in reversed(saved_further_positions):
                    for save_position in saved_line:
                        grid.set_symbol(save_position + direction, grid.get_symbol(save_position))
                        grid.set_symbol(save_position, ".")

                grid.set_symbol(next_position, "@")
                grid.set_symbol(current_position, ".")
                return next_position

            further_positions = [x + direction for x in further_positions if grid.get_symbol(x) == "[" or grid.get_symbol(x) == "]"]
            continue

    def push_large_box_horizontal(push_direction: Direction2d):
        bracket_symbol, bracket_pair_symbol = ("[", "]") if push_direction == Direction2d.RIGHT else ("]", "[")
        pair_symbol_position = next_position + direction

        further_position = pair_symbol_position + direction
        further_symbol = grid.get_symbol(further_position)
        while True:
            match further_symbol:
                case "[" | "]":
                    further_position += direction * 2
                    further_symbol = grid.get_symbol(further_position)
                    continue
                case ".":
                    while further_position != next_position:
                        grid.set_symbol(further_position, bracket_pair_symbol)
                        grid.set_symbol(further_position - direction, bracket_symbol)
                        further_position -= direction * 2
                    grid.set_symbol(next_position, "@")
                    grid.set_symbol(current_position, ".")
                    return next_position
                case "#":
                    return current_position

    match next_symbol:
        case ".":
            grid.set_symbol(next_position, "@")
            grid.set_symbol(current_position, ".")
            return next_position
        case "#":
            return current_position
        case "O":
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
        case "[" if direction in (Direction2d.DOWN, Direction2d.UP):
            return push_large_box_vertical(Direction2d.RIGHT)
        case "[" if direction == Direction2d.RIGHT:
            return push_large_box_horizontal(Direction2d.RIGHT)
        case "]" if direction in (Direction2d.DOWN, Direction2d.UP):
            return push_large_box_vertical(Direction2d.LEFT)
        case "]" if direction == Direction2d.LEFT:
            return push_large_box_horizontal(Direction2d.LEFT)
        case _:
            raise RuntimeError("Impossible movement")

    return Point2d(sys.maxsize, sys.maxsize)

def calculate_points(grid: Grid[str], is_gold: bool) -> int:
    boxes = grid.find_all_character_instances("O" if not is_gold else "[")
    return sum(box.y * 100 + box.x for box in boxes)

def silver_solution(lines: list[str]) -> int:
    grid, directions, starting_point = parse_input(lines, False)

    current_point = starting_point
    for direction in directions:
        current_point = move(grid, current_point, direction)

    return calculate_points(grid, False)

def gold_solution(lines: list[str]) -> int:
    grid, directions, starting_point = parse_input(lines, True)

    current_point = starting_point
    for direction in directions:
        current_point = move(grid, current_point, direction)

    return calculate_points(grid, True)
