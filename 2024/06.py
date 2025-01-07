from utils.matrix import Matrix
from utils.point import Direction, Point

# TODO
# https://github.com/theyoprst/adventofcode/blob/main/2024/06/main.go

WALL_SYMBOL = "#"
START_SYMBOLS = {
    "^": Direction.UP,
    ">": Direction.RIGHT,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
}

def rotate_90_right(direction: Direction) -> Direction:
    match direction:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP

    return Direction.NONE

def silver_solution(lines: list[str]) -> int:
    matrix = Matrix[str](lines, str)

    starting_point: Point
    starting_direction: Direction
    wall_locations: set[Point] = set()
    for y, line in enumerate(matrix.get_data()):
        for x, char in enumerate(line):
            if char == WALL_SYMBOL:
                wall_locations.add(Point(x, y))
            elif char in START_SYMBOLS.keys():
                starting_point = Point(x, y)
                starting_direction = START_SYMBOLS[char]

    width, height = matrix.width(), matrix.height()
    visited_positions = set[Point]([starting_point])
    current_point = starting_point
    current_direction = starting_direction

    while True:
        current_point += current_direction
        if current_point.x < 0 or current_point.x >= width:
            break

        if current_point.y < 0 or current_point.y >= height:
            break

        if current_point in wall_locations:
            current_point -= current_direction
            current_direction = rotate_90_right(current_direction)
            continue

        visited_positions.add(current_point)

    return len(visited_positions)

def check_loop(starting_point: Point, starting_direction: Direction, width: int, height: int, wall_locations: set[Point]) -> bool:
    current_point = starting_point
    current_direction = starting_direction

    repeating_positions = set[tuple[Point, Direction]]()

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


def gold_solution(lines: list[str]) -> int:
    matrix = Matrix[str](lines, str)

    starting_point: Point
    starting_direction: Direction
    wall_locations: set[Point] = set()
    for y, line in enumerate(matrix.get_data()):
        for x, char in enumerate(line):
            if char == WALL_SYMBOL:
                wall_locations.add(Point(x, y))
            elif char in START_SYMBOLS.keys():
                starting_point = Point(x, y)
                starting_direction = START_SYMBOLS[char]

    width, height = matrix.width(), matrix.height()
    visited_positions = set[Point]([starting_point])
    current_point = starting_point
    current_direction = starting_direction

    while True:
        current_point += current_direction
        if current_point.x < 0 or current_point.x >= width:
            break

        if current_point.y < 0 or current_point.y >= height:
            break

        if current_point in wall_locations:
            current_point -= current_direction
            current_direction = rotate_90_right(current_direction)
            continue

        visited_positions.add(current_point)

    # print("found visited positions", len(visited_positions))

    id = 0
    counter = 0
    for position in visited_positions:
        id += 1
        # print(id)
        is_loop = check_loop(starting_point, starting_direction, width, height, wall_locations.union(set([position])))
        if is_loop:
            counter += 1

    return counter
