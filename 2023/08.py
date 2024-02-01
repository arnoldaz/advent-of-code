from typing import NamedTuple
from math import lcm

class NodePath(NamedTuple):
    left: str
    right: str

def parse_input(lines: list[str]) -> tuple[str, dict[str, NodePath]]:
    path = lines[0]
    node_paths: dict[str, NodePath] = {}
    for line in lines[2:]:
        start_node, node_paths_string = line.split(" = ")
        left_path, right_path = node_paths_string[1:-1].split(", ")
        node_paths[start_node] = NodePath(left_path, right_path)

    return path, node_paths

def silver_solution(lines: list[str]) -> int:
    path, node_paths = parse_input(lines)
    path_length = len(path)

    current_node = "AAA"
    current_path_index = 0
    while True:
        direction = path[current_path_index % path_length]
        possible_paths = node_paths[current_node]
        current_node = possible_paths.left if direction == "L" else possible_paths.right
        current_path_index += 1

        if current_node == "ZZZ":
            break

    return current_path_index

def gold_solution(lines: list[str]) -> int:
    path, node_paths = parse_input(lines)
    path_length = len(path)

    current_nodes = [key for key in node_paths if key.endswith("A")]
    step_counters = []

    for current_node in current_nodes:
        current_path_index = 0
        while True:
            direction = path[current_path_index % path_length]
            possible_paths = node_paths[current_node]
            current_node = possible_paths.left if direction == "L" else possible_paths.right
            current_path_index += 1

            if current_node.endswith("Z"):
                step_counters.append(current_path_index)
                break

    return lcm(*step_counters)
