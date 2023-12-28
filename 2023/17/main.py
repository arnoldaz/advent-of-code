from enum import Enum
import sys

file_name = "input-test.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

class Direction(Enum):
    No = 0
    Up = 1
    Right = 2
    Down = 3
    Left = 4

def heuristic(node: tuple[int, int], goal: tuple[int, int]) -> float:
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5

def get_node_neighbors(node: tuple[int, int], direction: Direction, same_direction_count: int) -> list[tuple[tuple[int, int], Direction]]:
    current_x = node[0]
    current_y = node[1]

    neighbors: list[tuple[tuple[int, int], Direction]] = []

    if current_x > 0 and (not direction == Direction.Left or not same_direction_count > 3):
        neighbors.append(((current_x - 1, current_y), Direction.Left))
    
    if current_x < len(lines[0]) - 1 and (not direction == Direction.Right or not same_direction_count > 3):
        neighbors.append(((current_x + 1, current_y), Direction.Right))
    
    if current_y > 0 and (not direction == Direction.Up or not same_direction_count > 3):
        neighbors.append(((current_x, current_y - 1), Direction.Up))
    
    if current_y < len(lines) - 1 and (not direction == Direction.Down or not same_direction_count > 3):
        neighbors.append(((current_x, current_y + 1), Direction.Down))
    
    return neighbors

def find_least_loss_path(lines: list[str]):
    start: tuple[int, int] = (0, 0)
    end: tuple[int, int] = (len(lines[0]) - 1, len(lines) - 1)

    open_set: set[tuple[int, int]] = set([start])
    closed_set: set[tuple[int, int]] = set()

    g_values: dict[tuple[int, int], int] = {}
    g_values[start] = 0

    parents: dict[tuple[int, int], list[tuple[tuple[int, int], tuple[Direction, int]]]] = {}
    parents[start] = [(start, (Direction.No, 0))]

    test_matrix = [[0 for _ in range(len(lines[0]))] for _ in range(len(lines))]

    # previous_direction: Direction = Direction.No
    # same_direction_count = 0

    while len(open_set) > 0:
        for key in g_values:
            test_matrix[key[1]][key[0]] = g_values[key]

        # print(f"{open_set=} {closed_set=}")
        # print(f"{g_values=}")
        # for parent in parents:
        #     print(f"key {parent}, value = {parents[parent]}")
        # print(f"{previous_direction=}")
        # print(f"{same_direction_count=}")
        # print("=================")
        # print("\n".join(["".join(["{:4}".format(item) for item in row]) for row in lines]))
        # print("--------------------")
        # print("\n".join(["".join(["{:4}".format(item) for item in row]) for row in test_matrix]))
        # print("=================")

        n = None

        for v in open_set:
            if n == None or g_values[v] + heuristic(v, end) < g_values[n] + heuristic(n, end):
                n = v

        if n == None:
            return None

        if n == end:
            reconst_path = []

            while parents[n][0][0] != n:
                reconst_path.append(n)
                n = parents[n][0][0]

            reconst_path.append(start)
            reconst_path.reverse()

            print(f"Path found: {reconst_path}")
            return reconst_path

        neighbors: list[tuple[tuple[int, int], Direction]] = []
        for parent in parents[n]:
            neighbors += get_node_neighbors(n, parent[1][0], parent[1][1])

        print(f"{neighbors=}")

        for m_wrap in neighbors:
            m = m_wrap[0]
            direction = m_wrap[1]

            weight = int(lines[m[1]][m[0]])
            if m not in open_set and m not in closed_set:
                open_set.add(m)

                min_value = sys.maxsize
                min_value_index = -1
                for i, parent in enumerate(parents[n]):
                    value = parent[1][1] + 1 if parent[1][0] == direction else parent[1][1]
                    if value < min_value:
                        min_value = value
                        min_value_index = i

                parents[m] = [(n, (direction, parents[n][min_value_index][1][1] + 1 if parents[n][min_value_index][1][0] == direction else parents[n][min_value_index][1][1]))]
                g_values[m] = g_values[n] + weight

            else:
                if g_values[m] > g_values[n] + weight:
                    g_values[m] = g_values[n] + weight

                    min_value = sys.maxsize
                    min_value_index = -1
                    for i, parent in enumerate(parents[n]):
                        value = parent[1][1] + 1 if parent[1][0] == direction else parent[1][1]
                        if value < min_value:
                            min_value = value
                            min_value_index = i

                    parents[m] = [(n, (direction, parents[n][min_value_index][1][1] + 1 if parents[n][min_value_index][1][0] == direction else parents[n][min_value_index][1][1]))]

                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)
                elif g_values[m] == g_values[n] + weight and not any(x == n for x in parents[m][0]):

                    min_value = sys.maxsize
                    min_value_index = -1
                    for i, parent in enumerate(parents[n]):
                        value = parent[1][1] + 1 if parent[1][0] == direction else parent[1][1]
                        if value < min_value:
                            min_value = value
                            min_value_index = i

                    parents[m].append((n, (direction, parents[n][min_value_index][1][1] + 1 if parents[n][min_value_index][1][0] == direction else parents[n][min_value_index][1][1])))

                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)

        open_set.remove(n)
        closed_set.add(n)

    pass

weight_sum = 0
path = find_least_loss_path(lines)
if path == None:
    exit(0)

for step in path[1:]:
    weight = int(lines[step[1]][step[0]])
    weight_sum += weight

    lines[step[1]] = lines[step[1]][:step[0]] + "@" + lines[step[1]][step[0]+1:]

for line in lines:
    print(line)

print(f"{weight_sum=}")

