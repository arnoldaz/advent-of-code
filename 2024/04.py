from utils.matrix import Matrix
from utils.point import Point

def silver_solution(lines: list[str]) -> int:
    matrix = Matrix[str](lines, str)

    xmas_counter = 0

    height, width = matrix.height(), matrix.width()
    for y in range(height):
        for x in range(width):
            symbol = matrix.get_symbol(Point(x, y))
            if symbol != "X":
                continue

            neighbors = matrix.get_neighbors_diagonal(Point(x, y))
            for neighbor_point, neighbor_direction in neighbors:
                if matrix.get_symbol(neighbor_point) != "M":
                    continue

                a_point = neighbor_point + neighbor_direction
                if not matrix.in_bounds(a_point) or matrix.get_symbol(a_point) != "A":
                    continue

                s_point = a_point + neighbor_direction
                if not matrix.in_bounds(s_point) or matrix.get_symbol(s_point) != "S":
                    continue

                xmas_counter += 1

    return xmas_counter

def gold_solution(lines: list[str]) -> int:
    matrix = Matrix[str](lines, str)

    xmas_counter = 0
    a_frequency: dict[Point, int] = {}

    height, width = matrix.height(), matrix.width()
    for y in range(height):
        for x in range(width):
            symbol = matrix.get_symbol(Point(x, y))
            if symbol != "M":
                continue

            neighbors = matrix.get_neighbors_only_diagonal(Point(x, y))
            for neighbor_point, neighbor_direction in neighbors:
                if matrix.get_symbol(neighbor_point) != "A":
                    continue

                s_point = neighbor_point + neighbor_direction
                if not matrix.in_bounds(s_point) or matrix.get_symbol(s_point) != "S":
                    continue

                if neighbor_point in a_frequency:
                    a_frequency[Point(neighbor_point.x, neighbor_point.y)] = a_frequency[Point(neighbor_point.x, neighbor_point.y)] + 1
                else:
                    a_frequency[Point(neighbor_point.x, neighbor_point.y)] = 1

    for point, frequency in a_frequency.items():
        if frequency == 2:
            xmas_counter += 1

    return xmas_counter
