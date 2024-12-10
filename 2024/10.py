import queue
from utils.matrix import Matrix
from utils.point import Point

def get_paths_bfs(grid: Matrix[int], start: Point, ends: list[Point]) -> list[list[Point]]:
    frontier = queue.Queue[tuple[Point, list[Point]]]()
    frontier.put((start, []))
    all_paths: list[list[Point]] = []

    while not frontier.empty():
        current, path = frontier.get()
        for neighbor, _ in grid.get_neighbors(current):
            if grid.get_symbol(current) + 1 == grid.get_symbol(neighbor):
                new_path = path + [neighbor]
                frontier.put((neighbor, new_path))
                if neighbor in ends:
                    all_paths.append(new_path)

    return all_paths

def silver_solution(lines: list[str]) -> int:
    grid = Matrix[int](lines, int)
    starts = grid.find_all_character_instances(0)
    ends = grid.find_all_character_instances(9)

    return sum(len(set(path[-1] for path in get_paths_bfs(grid, start, ends))) for start in starts)

def gold_solution(lines: list[str]) -> int:
    grid = Matrix[int](lines, int)
    starts = grid.find_all_character_instances(0)
    ends = grid.find_all_character_instances(9)

    return sum(len(get_paths_bfs(grid, start, ends)) for start in starts)
