from typing import NamedTuple
from utils.point import Point

class Brick(NamedTuple):
    start: Point
    end: Point

def parse_input(lines: list[str]) -> list[Brick]:
    bricks: list[Brick] = []
    for line in lines:
        start_str, end_str = line.split("~")
        start_x, start_y, start_z = [int(n) for n in start_str.split(",")]
        end_x, end_y, end_z = [int(n) for n in end_str.split(",")]

        bricks.append(Brick(Point(start_x, start_y, start_z), Point(end_x, end_y, end_z)))

    # Lowest brick at the start
    bricks.sort(key=lambda brick: min(brick.start.z, brick.end.z))
    return bricks

def brick_has_block(brick: Brick, block_position: Point) -> bool:
    good_x = brick.start.x <= block_position.x <= brick.end.x or brick.start.x >= block_position.x >= brick.end.x
    good_y = brick.start.y <= block_position.y <= brick.end.y or brick.start.y >= block_position.y >= brick.end.y
    good_z = brick.start.z <= block_position.z <= brick.end.z or brick.start.z >= block_position.z >= brick.end.z

    return good_x and good_y and good_z

def brick_can_fall(brick: Brick, all_bricks: list[Brick]) -> bool:
    # Already on the ground
    if brick.start.z == 1 or brick.end.z == 1:
        return False

    # on X axis
    if brick.start.y == brick.end.y and brick.start.z == brick.end.z:
        min_x = min(brick.start.x, brick.end.x)
        max_x = max(brick.start.x, brick.end.x)
        for x in range(min_x, max_x + 1):
            block_position = Point(x, brick.start.y, brick.start.z - 1)
            for other_brick in all_bricks:
                if brick_has_block(other_brick, block_position):
                    return False
    # on Y axis
    elif brick.start.x == brick.end.x and brick.start.z == brick.end.z:
        min_y = min(brick.start.y, brick.end.y)
        max_y = max(brick.start.y, brick.end.y)
        for y in range(min_y, max_y + 1):
            block_position = Point(brick.start.x, y, brick.start.z - 1)
            for other_brick in all_bricks:
                if brick_has_block(other_brick, block_position):
                    return False
    # on Z axis
    else:
        min_z = min(brick.start.z, brick.end.z)
        block_position = Point(brick.start.x, brick.start.y, min_z - 1)
        for other_brick in all_bricks:
            if brick_has_block(other_brick, block_position):
                return False

    return True

def fall_bricks(all_bricks: list[Brick]) -> tuple[list[Brick], int]:
    anything_fall = True

    new_bricks = all_bricks[:]
    fall_blocks = [False for _ in new_bricks]

    while anything_fall:
        anything_fall = False
        for i, brick in enumerate(new_bricks):
            if brick_can_fall(brick, new_bricks):
                new_bricks[i] = Brick(Point(brick.start.x, brick.start.y, brick.start.z - 1), Point(brick.end.x, brick.end.y, brick.end.z - 1))
                fall_blocks[i] = True
                anything_fall = True

    fall_amount = sum(1 for x in fall_blocks if x)

    return (new_bricks, fall_amount)

def can_disintegrate_brick(brick: Brick, all_bricks: list[Brick]) -> bool:
    all_bricks_without_checked = [x for x in all_bricks if x != brick]
    for other_brick in all_bricks_without_checked:
        if brick_can_fall(other_brick, all_bricks_without_checked):
            return False

    return True

def count_disintegratable_bricks(all_bricks: list[Brick]) -> int:
    counter = 0
    for brick in all_bricks:
        if can_disintegrate_brick(brick, all_bricks):
            counter += 1

    return counter

def count_not_disintegratable_brick_sum(all_bricks: list[Brick]) -> int:
    counter = 0
    for brick in all_bricks:
        _, amount = fall_bricks([x for x in all_bricks if x != brick])
        counter += amount

    return counter

def silver_solution(lines: list[str]) -> int: # runs for ~600s
    bricks = parse_input(lines)
    all_new_bricks, _ = fall_bricks(bricks)
    return count_disintegratable_bricks(all_new_bricks)

def gold_solution(lines: list[str]) -> int: # runs for ~2800s
    bricks = parse_input(lines)
    all_new_bricks, _ = fall_bricks(bricks)
    return count_not_disintegratable_brick_sum(all_new_bricks)
