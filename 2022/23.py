import sys
from typing import Optional
from utils.point import INVALID_POINT, Direction, Point

NORTH_MOVEMENT_CHECK = [Direction.UP.value + Direction.LEFT.value, Direction.UP.value, Direction.UP.value + Direction.RIGHT.value]
SOUTH_MOVEMENT_CHECK = [Direction.DOWN.value + Direction.LEFT.value, Direction.DOWN.value, Direction.DOWN.value + Direction.RIGHT.value]
WEST_MOVEMENT_CHECK = [Direction.LEFT.value + Direction.UP.value, Direction.LEFT.value, Direction.LEFT.value + Direction.DOWN.value]
EAST_MOVEMENT_CHECK = [Direction.RIGHT.value + Direction.UP.value, Direction.RIGHT.value, Direction.RIGHT.value + Direction.DOWN.value]
VALID_DIRECTIONS = set(NORTH_MOVEMENT_CHECK + SOUTH_MOVEMENT_CHECK + WEST_MOVEMENT_CHECK + EAST_MOVEMENT_CHECK)

def parse_input(lines: list[str]) -> set[Point]:
    positions = set[Point]()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                positions.add(Point(x, y))

    return positions

def calculate_points(positions: set[Point]) -> int:
    min_x, max_x, min_y, max_y = sys.maxsize, -sys.maxsize, sys.maxsize, -sys.maxsize
    for point in positions:
        min_x = min(min_x, point.x)
        max_x = max(max_x, point.x)
        min_y = min(min_y, point.y)
        max_y = max(max_y, point.y)

    score = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Point(x, y) not in positions:
                score += 1

    return score

def perform_movement(positions: set[Point], round_count: Optional[int] = None) -> tuple[set[Point], int]:
    considerations: dict[Point, list[Point]] = { INVALID_POINT: [] }
    movement_order: list[tuple[list[Point], Direction]] = [
        (NORTH_MOVEMENT_CHECK, Direction.UP),
        (SOUTH_MOVEMENT_CHECK, Direction.DOWN),
        (WEST_MOVEMENT_CHECK, Direction.LEFT),
        (EAST_MOVEMENT_CHECK, Direction.RIGHT),
    ]

    i = 0
    while considerations:
        i += 1
        considerations = {}
        for position in positions:
            if not any((position + direction) in positions for direction in VALID_DIRECTIONS):
                continue

            for movement_check, movement_direction in movement_order:
                if not any((position + direction) in positions for direction in movement_check):
                    movement_new_position = position + movement_direction
                    if movement_new_position in considerations:
                        considerations[movement_new_position].append(position)
                    else:
                        considerations[movement_new_position] = [position]
                    break

        for destination, starts in considerations.items():
            if len(starts) != 1:
                continue

            start = starts[0]
            positions.remove(start)
            positions.add(destination)

        movement_order.append(movement_order.pop(0))

        if round_count is not None and i == round_count:
            break

    return positions, i

def silver_solution(lines: list[str]) -> int:
    positions = parse_input(lines)
    final_positions, _ = perform_movement(positions, 10)
    return calculate_points(final_positions)

def gold_solution(lines: list[str]) -> int: # runs for ~13s
    positions = parse_input(lines)
    _, iterations = perform_movement(positions)
    return iterations
