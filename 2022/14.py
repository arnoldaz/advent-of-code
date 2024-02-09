# pylint: disable=unused-argument

import sys
from utils.matrix import Matrix
from utils.point import Direction, Point

from colorama import Fore

WALL_SYMBOL = 1
SAND_SYMBOL = 2

def parse_input(lines: list[str]) -> Matrix[int]:
    width, height = 600, 600
    data = [[0 for _ in range(width)] for _ in range(height)]

    for line in lines:
        corners = [Point(int(x), int(y)) for corner_pair in line.split(" -> ") for x, y in [corner.split(",") for corner in corner_pair.split()]]
        for corner1, corner2 in zip(corners, corners[1:]):
            if corner1.x == corner2.x:
                for y in range(min(corner1.y, corner2.y), max(corner1.y, corner2.y) + 1):
                    data[y][corner1.x] = WALL_SYMBOL
            elif corner1.y == corner2.y:
                for x in range(min(corner1.x, corner2.x), max(corner1.x, corner2.x) + 1):
                    data[corner1.y][x] = WALL_SYMBOL
            else:
                raise ValueError("Impossible input")

    return Matrix[int](data, int)

LEEWAY_COUNT = 400

def parse_input2(lines: list[str]) -> tuple[Matrix[int], Point]:
    map_lines: list[tuple[Point, Point]] = []

    for line in lines:
        corners = [Point(int(x), int(y)) for corner_pair in line.split(" -> ") for x, y in [corner.split(",") for corner in corner_pair.split()]]
        for corner1, corner2 in zip(corners, corners[1:]):
            if corner1.x == corner2.x:
                map_lines.append((Point(corner1.x, min(corner1.y, corner2.y)), Point(corner1.x, max(corner1.y, corner2.y))))
            elif corner1.y == corner2.y:
                map_lines.append((Point(min(corner1.x, corner2.x), corner1.y), Point(max(corner1.x, corner2.x), corner1.y)))
            else:
                raise ValueError("Impossible input")

    max_x, max_y, min_x, min_y = 0, 0, sys.maxsize, sys.maxsize
    for start, end in map_lines:
        if start.x < min_x:
            min_x = start.x
        if start.x > max_x:
            max_x = start.x
        if end.x < min_x:
            min_x = end.x
        if end.x > max_x:
            max_x = end.x
        if start.y < min_y:
            min_y = start.y
        if start.y > max_y:
            max_y = start.y
        if end.y < min_y:
            min_y = end.y
        if end.y > max_y:
            max_y = end.y

    # print(max_x, max_y, min_x, min_y)

    width = max_x - min_x + LEEWAY_COUNT
    height = max_y - min_y + LEEWAY_COUNT
    data = [[0 for _ in range(width)] for _ in range(height)]
    offset = Point(min_x - LEEWAY_COUNT // 2, min_y - LEEWAY_COUNT // 2)

    for start, end in map_lines:
        if start.x == end.x:
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                data[y - offset.y][start.x - offset.x] = WALL_SYMBOL
        elif start.y == end.y:
            for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                data[start.y - offset.y][x - offset.x] = WALL_SYMBOL
        else:
            raise ValueError("Impossible input")

    for x in range(width):
        data[max_y + 2 - offset.y][x] = WALL_SYMBOL

    return Matrix[int](data, int), offset


def drop_sand(matrix: Matrix[int], sand_start: Point) -> bool:
    column = matrix.get_column(sand_start.x)
    first_obstacle_y = next((i for i, value in enumerate(column) if value > 0 and i > sand_start.y), None)
    if first_obstacle_y is None:
        return False

    first_obstacle = Point(sand_start.x, first_obstacle_y)

    obstacle_left = first_obstacle + Direction.LEFT
    if matrix.get_symbol(obstacle_left) == 0:
        return drop_sand(matrix, obstacle_left)

    obstacle_right = first_obstacle + Direction.RIGHT
    if matrix.get_symbol(obstacle_right) == 0:
        return drop_sand(matrix, obstacle_right)

    matrix.set_symbol(first_obstacle + Direction.UP, SAND_SYMBOL)
    return True

def drop_sand_offset(matrix: Matrix[int], sand_start: Point, offset: Point) -> bool:
    sand_start -= offset

    if matrix.get_symbol(sand_start) == SAND_SYMBOL:
        return False

    column = matrix.get_column(sand_start.x)
    first_obstacle_y = next((i for i, value in enumerate(column) if value > 0 and i > sand_start.y), None)
    if first_obstacle_y is None:
        return False

    first_obstacle = Point(sand_start.x, first_obstacle_y)

    obstacle_left = first_obstacle + Direction.LEFT
    if matrix.get_symbol(obstacle_left) == 0:
        return drop_sand(matrix, obstacle_left)

    obstacle_right = first_obstacle + Direction.RIGHT
    if matrix.get_symbol(obstacle_right) == 0:
        return drop_sand(matrix, obstacle_right)

    matrix.set_symbol(first_obstacle + Direction.UP, SAND_SYMBOL)
    return True

def count_sand(matrix: Matrix[int]) -> int:
    counter = 0
    for line in matrix.get_data():
        for number in line:
            if number == SAND_SYMBOL:
                counter += 1

    return counter

def silver_solution(lines: list[str]) -> int:
    matrix = parse_input(lines)
    sand_start = Point(500, 0)

    while drop_sand(matrix, sand_start):
        # for y in range(15):
        #     for x in range(490, 510):
        #         symbol = matrix.get_symbol(Point(x, y))
        #         if symbol == 1:
        #             print(f"{Fore.BLUE}{symbol}{Fore.RESET}", end="")
        #         elif symbol == 2:
        #             print(f"{Fore.RED}{symbol}{Fore.RESET}", end="")
        #         else:
        #             print(symbol, end="")
        #     print()
        pass

    for y in range(matrix.height()):
        for x in range(matrix.width()):
            symbol = matrix.get_symbol(Point(x, y))
            if symbol == 1:
                print(f"{Fore.BLUE}{symbol}{Fore.RESET}", end="")
            elif symbol == 2:
                print(f"{Fore.RED}{symbol}{Fore.RESET}", end="")
            else:
                print(symbol, end="")
        print()
    print("==============================================")

    return count_sand(matrix)

def gold_solution(lines: list[str]) -> int:
    matrix, offset = parse_input2(lines)
    sand_start = Point(500, 0)

    while drop_sand_offset(matrix, sand_start, offset):
        # for y in range(matrix.height()):
        #     for x in range(matrix.width()):
        #         symbol = matrix.get_symbol(Point(x, y))
        #         if symbol == 1:
        #             print(f"{Fore.BLUE}{symbol}{Fore.RESET}", end="")
        #         elif symbol == 2:
        #             print(f"{Fore.RED}{symbol}{Fore.RESET}", end="")
        #         else:
        #             print(symbol, end="")
        #     print()
        # print("==============================================")
        pass


    for y in range(matrix.height()):
        for x in range(matrix.width()):
            symbol = matrix.get_symbol(Point(x, y))
            if symbol == 1:
                print(f"{Fore.BLUE}{symbol}{Fore.RESET}", end="")
            elif symbol == 2:
                print(f"{Fore.RED}{symbol}{Fore.RESET}", end="")
            else:
                print(symbol, end="")
        print()
    print("==============================================")

    return count_sand(matrix)
