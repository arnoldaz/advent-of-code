# pylint: disable=unused-argument

import queue
import sys
import uuid
from utils.matrix import Matrix
from utils.point import INVALID_POINT, Direction, Point

sys.setrecursionlimit(2 ** 30)


def parse_input(lines: list[str]) -> tuple[Matrix[str], Point, Point]:
    grid = Matrix[str](lines, str)
    start = grid.find_first_character_instance("S")
    end = grid.find_first_character_instance("E")

    return grid, start, end

class Path:
    id: uuid.UUID
    steps: set[Point]

    current_position: Point
    previous_position: Point
    
    current_direction: Direction
    previous_direction: Direction

    cost: int

    def __init__(self, start_position: Point, start_direction: Direction):
        self.id = uuid.uuid1()
        self.steps = set([start_position])
        self.current_position = start_position
        self.previous_position = Point(-1, -1)
        self.current_direction = start_direction
        self.previous_direction = start_direction
        self.cost = 0

    def __str__(self):
        return f"{{Path: steps={len(self.steps)}, curr_pos={self.current_position}, prev_pos={self.previous_position}}}"

    def __repr__(self):
        return self.__str__()

    def take_step(self, new_position: Point, new_direction: Direction):
        self.steps.add(new_position)
        self.previous_position = self.current_position
        self.current_position = new_position

        self.previous_direction = self.current_direction
        self.current_direction = new_direction

        if self.previous_direction != self.current_direction:
            self.cost += 1000
        
        self.cost += 1

    def get_path_length(self) -> int:
        return len(self.steps)

    def copy(self):
        new_path = Path(self.current_position, self.current_direction)
        new_path.steps = self.steps.copy()
        new_path.previous_position = self.previous_position
        new_path.previous_direction = self.previous_direction

        return new_path

def get_possible_movements(path: Path, matrix: Matrix) -> list[tuple[Point, Direction]]:
    neighbors = matrix.get_neighbors(path.current_position)
    possible_movements: list[tuple[Point, Direction]] = []

    for neighbor in neighbors:
        neighbor_position, neighbor_direction = neighbor
        symbol = matrix.get_symbol(neighbor_position)

        if symbol == "#":
            continue
        if neighbor_position in path.steps:
            continue

        possible_movements.append((neighbor_position, neighbor_direction))

    return possible_movements

def walk_until_intersection(path: Path, matrix: Matrix, start_position: Point, end_position: Point) -> tuple[list[tuple[Point, Direction]], bool]:
    while True:
        possible_movements = get_possible_movements(path, matrix)

        if len(possible_movements) == 1:
            path.take_step(possible_movements[0][0], possible_movements[0][1])

            if path.current_position == end_position or path.current_position == start_position:
                return [], True
        else:
            return possible_movements, False

def get_intersections(grid: Matrix[str], start: Point, end: Point) -> list[Point]:
    intersections: list[Point] = [start]
    for y, line in enumerate(grid.get_data()):
        for x, _ in enumerate(line):
            neighbors = [1 for point, _ in grid.get_neighbors(Point(x, y)) if grid.get_symbol(point) != "#" and grid.get_symbol(Point(x, y)) == "."]
            if len(neighbors) > 2:
                intersections.append(Point(x, y))

    intersections.append(end)

    return intersections


def create_graph(matrix: Matrix, start_position: Point, end_position: Point):
    graph: dict[Point, dict[Direction, tuple[int, Point]]] = {}

    intersections = get_intersections(matrix, start_position, end_position)
    # path: list[Point] = []

    for intersection in intersections:
        graph[intersection] = {}
        current_cost = 0

        neighbors = matrix.get_neighbors(intersection)

        print("===")
        print(intersection)
        print(neighbors)

        for neighbor_position, neighbor_direction in neighbors:
            if matrix.get_symbol(neighbor_position) == "#":
                continue

            print("tesitng neighbor", neighbor_position, neighbor_direction)
            current_cost += 1

            current_neighbor_position, current_neighbor_direction = neighbor_position, neighbor_direction
            path = [intersection]
            while True:
                print("gogogo", current_neighbor_position, current_neighbor_direction, path)
                if current_neighbor_position in intersections or current_neighbor_position in path:
                    break

                path.append(current_neighbor_position)

                for sub_neighbor_position, sub_neighbor_direction in matrix.get_neighbors(current_neighbor_position):
                    print("gogogodeeper", sub_neighbor_position, sub_neighbor_direction, path)
                    if matrix.get_symbol(sub_neighbor_position) == "#":
                        continue
                    if sub_neighbor_position in path:
                        continue

                    current_cost += 1

                    if sub_neighbor_position in intersections:
                        graph[intersection][neighbor_direction] = (current_cost, sub_neighbor_position)
                        current_cost = 0
                        current_neighbor_position, current_neighbor_direction = sub_neighbor_position, sub_neighbor_direction
                        break

                    if sub_neighbor_direction != current_neighbor_direction:
                        current_cost += 1000

                    current_neighbor_position, current_neighbor_direction = sub_neighbor_position, sub_neighbor_direction
                    break

                

        # for walk_path in paths:
        #     _, _ = walk_until_intersection(walk_path, matrix, start_position, end_position)
        #     graph[intersection][walk_path.current_position] = walk_path.get_path_length() - 1

    return graph

