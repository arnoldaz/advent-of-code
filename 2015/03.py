from utils.point2d import Direction2d, Point2d

def parse_input(lines: list[str]) -> list[Direction2d]:
    return [Direction2d.from_character(direction) for direction in lines[0]]

def silver_solution(lines: list[str]) -> int:
    directions = parse_input(lines)

    current_location = Point2d(0, 0)
    visited_locations = {current_location}

    for direction in directions:
        current_location += direction
        visited_locations.add(current_location)

    return len(visited_locations)

def gold_solution(lines: list[str]) -> int:
    directions = parse_input(lines)

    current_location_santa = Point2d(0, 0)
    current_location_robot = Point2d(0, 0)
    visited_locations = {current_location_santa, current_location_robot}

    for i in range(0, len(directions), 2):
        santa_direction, robot_direction = directions[i], directions[i+1]
        current_location_santa += santa_direction
        current_location_robot += robot_direction
        visited_locations.add(current_location_santa)
        visited_locations.add(current_location_robot)

    return len(visited_locations)
