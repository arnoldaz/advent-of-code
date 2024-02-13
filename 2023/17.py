import queue
from utils.matrix import Matrix
from utils.point import INVALID_POINT, Direction, Point, reverse_direction

def get_valid_neighbors(current: Point, previous_direction: Direction, grid: Matrix[int], possible_movements: list[tuple[Point, Direction]]) -> list[tuple[Point, Direction, int]]:
    valid_destinations = [(point + current, dir) for point, dir in possible_movements if dir != previous_direction and dir != reverse_direction(previous_direction) and grid.in_bounds(point + current)]

    valid_neighbors: list[tuple[Point, Direction, int]] = []
    for destination, direction in valid_destinations:
        match direction:
            case Direction.UP:
                column = grid.get_column(current.x)
                cost = sum(column[destination.y:current.y])
            case Direction.DOWN:
                column = grid.get_column(current.x)
                cost = sum(column[current.y+1:destination.y+1])
            case Direction.LEFT:
                row = grid.get_row(current.y)
                cost = sum(row[destination.x:current.x])
            case Direction.RIGHT:
                row = grid.get_row(current.y)
                cost = sum(row[current.x+1:destination.x+1])
            case Direction.NONE:
                cost = 0

        valid_neighbors.append((destination, direction, cost))

    return valid_neighbors

PointFrom = tuple[Point, Direction]

def djikstra_search(grid: Matrix[int], start: Point, possible_movements: list[tuple[Point, Direction]]):
    frontier = queue.Queue[PointFrom]()
    came_from: dict[PointFrom, Point] = {}
    cost_so_far: dict[PointFrom, int] = {}

    frontier.put((start, Direction.NONE))
    came_from[(start, Direction.NONE)] = INVALID_POINT
    cost_so_far[(start, Direction.NONE)] = 0

    while not frontier.empty():
        current, direction = frontier.get()
        for (neighbor, new_direction, cost) in get_valid_neighbors(current, direction, grid, possible_movements):
            new_cost = cost_so_far[(current, direction)] + cost
            if (neighbor, new_direction) not in cost_so_far or new_cost < cost_so_far[(neighbor, new_direction)]:
                cost_so_far[(neighbor, new_direction)] = new_cost
                came_from[(neighbor, new_direction)] = current
                frontier.put((neighbor, new_direction))

    return cost_so_far

def calculate_min_cost(grid: Matrix[int], min_step_count: int, max_step_count: int):
    start, end = Point(0, 0), Point(grid.width() - 1, grid.height() - 1)
    possible_movements = [(direction * amount, direction) for direction in Direction.valid_directions() for amount in range(min_step_count, max_step_count + 1)]
    costs = djikstra_search(grid, start, possible_movements)
    return min(costs[(end, Direction.DOWN)], costs[(end, Direction.RIGHT)])

def silver_solution(lines: list[str]) -> int:
    grid = Matrix[int](lines, int)
    return calculate_min_cost(grid, 1, 3)

def gold_solution(lines: list[str]) -> int:
    grid = Matrix[int](lines, int)
    return calculate_min_cost(grid, 4, 10)
