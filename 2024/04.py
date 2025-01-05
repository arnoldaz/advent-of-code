from utils.grid import Grid
from utils.point2d import Point2d

def silver_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)
    xmas_counter = 0

    for point in grid.find_all_character_instances("X"):
        neighbors = grid.get_neighbors_with_directions(point, True)
        for neighbor_point, neighbor_direction in neighbors:
            if grid.get_symbol(neighbor_point) != "M":
                continue

            a_point = neighbor_point + neighbor_direction
            if not grid.in_bounds(a_point) or grid.get_symbol(a_point) != "A":
                continue

            s_point = a_point + neighbor_direction
            if not grid.in_bounds(s_point) or grid.get_symbol(s_point) != "S":
                continue

            xmas_counter += 1

    return xmas_counter

def gold_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)
    a_frequency: dict[Point2d, int] = {}

    for point in grid.find_all_character_instances("A"):
        diagonal_neighbors = grid.get_neighbors_with_directions(point, True, True)
        for neighbor_point, neighbor_direction in diagonal_neighbors:
            if grid.get_symbol(neighbor_point) != "M":
                continue

            s_point = point - neighbor_direction
            if not grid.in_bounds(s_point) or grid.get_symbol(s_point) != "S":
                continue

            a_frequency[point] = a_frequency.get(point, 0) + 1

    return sum(1 for frequency in a_frequency.values() if frequency == 2)
