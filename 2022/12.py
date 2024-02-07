import queue
import sys
from typing import Optional
from utils.matrix import Matrix
from utils.point import INVALID_POINT, Point

def parse_input(lines: list[str]) -> tuple[Matrix[int], Point, Point]:
    start, end = INVALID_POINT, INVALID_POINT
    height, width = len(lines), len(lines[0])
    data: list[list[int]] = [[0 for _ in range(width)] for _ in range(height)]
    ordinal_initial_count = ord("a") - 1

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                start = Point(x, y)
                data[y][x] = ord("a") - ordinal_initial_count
            elif char == "E":
                end = Point(x, y)
                data[y][x] = ord("z") - ordinal_initial_count
            else:
                data[y][x] = ord(char) - ordinal_initial_count

    return Matrix[int](data, int), start, end

def djikstra_search(grid: Matrix[int], start: Point, end: Point) -> dict[Point, Point]:
    frontier = queue.Queue[Point]()
    frontier.put(start)
    came_from: dict[Point, Point] = {}
    came_from[start] = INVALID_POINT
    cost_so_far: dict[Point, int] = {}
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break

        for (neighbor, _) in grid.get_neighbors(current):
            if not grid.get_symbol(neighbor) <= grid.get_symbol(current) + 1:
                continue

            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                frontier.put(neighbor)

    return came_from

def reconstruct_shortest_path(came_from: dict[Point, Point], start: Point, end: Point) -> Optional[list[Point]]:
    current = end
    path: list[Point] = []

    if end not in came_from:
        return None

    while current != start:
        if current == INVALID_POINT:
            return None

        path.append(current)
        current = came_from[current]

    return path

def get_shortest_path_length(grid: Matrix[int], start: Point, end: Point) -> Optional[int]:
    came_from = djikstra_search(grid, start, end)
    path = reconstruct_shortest_path(came_from, start, end)
    return len(path) if path is not None else None

def silver_solution(lines: list[str]) -> int:
    grid, start, end = parse_input(lines)
    return get_shortest_path_length(grid, start, end) or -1

def gold_solution(lines: list[str]) -> int:
    grid, _, end = parse_input(lines)
    possible_starts = [point for y, line in enumerate(grid.get_data()) for x, _ in enumerate(line) if (point := Point(x, y)) and grid.get_symbol(point) == 1]

    shortest_path = sys.maxsize
    for start in possible_starts:
        length = get_shortest_path_length(grid, start, end)
        if length is not None and length < shortest_path:
            shortest_path = length

    return shortest_path
