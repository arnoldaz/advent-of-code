# pylint: disable-all

from itertools import combinations
from utils.point2d import Point2d

def parse_input(lines: list[str]) -> list[Point2d]:
    return [Point2d(*map(int, line.split(","))) for line in lines]

def silver_solution(lines: list[str]) -> int:
    points = parse_input(lines)
    
    max_area = 0
    for point1, point2 in combinations(points, 2):
        width = abs(point1.x - point2.x) + 1
        height = abs(point1.y - point2.y) + 1

        area = width * height
        if area > max_area:
            max_area = area

    return max_area

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
