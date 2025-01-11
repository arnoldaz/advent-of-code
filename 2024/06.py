

# TODO
# https://github.com/theyoprst/adventofcode/blob/main/2024/06/main.go

from utils import point
from utils.grid import Grid
from utils.point2d import Direction2d, Point2d


WALL_SYMBOL = "#"
START_SYMBOLS = {
    "^": Direction2d.UP,
    ">": Direction2d.RIGHT,
    "v": Direction2d.DOWN,
    "<": Direction2d.LEFT,
}

def rotate_90_right(direction: Direction2d) -> Direction2d:
    match direction:
        case Direction2d.UP:
            return Direction2d.RIGHT
        case Direction2d.RIGHT:
            return Direction2d.DOWN
        case Direction2d.DOWN:
            return Direction2d.LEFT
        case Direction2d.LEFT:
            return Direction2d.UP

    return Direction2d.NONE

def parse_input(lines: list[str]):
    grid = Grid[str](lines)
    walls = set(grid.find_all_character_instances("#"))
    start = grid.find_first_character_instance("^")

    return grid, walls, start, Direction2d.UP

def get_guard_path(grid: Grid[str], start_point: Point2d, start_direction: Direction2d, walls: set[Point2d]) -> list[tuple[Point2d, Direction2d]]:
    visited_positions = [(start_point, start_direction)]
    current_point = start_point
    current_direction = start_direction

    while True:
        current_point += current_direction
        if not grid.in_bounds(current_point):
            break

        if current_point in walls:
            current_point -= current_direction
            current_direction = current_direction.turn_right()
            continue

        visited_positions.append((current_point, current_direction))

    return visited_positions

def get_guard_path_loop(grid: Grid[str], start_point: Point2d, start_direction: Direction2d, walls: set[Point2d]) -> list[tuple[Point2d, Direction2d]]:
    visited_positions = [(start_point, start_direction)]
    current_point = start_point
    current_direction = start_direction

    while True:
        current_point += current_direction
        if not grid.in_bounds(current_point):
            # print("ioyut of bounds", current_point)
            break

        if current_point in walls:
            current_point -= current_direction
            current_direction = current_direction.turn_right()
            continue

        if (current_point, current_direction) in visited_positions:
            # print("returning loop")
            return visited_positions

        visited_positions.append((current_point, current_direction))

    return visited_positions

def silver_solution(lines: list[str]) -> int:
    grid, walls, start_point, start_direction = parse_input(lines)
    visited_positions = get_guard_path(grid, start_point, start_direction, walls)

    # for x in visited_positions:
    #     print(x)

    a = set(position for position, _ in visited_positions)
    # for x in a:
    #     grid.set_symbol(x, "@")

    # grid.print()

    return len(a)

def check_loop(starting_point: Point2d, starting_direction: Direction2d, width: int, height: int, wall_locations: set[Point2d]) -> bool:
    current_point = starting_point
    current_direction = starting_direction

    repeating_positions = set[tuple[Point2d, Direction2d]]()

    while True:
        current_point += current_direction
        if current_point.x < 0 or current_point.x >= width:
            return False

        if current_point.y < 0 or current_point.y >= height:
            return False

        if current_point in wall_locations:
            current_point -= current_direction
            current_direction = rotate_90_right(current_direction)
            continue

        if (current_point, current_direction) in repeating_positions:
            return True

        repeating_positions.add((current_point, current_direction))

def check_loop2(grid: Grid[str], start_point: Point2d, start_direction: Direction2d, walls: set[Point2d]) -> bool:
    repeating_positions = set[tuple[Point2d, Direction2d]]()
    current_point = start_point
    current_direction = start_direction

    while True:
        current_point += current_direction
        if not grid.in_bounds(current_point):
            return False

        if current_point in walls:
            current_point -= current_direction
            current_direction = current_direction.turn_right()
            continue

        if (current_point, current_direction) in repeating_positions:
            # print("found lupo", current_point, current_direction)
            return True

        repeating_positions.add((current_point, current_direction))


def gold_solution(lines: list[str]) -> int:
    grid, walls, start_point, start_direction = parse_input(lines)
    visited_positions = get_guard_path(grid, start_point, start_direction, walls)

    # for x in visited_positions:
    #     print(x)

    counter = 0
    check_positions = set()
    # loop_positions = set()
    for i, (position, _) in enumerate(visited_positions[1:]):
        if position in check_positions:
            continue
        check_positions.add(position)
        # if position in loop_positions:
        #     continue
        previous_position, previous_direction = visited_positions[i-1]
        is_loop = check_loop2(grid, previous_position, previous_direction, walls | {position})
        if is_loop:
            counter += 1
            # loop_positions.add(position)
    # return len(loop_positions)
    return counter
