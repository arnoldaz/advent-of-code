import queue
from utils.matrix import Matrix
from utils.point import INVALID_POINT, Point

# TODO refactor to new grid and point2d

def parse_input(lines: list[str]) -> tuple[Matrix[str], Point, Point]:
    grid = Matrix[str](lines, str)
    start = grid.find_first_character_instance("S")
    end = grid.find_first_character_instance("E")

    return grid, start, end

def djikstra_search(grid: Matrix[str], start: Point, end: Point) -> dict[Point, int]:
    frontier = queue.Queue[Point]()
    came_from: dict[Point, Point] = {}
    cost_so_far: dict[Point, int] = {}

    frontier.put(start)
    came_from[start] = INVALID_POINT
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break

        for (neighbor, _) in grid.get_neighbors(current):
            if grid.get_symbol(neighbor) == "#":
                continue

            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                frontier.put(neighbor)

    return cost_so_far

def grid_distance(point1: Point, point2: Point):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def get_cheat_enough_saved_counter(cost_map: dict[Point, int], max_distance: int, minimum_saved: int):
    path = cost_map.keys()
    counter = 0

    for point in path:
        for y in range(-max_distance, max_distance + 1):
            for x in range(-max_distance, max_distance + 1):
                possible_path = point + Point(x, y)
                if possible_path not in cost_map or point == possible_path:
                    continue

                distance = grid_distance(point, possible_path)
                if distance <= max_distance:
                    saved_amount = cost_map[possible_path] - cost_map[point] - distance
                    if saved_amount >= minimum_saved:
                        counter += 1

        # for other_point in path:
        #     distance = grid_distance(point, other_point)
        #     if distance <= max_distance:
        #         saved_amount = cost_map[other_point] - cost_map[point] - distance
        #         if saved_amount >= minimum_saved:
        #             counter += 1

    return counter

def silver_solution(lines: list[str]) -> int:
    grid, start, end = parse_input(lines)
    cost_map = djikstra_search(grid, start, end)
    return get_cheat_enough_saved_counter(cost_map, 2, 100)

def gold_solution(lines: list[str]) -> int:
    grid, start, end = parse_input(lines)
    cost_map = djikstra_search(grid, start, end)
    return get_cheat_enough_saved_counter(cost_map, 20, 100)
