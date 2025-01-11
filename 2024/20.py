import queue
import sys

from utils.grid import Grid
from utils.point2d import Point2d

def parse_input(lines: list[str]) -> tuple[Grid[str], Point2d, Point2d]:
    grid = Grid[str](lines)
    start = grid.find_first_character_instance("S")
    end = grid.find_first_character_instance("E")

    return grid, start, end

def djikstra_search(grid: Grid[str], start: Point2d, end: Point2d) -> dict[Point2d, int]:
    frontier = queue.Queue[Point2d]()
    came_from: dict[Point2d, Point2d] = {}
    cost_so_far: dict[Point2d, int] = {}

    frontier.put(start)
    came_from[start] = Point2d(sys.maxsize, sys.maxsize)
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break

        for neighbor in grid.get_neighbors(current):
            if grid.get_symbol(neighbor) == "#":
                continue

            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                frontier.put(neighbor)

    return cost_so_far

def get_cheat_enough_saved_counter(cost_map: dict[Point2d, int], max_distance: int, minimum_saved: int):
    counter = 0

    possible_coordinates: list[tuple[Point2d, int]] = []
    for y in range(-max_distance, max_distance + 1):
        for x in range(-max_distance, max_distance + 1):
            distance = abs(x) + abs(y)
            if distance <= max_distance:
                possible_coordinates.append((Point2d(x, y), distance))

    for point in cost_map.keys():
        point_cost = cost_map[point]
        for coord, distance in possible_coordinates:
            if (path := point + coord) in cost_map:
                if cost_map[path] - point_cost - distance >= minimum_saved:
                    counter += 1

    return counter

def silver_solution(lines: list[str]) -> int:
    grid, start, end = parse_input(lines)
    cost_map = djikstra_search(grid, start, end)
    return get_cheat_enough_saved_counter(cost_map, 2, 100)

def gold_solution(lines: list[str]) -> int:
    grid, start, end = parse_input(lines)
    cost_map = djikstra_search(grid, start, end)
    return get_cheat_enough_saved_counter(cost_map, 20, 100)
