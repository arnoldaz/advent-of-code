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

def perform_steps(steps: list[tuple[Direction, int]]) -> int:
    head_position, tail_position = Point(0, 0), Point(0, 0)
    tail_position_set: set[Point] = set([tail_position])

    for (step_direction, step_count) in steps:
        for _ in range(step_count):
            head_position += step_direction
            if not is_tail_adjacent(head_position, tail_position):
                tail_position += get_diagonal_step(head_position, tail_position)
                tail_position_set.add(tail_position)

    return len(tail_position_set)

def perform_steps_gold(steps: list[tuple[Direction, int]], tail_count: int) -> int:
    tail_positions = [Point(0, 0) for _ in range(tail_count + 1)]
    last_tail_position_set: list[Point] = list([tail_positions[-1]])

    for (step_direction, step_count) in steps:
        for _ in range(step_count):
            tail_positions[0] += step_direction

            for i in range(1, len(tail_positions)):
                if not is_tail_adjacent(tail_positions[i-1], tail_positions[i]):
                    tail_positions[i] += get_diagonal_step(tail_positions[i-1], tail_positions[i])
                    if i == len(tail_positions) - 1:
                        last_tail_position_set.append(tail_positions[i])

    return len(set(last_tail_position_set))

def silver_solution(lines: list[str]) -> int:
    steps = parse_input(lines)
    result = perform_steps(steps)

    return result

def gold_solution(lines: list[str]) -> int:
    steps = parse_input(lines)
    result = perform_steps_gold(steps, 9)

    return result
