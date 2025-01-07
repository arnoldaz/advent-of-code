import sys
from collections import deque

from utils.point2d import Point2d

def parse_input(lines: list[str]) -> list[Point2d]:
    return [Point2d(int(x), int(y)) for line in lines for x, y in [line.split(",")]]

def get_path_bfs(start: Point2d, end: Point2d, walls: set[Point2d], width: int, height: int):
    visited: dict[Point2d, Point2d] = {}
    queue = deque[Point2d]()
    path: list[Point2d] = []
    invalid_point = Point2d(sys.maxsize, sys.maxsize)

    visited[start] = invalid_point
    queue.append(start)

    while queue:
        current = queue.popleft()
        if current == end:
            while current != invalid_point:
                path.append(current)
                current = visited[current]
            return path[::-1]
        for neighbor in current.get_neighbors(width, height):
            if neighbor not in visited and neighbor not in walls:
                visited[neighbor] = current
                queue.append(neighbor)

    return path

def silver_solution(lines: list[str]) -> int:
    walls = parse_input(lines)
    grid_size = 70
    fallen_walls = 1024

    path = get_path_bfs(
        Point2d(0, 0),
        Point2d(grid_size, grid_size),
        set(walls[:fallen_walls]),
        grid_size + 1,
        grid_size + 1,
    )

    return len(path) - 1

def gold_solution(lines: list[str]) -> str:
    points = parse_input(lines)
    grid_size = 70

    start = Point2d(0, 0)
    end = Point2d(grid_size, grid_size)

    low = 0
    mid = 0
    high = len(points) - 1

    while low <= high:
        mid = (high + low) // 2
        path = get_path_bfs(start, end, set(points[:mid+1]), grid_size + 1, grid_size + 1)

        if len(path) > 0:
            low = mid + 1
        elif low == mid:
            break
        else:
            high = mid

    return f"{points[mid].x},{points[mid].y}"
