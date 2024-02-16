import uuid
import sys
from utils.matrix import Matrix
from utils.point import Direction, Point

sys.setrecursionlimit(2 ** 30)

class Path:
    id: uuid.UUID
    steps: set[Point]
    current_position: Point
    previous_position: Point

    def __init__(self, start_position: Point):
        self.id = uuid.uuid1()
        self.steps = set([start_position])
        self.current_position = start_position
        self.previous_position = Point(-1, -1)

    def __str__(self):
        return f"{{Path: steps={len(self.steps)}, curr_pos={self.current_position}, prev_pos={self.previous_position}}}"

    def __repr__(self):
        return self.__str__()

    def take_step(self, new_position: Point):
        self.steps.add(new_position)
        self.previous_position = self.current_position
        self.current_position = new_position

    def get_path_length(self) -> int:
        return len(self.steps)

    def copy(self):
        new_path = Path(self.current_position)
        new_path.steps = self.steps.copy()
        new_path.previous_position = self.previous_position

        return new_path

def get_initial_data(lines: list[str]) -> tuple[Matrix, Point, Point]:
    matrix = Matrix[str](lines, str)
    matrix_data = matrix.get_data()

    first_line = matrix_data[0]
    last_line = matrix_data[-1]

    start_position = Point()
    end_position = Point()

    for x, char in enumerate(first_line):
        if char == ".":
            start_position = Point(x, 0)
            break

    for x, char in enumerate(last_line):
        if char == ".":
            end_position = Point(x, matrix.height() - 1)
            break

    return (matrix, start_position, end_position)

def get_possible_movements(path: Path, matrix: Matrix, ignore_directions: bool) -> list[Point]:
    neighbors = matrix.get_neighbors(path.current_position)
    possible_movements: list[Point] = []

    for neighbor in neighbors:
        neighbor_position, neighbor_direction = neighbor
        symbol = matrix.get_symbol(neighbor_position)

        if symbol == "#":
            continue
        if not ignore_directions:
            if symbol == "<" and neighbor_direction != Direction.LEFT:
                continue
            if symbol == ">" and neighbor_direction != Direction.RIGHT:
                continue
            if symbol == "v" and neighbor_direction != Direction.DOWN:
                continue
            if symbol == "^" and neighbor_direction != Direction.UP:
                continue
        if neighbor_position in path.steps:
            continue

        possible_movements.append(neighbor_position)

    return possible_movements

def walk_until_intersection(path: Path, matrix: Matrix, start_position: Point, end_position: Point, ignore_directions: bool) -> tuple[list[Point], bool]:
    while True:
        possible_movements = get_possible_movements(path, matrix, ignore_directions)

        if len(possible_movements) == 1:
            path.take_step(possible_movements[0])

            if path.current_position == end_position or path.current_position == start_position:
                return [], True
        else:
            return possible_movements, False

def create_graph(matrix: Matrix, start_position: Point, end_position: Point, ignore_directions: bool) -> dict[Point, dict[Point, int]]:
    graph: dict[Point, dict[Point, int]] = {}

    intersections: list[Point] = [start_position]
    for y, line in enumerate(matrix.get_data()):
        for x, _ in enumerate(line):
            neighbors = [1 for point, _ in matrix.get_neighbors(Point(x, y)) if matrix.get_symbol(point) != "#" and matrix.get_symbol(Point(x, y)) == "."]
            if len(neighbors) > 2:
                intersections.append(Point(x, y))

    intersections.append(end_position)

    for intersection in intersections:
        graph[intersection] = {}
        path = Path(intersection)
        neighbors = get_possible_movements(path, matrix, ignore_directions)

        paths: list[Path] = []
        for neighbor_position in neighbors:
            copy_path = path.copy()
            copy_path.take_step(neighbor_position)
            paths.append(copy_path)

        for walk_path in paths:
            _, _ = walk_until_intersection(walk_path, matrix, start_position, end_position, ignore_directions)
            graph[intersection][walk_path.current_position] = walk_path.get_path_length() - 1

    # 2d matrix graph
    # simple_graph_matrix = [[0 for _ in range(len(graph))] for _ in range(len(graph))]

    # keys = list(graph.keys())
    # for y, key in enumerate(keys):
    #     edges = graph[key]
    #     edge_keys = list(edges.keys())
    #     for edge_key in edge_keys:
    #         x = keys.index(edge_key)
    #         simple_graph_matrix[y][x] = edges[edge_key]

    return graph

def find_all_paths(graph: dict[Point, dict[Point, int]], start: Point, end: Point, path: list[Point], visited: list[Point]) -> list[list[Point]]:
    path = path + [start]
    if start == end:
        return [path]

    if start not in graph or start in visited:
        return []

    visited.append(start)

    paths: list[list[Point]] = []
    for node in graph[start]:
        if node not in path:
            new_paths = find_all_paths(graph, node, end, path, visited.copy())
            for new_path in new_paths:
                paths.append(new_path)

    visited.remove(start)

    return paths

def get_max_path_weight(graph: dict[Point, dict[Point, int]], start: Point, end: Point) -> int:
    max_path_sum = 0
    all_paths = find_all_paths(graph, start, end, [], [])

    for path in all_paths:
        path_sum = sum([graph[point1][point2] for point1, point2 in zip(path, path[1:])])
        if path_sum > max_path_sum:
            max_path_sum = path_sum

    return max_path_sum

def silver_solution(lines: list[str]) -> int:
    matrix, start_position, end_position = get_initial_data(lines)
    graph_dict = create_graph(matrix, start_position, end_position, False)
    return get_max_path_weight(graph_dict, start_position, end_position)

def gold_solution(lines: list[str]) -> int: # runs for ~345s
    matrix, start_position, end_position = get_initial_data(lines)
    graph_dict = create_graph(matrix, start_position, end_position, True)
    return get_max_path_weight(graph_dict, start_position, end_position)
