from utils.grid import Grid
from utils.point2d import Direction2d, Point2d

def parse_input(lines: list[str]) -> tuple[Point2d, Direction2d, set[Point2d], int, int]:
    width, height = len(lines[0]), len(lines)
    walls = set[Point2d]()
    start_point: Point2d
    for point, symbol in Grid.iterate_lines(lines):
        if symbol == "#":
            walls.add(point)
        elif symbol == "^":
            start_point = point

    return start_point, Direction2d.UP, walls, width, height

def get_guard_path(start_point: Point2d, start_direction: Direction2d, walls: set[Point2d], width: int, height: int) -> list[tuple[Point2d, Direction2d]]:
    visited_positions = [(start_point, start_direction)]
    current_point = start_point
    current_direction = start_direction

    while True:
        current_point += current_direction
        if not current_point.in_bounds(width, height):
            break

        if current_point in walls:
            current_point -= current_direction
            current_direction = current_direction.turn_right()
            continue

        visited_positions.append((current_point, current_direction))

    return visited_positions

def check_loop(start_point: Point2d, start_direction: Direction2d, walls: set[Point2d], width: int, height: int) -> bool:
    repeating_positions = set[tuple[Point2d, Direction2d]]()
    current_point = start_point
    current_direction = start_direction

    while True:
        current_point += current_direction
        if not current_point.in_bounds(width, height):
            return False

        if current_point in walls:
            current_point -= current_direction
            current_direction = current_direction.turn_right()
            continue

        if (current_point, current_direction) in repeating_positions:
            return True

        repeating_positions.add((current_point, current_direction))

def silver_solution(lines: list[str]) -> int:
    start_point, start_direction, walls, width, height = parse_input(lines)
    visited_positions = get_guard_path(start_point, start_direction, walls, width, height)

    return len(set(position for position, _ in visited_positions))

def gold_solution(lines: list[str]) -> int:
    start_point, start_direction, walls, width, height = parse_input(lines)
    visited_positions = get_guard_path(start_point, start_direction, walls, width, height)

    loop_counter = 0
    checked_positions = set[Point2d]()
    for i, (position, _) in enumerate(visited_positions[1:]):
        if position in checked_positions:
            continue

        checked_positions.add(position)

        previous_position, previous_direction = visited_positions[i-1]
        if check_loop(previous_position, previous_direction, walls | {position}, width, height):
            loop_counter += 1

    return loop_counter
