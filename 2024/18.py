# pylint: disable=unused-argument

from collections import deque
import queue
import sys
from utils.matrix import Matrix
from utils.point import INVALID_POINT, Direction, Point

sys.setrecursionlimit(2 ** 30)

def parse_input(lines: list[str]) -> list[Point]:
    points: list[Point] = []
    for line in lines:
        x, y = line.split(",")
        points.append(Point(int(x), int(y)))

    return points

# def get_paths_bfs(grid: Matrix[int], start: Point, end: Point) -> list[list[Point]]:
#     frontier = queue.Queue[tuple[Point, list[Point]]]()
#     frontier.put((start, []))
#     all_paths: list[list[Point]] = []

#     while not frontier.empty():
#         current, path = frontier.get()
#         for neighbor, _ in grid.get_neighbors(current):
#             if grid.get_symbol(current) + 1 == grid.get_symbol(neighbor):
#                 new_path = path + [neighbor]
#                 frontier.put((neighbor, new_path))
#                 if neighbor == end:
#                     all_paths.append(new_path)

#     return all_paths

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

# def get_path_dfs(start: Point, end: Point, walls: set[Point], width: int, height: int, visited: set[Point], path: list[Point]) -> list[Point]:
#     visited.add(start)
#     path.append(start)

#     if start == end:
#         return path

#     for neighbor in start.get_neighbors_2d_in_bounds(width, height):
#         if neighbor not in visited and neighbor not in walls and neighbor.in_bounds_2d(width, height):
#             result = get_path_dfs(neighbor, end, walls, width, height, visited, path)
#             if result:
#                 return result

#     path.pop()
#     return []

def bfs(graph: Matrix[str], node: Point, target: Point):
    visited = {}
    queue = deque[Point]()

    visited[node] = INVALID_POINT
    queue.append(node)
    
    while queue:
        m = queue.popleft() 
        if m == target:
            path = []
            while m != INVALID_POINT:
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


# visited = set() # Set to keep track of visited nodes of graph.

# def dfs(visited, graph, node):  #function for dfs 
#     if node not in visited:
#         print (node)
#         visited.add(node)
#         for neighbour in graph[node]:
#             dfs(visited, graph, neighbour)

def dfs(graph: Matrix[str], start: Point, end: Point, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    # Mark the current node as visited and add it to the path
    visited.add(start)
    path.append(start)

    # If the end node is reached, return the path
    if start == end:
        return path

    # Recur for all the vertices adjacent to this vertex
    for neighbor, _ in graph.get_neighbors(start):
        if graph.get_symbol(neighbor) == "#":
            continue
        if neighbor not in visited:
            result = dfs(graph, neighbor, end, visited, path)
            if result:  # If the end node is found in this path, propagate it upwards
                return result

    # If no path to the end node is found, backtrack
    path.pop()
    return []

# Driver Code
# print("Following is the Depth-First Search")
# dfs(visited, graph, '5')

def silver_solution(lines: list[str]) -> int:
    walls = parse_input(lines)

    # SIZE = 6
    # AMOUNT = 12
    SIZE = 70
    AMOUNT = 1024

    path = get_path_bfs(Point(0, 0), Point(SIZE, SIZE), set(walls[:AMOUNT]), SIZE + 1, SIZE + 1)

    # data = [["." for _ in range(SIZE+1)] for _ in range(SIZE+1)]
    # grid = Matrix[str](data, str)

    # for point in walls[:AMOUNT]:
    #     grid.set_symbol(point, "#")

    # path = bfs(grid, Point(0, 0), Point(SIZE, SIZE))

    # for point in path:
    #     grid.set_symbol(point, "@")

    # grid.print()

    # print(path)

    return len(path) - 1

# def binary_search(arr, x):
#     low = 0
#     high = len(arr) - 1
#     mid = 0
 
#     while low <= high:
 
#         mid = (high + low) // 2
 
#         # If x is greater, ignore left half
#         if arr[mid] < x:
#             low = mid + 1
 
#         # If x is smaller, ignore right half
#         elif arr[mid] > x:
#             high = mid - 1
 
#         # means x is present at mid
#         else:
#             return mid
 
#     # If we reach here, then the element was not present
#     return -1

def gold_solution(lines: list[str]) -> str:
    points = parse_input(lines)


    # RANGE = 6
    RANGE = 70

    start = Point(0, 0)
    end = Point(RANGE, RANGE)

    low = 0
    mid = 0
    high = len(points) - 1

    while low <= high:
        mid = (high + low) // 2

        path = get_path_bfs(start, end, set(points[:mid+1]), RANGE + 1, RANGE + 1)
        # print("mid", low, mid, high, len(path))


        if len(path) > 0:
            low = mid + 1
        elif low == mid:
            break
        else:
            high = mid

        # print("end", low, mid, high)

    # print("FINAL", mid)

    return f"{points[mid].x},{points[mid].y}"

    path: list[Point] = []
    for i in range(len(points)):
        # print(points[:i+1])
        if points[i] not in path and len(path) > 0:
            continue

        # path = get_path_bfs(start, end, set(points[:i+1]), RANGE + 1, RANGE + 1)
        path = get_path_dfs(start, end, set(points[:i+1]), RANGE + 1, RANGE + 1, set(), [])
        # print(i, len(path))
        if len(path) == 0:
            print("AAA", i)
            return str(points[i].x) + "," + str(points[i].y)

    return "A"


    # data = [["." for _ in range(RANGE)] for _ in range(RANGE)]
    # grid = Matrix[str](data, str)
    data = [["." for _ in range(RANGE)] for _ in range(RANGE)]
    grid = Matrix[str](data, str)

    result = ""
    previous_path = []

    for i in range(len(points)):
        grid.set_symbol(points[i], "#")

        if points[i] not in previous_path and len(previous_path) > 0:
            continue

        paths = dfs(grid, Point(0, 0), Point(RANGE - 1, RANGE - 1))


        # if i > 3000:
        #     for point in paths:
        #         grid.set_symbol(point, "@")
        #     grid.print()
        #     print("====")
        #     for point in paths:
        #         grid.set_symbol(point, ".")
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