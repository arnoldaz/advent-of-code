from collections import deque
from utils.point import INVALID_POINT, Direction, Point

GRID_SIZE = 70

def parse_input(lines: list[str]) -> list[Point]:
    points: list[Point] = []
    for line in lines:
        x, y = line.split(",")
        points.append(Point(int(x), int(y)))

    return points

def get_path_bfs(start: Point, end: Point, walls: set[Point], width: int, height: int):
    visited: dict[Point, Point] = {}
    queue = deque[Point]()
    path: list[Point] = []

    visited[start] = INVALID_POINT
    queue.append(start)

    while queue:
        current = queue.popleft() 
        if current == end:
            while current != INVALID_POINT:
                path.append(current)
                current = visited[current]
            return path[::-1]
        for neighbor in [current + direction for direction in Direction.valid_directions()]:
            if neighbor not in visited and neighbor not in walls and neighbor.in_bounds_2d(width, height):
                visited[neighbor] = current
                queue.append(neighbor)

    return path

def silver_solution(lines: list[str]) -> int:
    walls = parse_input(lines)
    WALL_AMOUNT = 1024

    path = get_path_bfs(Point(0, 0), Point(GRID_SIZE, GRID_SIZE), set(walls[:WALL_AMOUNT]), GRID_SIZE + 1, GRID_SIZE + 1)

    return len(path) - 1

def gold_solution(lines: list[str]) -> str:
    points = parse_input(lines)

    start = Point(0, 0)
    end = Point(GRID_SIZE, GRID_SIZE)

    low = 0
    mid = 0
    high = len(points) - 1

    while low <= high:
        mid = (high + low) // 2
        path = get_path_bfs(start, end, set(points[:mid+1]), GRID_SIZE + 1, GRID_SIZE + 1)

        if len(path) > 0:
            low = mid + 1
        elif low == mid:
            break
        else:
            high = mid

    return f"{points[mid].x},{points[mid].y}"
