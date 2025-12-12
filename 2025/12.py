from itertools import groupby
from utils.point2d import Point2d

def parse_input(lines: list[str]) -> tuple[list[int], list[tuple[Point2d, list[int]]]]:
    groups = [list(group) for key, group in groupby(lines, key=lambda x: not x) if not key]

    shape_sizes = [sum(1 for x in "".join(shape) if x == "#") for shape in groups[:-1]]

    regions: list[tuple[Point2d, list[int]]] = []
    for region in groups[-1]:
        size, numbers = region.split(": ")
        regions.append((Point2d(*map(int, size.split("x"))), list(map(int, numbers.split()))))

    return shape_sizes, regions

def silver_solution(lines: list[str]) -> int:
    shape_sizes, regions = parse_input(lines)

    answer = 0
    for size, shape_counts in regions:
        area = size.x * size.y
        required_blocks = sum(a * b for a, b in zip(shape_sizes, shape_counts))
        if required_blocks <= area:
            answer += 1

    return answer

def gold_solution(_lines: list[str]) -> int:
    return 0
