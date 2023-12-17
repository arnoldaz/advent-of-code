from typing import NamedTuple
from math import lcm

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

class Node(NamedTuple):
    start: str
    left: str
    right: str

path = lines[0]
nodes: list[Node] = []
for line in lines[2:]:
    start_string, node_string = line.split("=")
    left, right = node_string.replace("(", "").replace(")", "").split(",")
    nodes.append(Node(start_string.strip(), left.strip(), right.strip()))

def count_steps_simple(path: str, nodes: list[Node]) -> int:
    steps = 0

    current_node = "AAA"
    current_path_index = 0
    while True:
        symbol = path[current_path_index]
        possible_paths = next(node for node in nodes if node.start == current_node)
        if symbol == "L":
            current_node = possible_paths.left
        elif symbol == "R":
            current_node = possible_paths.right
        steps += 1
        current_path_index += 1

        if current_path_index == len(path):
            current_path_index = 0

        if current_node == "ZZZ":
            break

    return steps

def count_steps_ghost(path: str, nodes: list[Node]) -> int:
    current_nodes = [x.start for x in nodes if x.start.endswith("A")]
    step_results = []

    for current_node in current_nodes:
        steps = 0
        current_path_index = 0
        while True:
            symbol = path[current_path_index]
            possible_paths = next(node for node in nodes if node.start == current_node)
            if symbol == "L":
                current_node = possible_paths.left
            elif symbol == "R":
                current_node = possible_paths.right
            steps += 1
            current_path_index += 1

            if current_path_index == len(path):
                current_path_index = 0

            if current_node.endswith("Z"):
                step_results.append(steps)
                break

    return lcm(*step_results)

print(f"{count_steps_simple(path, nodes)=}")
print(f"{count_steps_ghost(path, nodes)=}")
