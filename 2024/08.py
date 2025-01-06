from itertools import combinations

from utils.grid import Grid
from utils.point2d import Point2d

def parse_input(lines: list[str]) -> tuple[dict[str, set[Point2d]], int, int]:
    width, height = len(lines[0]), len(lines)
    locations: dict[str, set[Point2d]] = {}

    for point, symbol in Grid.iterate_lines(lines):
        if symbol != ".":
            locations.setdefault(symbol, set()).add(point)

    return locations, width, height

def silver_solution(lines: list[str]) -> int:
    locations, width, height = parse_input(lines)
    antinodes = set[Point2d]()

    for points in locations.values():
        for first, second in combinations(points, 2):
            antinodes.add(first - (second - first))
            antinodes.add(second - (first - second))

    return sum(1 for point in antinodes if point.in_bounds(width, height))

def gold_solution(lines: list[str]) -> int:
    locations, width, height = parse_input(lines)
    antinodes = set[Point2d]()

    for points in locations.values():
        for first, second in combinations(points, 2):
            first_back = second - first
            second_back = first - second

            first_back_moving = first - first_back
            second_back_moving = second - second_back
            while first_back_moving.in_bounds(width, height):
                antinodes.add(first_back_moving)
                first_back_moving -= first_back
            while second_back_moving.in_bounds(width, height):
                antinodes.add(second_back_moving)
                second_back_moving -= second_back

            antinodes.add(first)
            antinodes.add(second)

    return len(antinodes)
