import queue

from utils.grid import Grid
from utils.point2d import Direction2d, Point2d

def parse_input(lines: list[str]) -> tuple[Grid[str], Point2d, Point2d]:
    grid = Grid[str](lines)
    start = grid.find_first_character_instance("S")
    end = grid.find_first_character_instance("E")

    return grid, start, end

def get_weights_djikstra(grid: Grid[str], start: Point2d):
    weight_grid: Grid[int] = Grid.create_empty(-1, grid.width(), grid.height())
    weight_grid.set_symbol(start, 0)

    frontier = queue.Queue[tuple[Point2d, Direction2d, int]]()
    frontier.put((start, Direction2d.RIGHT, 0))

    while not frontier.empty():
        current_point, current_direction, cost = frontier.get()

        for neighbor, new_direction in grid.get_neighbors_with_directions(current_point):
            if grid.get_symbol(neighbor) == "#":
                continue

            new_cost = cost + 1
            if current_direction != new_direction:
                new_cost += 1000

            weight = weight_grid.get_symbol(neighbor)
            if weight == -1 or new_cost <= weight:
                weight_grid.set_symbol(neighbor, new_cost)
                frontier.put((neighbor, new_direction, new_cost))

    return weight_grid

def get_points_in_min_paths(weight_grid: Grid[int], start: Point2d, end: Point2d, max_cost: int):
    path_points = set[Point2d]([end])

    frontier = queue.Queue[Point2d]()
    frontier.put(end)

    while not frontier.empty():
        current_point = frontier.get()
        if current_point == start:
            continue

        for neighbor in weight_grid.get_neighbors(current_point):
            neighbor_cost = weight_grid.get_symbol(neighbor)
            if neighbor not in path_points and 0 < neighbor_cost <= max_cost:
                frontier.put(neighbor)
                path_points.add(neighbor)

    return path_points

def silver_solution(lines: list[str]) -> int:
    grid, start, end = parse_input(lines)
    weight_grid = get_weights_djikstra(grid, start)
    return weight_grid.get_symbol(end)

def gold_solution(lines: list[str]) -> int:
    grid, start, end = parse_input(lines)
    weight_grid_from_start = get_weights_djikstra(grid, start)
    weight_grid_from_end = get_weights_djikstra(grid, end)

    # Calculating the paths based on single direction weight grid breaks due to intersections where the valid paths split,
    # since they have a lower than expected value for one of the paths because the other path comes into the intersection with lower value without having turned yet.
    # e.g. 4009 3010 4011
    #      #### 3009 ####
    # Combining the paths from both sides fixes this issue by making all path points having the value of min cost + 1000 and these problematic corners having exactly min cost.
    # e.g. 8036 7036 8036
    #      #### 8036 ####
    weight_grid_combined = Grid.create_empty(0, grid.width(), grid.height())
    for point, _ in weight_grid_combined.iterate():
        weight_grid_combined.set_symbol(point, weight_grid_from_start.get_symbol(point) + weight_grid_from_end.get_symbol(point))

    min_path_cost = weight_grid_from_start.get_symbol(end)

    return len(get_points_in_min_paths(weight_grid_combined, start, end, min_path_cost + 1000))
