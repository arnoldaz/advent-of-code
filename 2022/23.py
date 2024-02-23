import sys
from utils.point import INVALID_POINT, Direction, Point

NORTH_MOVEMENT_CHECK = [Direction.UP.value + Direction.LEFT.value, Direction.UP.value, Direction.UP.value + Direction.RIGHT.value]
SOUTH_MOVEMENT_CHECK = [Direction.DOWN.value + Direction.LEFT.value, Direction.DOWN.value, Direction.DOWN.value + Direction.RIGHT.value]
WEST_MOVEMENT_CHECK = [Direction.LEFT.value + Direction.UP.value, Direction.LEFT.value, Direction.LEFT.value + Direction.DOWN.value]
EAST_MOVEMENT_CHECK = [Direction.RIGHT.value + Direction.UP.value, Direction.RIGHT.value, Direction.RIGHT.value + Direction.DOWN.value]

def parse_input(lines: list[str]) -> set[Point]:
    positions = set[Point]()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                positions.add(Point(x, y))

    return positions

VALID_DIRECTIONS = [
    Direction.UP.value + Direction.LEFT.value,
    Direction.UP.value,
    Direction.UP.value + Direction.RIGHT.value,
    Direction.RIGHT.value,
    Direction.RIGHT.value + Direction.DOWN.value,
    Direction.DOWN.value,
    Direction.DOWN.value + Direction.LEFT.value,
    Direction.LEFT.value,
]

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

def silver_solution(lines: list[str]) -> int:
    positions = parse_input(lines)

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
        # print(movement_order)
        considerations = {}
        for position in positions:
            if not any((position + direction) in positions for direction in VALID_DIRECTIONS):
                # print("position", position)
                continue

            for movement_check, movement_direction in movement_order:
                if not any((position + direction) in positions for direction in movement_check):
                    # print("nigga", movement_direction, position)
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

        # print("cons", considerations)

        # move to end
        movement_order.append(movement_order.pop(0))

        if i == 10:
            break

        # for y in range(-10, 20):
        #     for x in range(-10, 20):
        #         if Point(x, y) in positions:
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        # print("===========", i)
    # for x in considerations:
    #     print(x, considerations[x])

    # for y in range(-10, 20):
    #     for x in range(-10, 20):
    #         if Point(x, y) in positions:
    #             print("#", end="")
    #         else:
    #             print(".", end="")
    #     print()
    # print("===========", i)

    return calculate_points(positions)

def gold_solution(lines: list[str]) -> int:
    positions = parse_input(lines)

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
        # print(movement_order)
        considerations = {}
        for position in positions:
            if not any((position + direction) in positions for direction in VALID_DIRECTIONS):
                # print("position", position)
                continue

            for movement_check, movement_direction in movement_order:
                if not any((position + direction) in positions for direction in movement_check):
                    # print("nigga", movement_direction, position)
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

        # print("cons", considerations)

        # move to end
        movement_order.append(movement_order.pop(0))

        # if i == 10:
        #     break

        # for y in range(-10, 20):
        #     for x in range(-10, 20):
        #         if Point(x, y) in positions:
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        # print("===========", i)
    # for x in considerations:
    #     print(x, considerations[x])

    # for y in range(-10, 20):
    #     for x in range(-10, 20):
    #         if Point(x, y) in positions:
    #             print("#", end="")
    #         else:
    #             print(".", end="")
    #     print()
    # print("===========", i)

    return i

    # return calculate_points(positions)


# if not any((position + direction) in positions for direction in SOUTH_MOVEMENT_CHECK):
#     down_position = position + Direction.DOWN
#     if down_position in considerations:
#         considerations[down_position].append(position)
#     else:
#         considerations[down_position] = [position]
#     continue

# if not any((position + direction) in positions for direction in WEST_MOVEMENT_CHECK):
#     left_position = position + Direction.LEFT
#     if left_position in considerations:
#         considerations[left_position].append(position)
#     else:
#         considerations[left_position] = [position]
#     continue

# if not any((position + direction) in positions for direction in EAST_MOVEMENT_CHECK):
#     right_position = position + Direction.RIGHT
#     if right_position in considerations:
#         considerations[right_position].append(position)
#     else:
#         considerations[right_position] = [position]
#     continue
