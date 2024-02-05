from utils.point import Direction, Point

def parse_input(lines: list[str]) -> list[tuple[Direction, int]]:
    steps: list[tuple[Direction, int]] = []
    for line in lines:
        direction_letter, step_count = line.split()
        match direction_letter:
            case "U":
                direction = Direction.UP
            case "D":
                direction = Direction.DOWN
            case "L":
                direction = Direction.LEFT
            case "R":
                direction = Direction.RIGHT
            case _:
                direction = Direction.NONE

        steps.append((direction, int(step_count)))
    return steps

def is_tail_adjacent(head_position: Point, tail_position: Point) -> bool:
    is_x_adjacent = head_position.x - 1 <= tail_position.x <= head_position.x + 1
    is_y_adjacent = head_position.y - 1 <= tail_position.y <= head_position.y + 1

    return is_x_adjacent and is_y_adjacent

def get_diagonal_step(head_position: Point, tail_position: Point) -> Point:
    x_diff = head_position.x - tail_position.x
    y_diff = head_position.y - tail_position.y

    if x_diff not in (1, -1):
        x_diff //= 2

    if y_diff not in (1, -1):
        y_diff //= 2

    return Point(x_diff, y_diff)

def count_tail_unique_positions(steps: list[tuple[Direction, int]], knot_count: int) -> int:
    knot_positions = [Point(0, 0) for _ in range(knot_count)]
    tail_positions = set([knot_positions[-1]])

    for (step_direction, step_count) in steps:
        for _ in range(step_count):
            knot_positions[0] += step_direction
            for i in range(1, len(knot_positions)):
                if not is_tail_adjacent(knot_positions[i-1], knot_positions[i]):
                    knot_positions[i] += get_diagonal_step(knot_positions[i-1], knot_positions[i])

            tail_positions.add(knot_positions[-1])

    return len(tail_positions)

def silver_solution(lines: list[str]) -> int:
    steps = parse_input(lines)
    return count_tail_unique_positions(steps, 2)

def gold_solution(lines: list[str]) -> int:
    steps = parse_input(lines)
    return count_tail_unique_positions(steps, 10)
