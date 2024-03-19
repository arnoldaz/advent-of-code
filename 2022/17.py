# pylint: disable=unused-argument

from typing import NamedTuple
from utils.point import Direction, Point

class Shape(NamedTuple):
    points: list[Point]
    width: int
    height: int

    def copy(self):
        new_points = [point.copy() for point in self.points]
        return Shape(new_points, self.width, self.height)


ROCK_COUNT = 2022
CHAMBER_WIDTH = 7
SHAPES: list[Shape] = [
    # @@@@
    Shape([Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)], 4, 1),
    # .@.
    # @@@
    # .@.
    Shape([Point(1, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 2)], 3, 3),
    # ..@
    # ..@
    # @@@
    Shape([Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2)], 3, 3),
    # @
    # @
    # @
    # @
    Shape([Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)], 1, 4),
    # @@
    # @@
    Shape([Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)], 2, 2),
]

def parse_input(lines: list[str]) -> list[Direction]:
    directions: list[Direction] = []
    assert len(lines) == 1
    for char in lines[0]:
        match char:
            case "<":
                directions.append(Direction.LEFT)
            case ">":
                directions.append(Direction.RIGHT)
            case _:
                raise ValueError(f"Unknown char '{char}'")

    return directions

def can_push(point_to_push: Point, push_direction: Direction, chamber: list[Point]) -> bool:
    new_point = point_to_push + push_direction
    if new_point in chamber:
        return False

    if new_point.x < 0 or new_point.y < 0 or new_point.x >= CHAMBER_WIDTH:
        return False

    return True

def fall_step(shape: Shape, chamber: list[Point], push_direction: Direction) -> bool:
    can_push_shape = all(can_push(x, push_direction, chamber) for x in shape.points)
    if can_push_shape:
        for point in shape.points:
            point.x += push_direction.value.x
            point.y += push_direction.value.y
        return True

    return False

def print_tower(chamber: list[Point], shape: Shape):
    for y in reversed(range(20)):
        for x in range(CHAMBER_WIDTH):
            if Point(x, y) in chamber or Point(x, y) in shape.points:
                print("#", end="")
            else:
                print(".", end="")
        print()



def silver_solution(lines: list[str]) -> int:
    directions = parse_input(lines)
    chamber: list[Point] = []

    current_direction_index = 0

    for i in range(ROCK_COUNT):
        highest_point = max((point.y + 1 for point in chamber), default=0)

        # print(highest_point, "AAA")

        shape = SHAPES[i % len(SHAPES)].copy()
        for point in shape.points:
            point.x += 2
            point.y += highest_point + 3

        # print("START:")
        # print_tower(chamber, shape)
        # print("===============")

        fall = True
        while fall:
            # if not all(can_push(x, Direction.UP, chamber) for x in shape.points):
            #     break

            fall_step(shape, chamber, directions[current_direction_index % len(directions)])
            current_direction_index += 1
            fall = fall_step(shape, chamber, Direction.UP) # uhhh need to make it down
            # print_tower(chamber, shape)
            # print("===============")

        chamber += shape.copy().points

    return max((point.y + 1 for point in chamber), default=0)

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
