from utils.point2d import Direction2d, Point2d

def parse_input(lines: list[str]) -> list[tuple[bool, int]]:
    steps: list[tuple[bool, int]] = []
    for step in lines[0].split(", "):
        is_right_turn = step[0] == "R"
        distance = int(step[1:])
        steps.append((is_right_turn, distance))

    return steps

def silver_solution(lines: list[str]) -> int:
    steps = parse_input(lines)

    current_location = Point2d(0, 0)
    current_direction = Direction2d.UP

    for is_right_turn, distance in steps:
        current_direction = current_direction.turn_right() if is_right_turn else current_direction.turn_left()
        current_location += current_direction * distance

    return Point2d.manhattan_distance(current_location, Point2d(0, 0))

def gold_solution(lines: list[str]) -> int:
    steps = parse_input(lines)

    current_location = Point2d(0, 0)
    current_direction = Direction2d.UP

    visited_locations = set[Point2d]([current_location])

    for is_right_turn, distance in steps:
        current_direction = current_direction.turn_right() if is_right_turn else current_direction.turn_left()

        found_double_location = False
        for _ in range(distance):
            current_location += current_direction
            if current_location in visited_locations:
                found_double_location = True
                break

            visited_locations.add(current_location)

        if found_double_location:
            break

    return Point2d.manhattan_distance(current_location, Point2d(0, 0))
