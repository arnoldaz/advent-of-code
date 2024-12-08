from itertools import combinations
from utils.matrix import Matrix
from utils.point import Point

def parse_input(lines: list[str]) -> tuple[dict[str, set[Point]], int, int]:
    width, height = len(lines[0]), len(lines)
    locations: dict[str, set[Point]] = {}

    for y in range(height):
        for x in range(width):
            symbol = lines[y][x] 
            if symbol != ".":
                locations.setdefault(symbol, set()).add(Point(x, y))

    return locations, width, height

def silver_solution(lines: list[str]) -> int:
    locations, width, height = parse_input(lines)
    new_points = set[Point]()

    for key in locations.keys():
        # print(f"{key=}")
        points = locations[key]
        for first, second in combinations(points, 2):
            new_points.add(first - (second - first))
            new_points.add(second - (first - second))

    counter = 0
    for point in new_points:
        if point.in_bounds_2d(width, height):
            counter += 1

    # matrix = Matrix[str](lines, str)
    # for point in new_points:
    #     if matrix.in_bounds(point):
    #         matrix.set_symbol(point, "#")
    
    # matrix.print(1)


    return counter

def gold_solution(lines: list[str]) -> int:
    locations, width, height = parse_input(lines)
    new_points = set[Point]()

    for key in locations.keys():
        # print(f"{key=}")
        points = locations[key]
        for first, second in combinations(points, 2):
            first_back = second - first
            second_back = first - second
            
            first_back_moving = first - first_back
            second_back_moving = second - second_back
            while first_back_moving.in_bounds_2d(width, height):
                new_points.add(first_back_moving)
                first_back_moving -= first_back
            while second_back_moving.in_bounds_2d(width, height):
                new_points.add(second_back_moving)
                second_back_moving -= second_back

            # optimize this unnecessary addition
            new_points.add(first)
            new_points.add(second)


    # matrix = Matrix[str](lines, str)
    # for point in new_points:
    #     if matrix.in_bounds(point):
    #         matrix.set_symbol(point, "#")
    
    # matrix.print(1)


    return len(new_points)