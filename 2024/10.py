# pylint: disable=unused-argument

import queue
from typing import Optional
from utils.matrix import Matrix
from utils.point import INVALID_POINT, Point


def get_paths_bfs(grid: Matrix[int], start: Point, ends: list[Point]) -> list[list[Point]]:
    frontier = queue.Queue[tuple[Point, list[Point]]]()
    frontier.put((start, []))
    visited = set([start])
    all_paths: list[list[Point]] = []

    while not frontier.empty():
        current, path = frontier.get()
        for neighbor, _ in grid.get_neighbors(current):
            if neighbor not in visited and grid.get_symbol(current) + 1 == grid.get_symbol(neighbor):
                visited.add(neighbor)
                new_path = path + [neighbor]
                frontier.put((neighbor, new_path))
                if neighbor in ends:
                    all_paths.append(new_path)

    return all_paths

def djikstra_search(grid: Matrix[int], start: Point, end: Point) -> dict[Point, Point]:
    frontier = queue.Queue[Point]()
    came_from: dict[Point, Point] = {}
    cost_so_far: dict[Point, int] = {}

    # for start in starts:
    #     frontier.put(start)
    #     came_from[start] = INVALID_POINT
    #     cost_so_far[start] = 0

    frontier.put(start)
    came_from[start] = INVALID_POINT
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break

        for (neighbor, _) in grid.get_neighbors(current):
            if not grid.get_symbol(neighbor) == grid.get_symbol(current) + 1:
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

def silver_solution(lines: list[str]) -> int:
    return 0

    grid = Matrix[int](lines, int)
    starts = grid.find_all_character_instances(0)
    ends = grid.find_all_character_instances(9)

    # print(starts)
    # print(ends)

    final_result = 0

    for start in starts:
        result = 0
        for end in ends:
            # print("AAA", start, end)
            came_from = djikstra_search(grid, start, end)
            for x in came_from.keys():
                print(x, came_from[x])
            print("+===========")
            path = reconstruct_shortest_path(came_from, start, end)
            # print(path)
            if path is not None:
                result += 1
            # test_matrix = Matrix[int](lines, int)
            # if path is not None:
            #     for a in path:
            #         test_matrix.set_symbol(a, -1)
            #     test_matrix.print(2)

        # print(result)
        final_result += result

    return final_result

def gold_solution(lines: list[str]) -> int:
    grid = Matrix[int](lines, int)
    starts = grid.find_all_character_instances(0)
    ends = grid.find_all_character_instances(9)

    # for start in starts:
    paths = get_paths_bfs(grid, starts[0], ends)
    for x in paths:
        print(x)

    return -321