# def djikstra_search2(grid: Matrix[str], start: Point):
#     frontier = queue.Queue[tuple[Point, Direction]]()
#     came_from: dict[tuple[Point, Direction], Point] = {}
#     cost_so_far: dict[tuple[Point, Direction], int] = {}

#     frontier.put((start, Direction.RIGHT))
#     came_from[(start, Direction.RIGHT)] = INVALID_POINT
#     cost_so_far[(start, Direction.RIGHT)] = 0

#     while not frontier.empty():
#         current, direction = frontier.get()
#         for (neighbor, new_direction) in grid.get_neighbors(current):
#             if direction != new_direction:
#                 cost = 1000
#             else:
#                 cost = 1

#             new_cost = cost_so_far[(current, direction)] + cost
#             if (neighbor, new_direction) not in cost_so_far or new_cost < cost_so_far[(neighbor, new_direction)]:
#                 cost_so_far[(neighbor, new_direction)] = new_cost
#                 came_from[(neighbor, new_direction)] = current
#                 frontier.put((neighbor, new_direction))

#     return cost_so_far


# def djikstra_search3(grid: Matrix[str], start: Point, end: Point):
#     pass

def find_all_paths(graph: dict[Point, dict[Direction, tuple[int, Point]]], start: Point, end: Point, path: list[tuple[Point, int]], visited: list[Point], current_direciton: Direction, current_cost: int) -> list[list[tuple[Point, int]]]:
    print("PATH", path, current_direciton, current_cost)
    path = path + [(start, current_cost)]
    if start == end:
        return [path]

    if start not in graph or start in visited:
        return []

    visited.append(start)

    paths: list[list[tuple[Point, int]]] = []
    ongoing_cost = current_cost
    for direction, (cost, point) in graph[start].items():
        if point not in [point for point, cost in path]:
            if current_direciton != direction:
                ongoing_cost += 1000
            ongoing_cost += cost
            new_paths = find_all_paths(graph, point, end, path, visited.copy(), direction, ongoing_cost)

            for new_path in new_paths:
                paths.append(new_path)

    visited.remove(start)

    print("asdasdsad", paths, ongoing_cost)
    return paths

# def get_paths_bfs(graph: dict[Point, dict[Point, int]], start: Point, end: Point):
#     frontier = queue.Queue[tuple[Point, list[Point]]]()
#     frontier.put((start, []))
#     visited = set([start])
#     all_paths: list[list[Point]] = []

#     while not frontier.empty():
#         current, path = frontier.get()
#         if current not in graph:
#             continue
#         for neighbor in graph[current]:
#             if neighbor not in visited:
#                 visited.add(neighbor)
#                 new_path = path + [neighbor]
#                 frontier.put((neighbor, new_path))
#                 if neighbor == end:
#                     all_paths.append(new_path)

#     return all_paths


def silver_solution(lines: list[str]) -> int:
    grid, start, end = parse_input(lines)

    graph_dict = create_graph(grid, start, end)

    print(len(graph_dict))
    for x in graph_dict.keys():
        print(x, graph_dict[x])

    all_paths = find_all_paths(graph_dict, start, end, [], [], Direction.RIGHT, 0)
    # a = get_paths_bfs(graph_dict, start, end)

    print("PATHS:")
    for path in all_paths:
        print(path)



    # grid.print()

    intersections = get_intersections(grid, start, end)
    height, width = grid.height(), grid.width()

    for y in range(height):
        for x in range(width):
            symbol = grid.get_symbol(Point(x, y))
            if Point(x, y) in intersections:
                print("@", end="")
            else:
                print(symbol, end="")

        print()


    # all_paths = find_all_paths(grid, start, end, [], [])
    
    # print(all_paths)

    # height, width = grid.height(), grid.width()
    # for path in all_paths:
    #     for y in range(height):
    #         for x in range(width):
    #             symbol = grid.get_symbol(Point(x, y))
    #             if Point(x, y) in path:
    #                 print("@", end="")
    #             else:
    #                 print(symbol, end="")

    #         print()
    #     print("=================")


        # print(len(all_paths))

    return -123

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321



# [({x=1, y=13}, 0), ({x=1, y=11}, 1002), ({x=3, y=9}, 2006), ({x=3, y=7}, 2008), ({x=5, y=7}, 3012), ({x=9, y=7}, 3016), ({x=13, y=1}, 7040)]

###############
#..@....#....@#
#.#.###.#.###.#
#@.@..#.#...#.#
#.###.#####.#.#
#.#.#....@..#.#
#.#.#####.###.#
#..@.@...@..#.#
###.#.#####.#.#
#..@#@....#.#.#
#.#.#.###.#.#.#
#@.@.@#..@#.#.#
#.###.#.#.#.#.#
#@..#..@..#...#
###############