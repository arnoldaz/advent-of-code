# pylint: disable=unused-argument

from collections import deque
import queue
from utils.matrix import Matrix
from utils.point import Point

def parse_input(lines: list[str]) -> list[Point]:
    points: list[Point] = []
    for line in lines:
        x, y = line.split(",")
        points.append(Point(int(x), int(y)))

    return points

def get_paths_bfs(grid: Matrix[int], start: Point, end: Point) -> list[list[Point]]:
    frontier = queue.Queue[tuple[Point, list[Point]]]()
    frontier.put((start, []))
    all_paths: list[list[Point]] = []

    while not frontier.empty():
        current, path = frontier.get()
        for neighbor, _ in grid.get_neighbors(current):
            if grid.get_symbol(current) + 1 == grid.get_symbol(neighbor):
                new_path = path + [neighbor]
                frontier.put((neighbor, new_path))
                if neighbor == end:
                    all_paths.append(new_path)

    return all_paths

def bfs(graph: Matrix[str], node: Point, target: Point):
    visited = {}
    queue = deque[Point]()

    visited[node] = None
    queue.append(node)
    
    while queue:
        m = queue.popleft() 
        if m == target:
            path = []
            while m:
                path.append(m)
                m = visited[m]
            return path[::-1]
        for neighbour, _ in graph.get_neighbors(m):
            if graph.get_symbol(neighbour) == "#":
                continue
            if neighbour not in visited:
                visited[neighbour] = m
                queue.append(neighbour)

    return []

def silver_solution(lines: list[str]) -> int:
    points = parse_input(lines)

    # RANGE = 7
    # AMOUNT = 12
    RANGE = 71
    AMOUNT = 1024

    data = [["." for _ in range(RANGE)] for _ in range(RANGE)]
    grid = Matrix[str](data, str)

    for point in points[:AMOUNT]:
        grid.set_symbol(point, "#")

    paths = bfs(grid, Point(0, 0), Point(RANGE - 1, RANGE - 1))

    for point in paths:
        grid.set_symbol(point, "@")

    # grid.print()

    # print(paths)

    return len(paths) - 1

def gold_solution(lines: list[str]) -> str:
    points = parse_input(lines)

    # RANGE = 7
    # AMOUNT = 12
    RANGE = 71
    # AMOUNT = 1024

    # data = [["." for _ in range(RANGE)] for _ in range(RANGE)]
    # grid = Matrix[str](data, str)
    data = [["." for _ in range(RANGE)] for _ in range(RANGE)]
    grid = Matrix[str](data, str)

    result = ""
    previous_path = []

    for i in range(len(points)):
        grid.set_symbol(points[i], "#")

        # if points[i] not in previous_path and len(previous_path) > 0:
        #     continue

        paths = bfs(grid, Point(0, 0), Point(RANGE - 1, RANGE - 1))


        if i > 3000:
            for point in paths:
                grid.set_symbol(point, "@")
            grid.print()
            print("====")
            for point in paths:
                grid.set_symbol(point, ".")
        # for point in paths:
        #     grid.set_symbol(point, "@")
        # grid.print()
        # print("====")
        if len(paths) > 0:
            continue
        else:
            result = str(points[i].x) + "," + str(points[i].y)

            break

    # grid.print()

    # print(paths)

    return result