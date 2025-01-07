from utils.matrix import Matrix
from utils.point import INVALID_POINT, Direction, Point

# TODO refactor

def parse_input(lines: list[str], is_gold: bool):
    empty_line = lines.index("")

    if not is_gold:
        grid = Matrix[str](lines[:empty_line], str)
    else:
        grid_lines = lines[:empty_line]
        for i, line in enumerate(grid_lines):
            grid_lines[i] = line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        grid = Matrix[str](grid_lines, str)

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
        case "[" if direction == Direction.DOWN or direction == Direction.UP:
            pair_symbol_position = next_position + Direction.RIGHT

            saved_further_positions = [[next_position, pair_symbol_position]]
            further_positions = [next_position + direction, pair_symbol_position + direction]
            while True:
                if grid.get_symbol(further_positions[-1]) == "[":
                    further_positions.append(further_positions[-1] + Direction.RIGHT)
                if grid.get_symbol(further_positions[0]) == "]":
                    further_positions.insert(0, further_positions[0] + Direction.LEFT)
                saved_further_positions.append([x for x in further_positions if grid.get_symbol(x) != "."])

                if any(grid.get_symbol(x) == "#" for x in further_positions):
                    return current_position
                elif all(grid.get_symbol(x) == "." for x in further_positions):
                    saved_further_positions.pop()
                    for saved_line in reversed(saved_further_positions):
                        for save_position in saved_line:
                            grid.set_symbol(save_position + direction, grid.get_symbol(save_position))
                            grid.set_symbol(save_position, ".")

                    grid.set_symbol(next_position, "@")
                    grid.set_symbol(current_position, ".")
                    return next_position
                else:
                    further_positions = [x + direction for x in further_positions if grid.get_symbol(x) == "[" or grid.get_symbol(x) == "]"]
                    continue
        case "[" if direction == Direction.RIGHT:
            pair_symbol_position = next_position + direction

            further_position = pair_symbol_position + direction
            further_symbol = grid.get_symbol(further_position)
            while True:
                match further_symbol:
                    case "[":
                        further_position += direction * 2
                        further_symbol = grid.get_symbol(further_position)
                        continue
                    case ".":
                        while further_position != next_position:
                            grid.set_symbol(further_position, "]")
                            grid.set_symbol(further_position - direction, "[")
                            further_position -= direction * 2
                        grid.set_symbol(next_position, "@")
                        grid.set_symbol(current_position, ".")
                        return next_position
                    case "#":
                        return current_position
        case "]" if direction == Direction.DOWN or direction == Direction.UP:
            pair_symbol_position = next_position + Direction.LEFT

            saved_further_positions = [[pair_symbol_position, next_position]]
            further_positions = [pair_symbol_position + direction, next_position + direction]
            while True:
                if grid.get_symbol(further_positions[-1]) == "[":
                    further_positions.append(further_positions[-1] + Direction.RIGHT)
                if grid.get_symbol(further_positions[0]) == "]":
                    further_positions.insert(0, further_positions[0] + Direction.LEFT)
                saved_further_positions.append([x for x in further_positions if grid.get_symbol(x) != "."])

                if any(grid.get_symbol(x) == "#" for x in further_positions):
                    return current_position
                elif all(grid.get_symbol(x) == "." for x in further_positions):
                    saved_further_positions.pop()
                    for saved_line in reversed(saved_further_positions):
                        for save_position in saved_line:
                            grid.set_symbol(save_position + direction, grid.get_symbol(save_position))
                            grid.set_symbol(save_position, ".")

                    grid.set_symbol(next_position, "@")
                    grid.set_symbol(current_position, ".")
                    return next_position
                else:
                    further_positions = [x + direction for x in further_positions if grid.get_symbol(x) == "[" or grid.get_symbol(x) == "]"]
                    continue
        case "]" if direction == Direction.LEFT:
            pair_symbol_position = next_position + direction

            further_position = pair_symbol_position + direction
            further_symbol = grid.get_symbol(further_position)
            while True:
                match further_symbol:
                    case "]":
                        further_position += direction * 2
                        further_symbol = grid.get_symbol(further_position)
                        continue
                    case ".":
                        while further_position != next_position:
                            grid.set_symbol(further_position, "[")
                            grid.set_symbol(further_position - direction, "]")
                            further_position -= direction * 2
                        grid.set_symbol(next_position, "@")
                        grid.set_symbol(current_position, ".")
                        return next_position
                    case "#":
                        return current_position
        case _:
            raise

    return INVALID_POINT

def calculate_points(grid: Matrix[str], is_gold: bool) -> int:
    boxes = grid.find_all_character_instances("O" if not is_gold else "[")

    result = 0
    for box in boxes:
        result += box.y * 100 + box.x

    return result

def silver_solution(lines: list[str]) -> int:
    grid, directions = parse_input(lines, False)
    starting_point = grid.find_first_character_instance("@")

    current_point = starting_point
    for direction in directions:
        current_point = move(grid, current_point, direction)

    return calculate_points(grid, False)

def gold_solution(lines: list[str]) -> int:
    grid, directions = parse_input(lines, True)
    starting_point = grid.find_first_character_instance("@")

    # os.system("cls")
    # grid.print()

    current_point = starting_point
    for direction in directions:
        current_point = move(grid, current_point, direction)
        # print("\033[0;0H")
        # grid.print()

    return calculate_points(grid, True)
