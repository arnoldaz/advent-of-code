
file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

def get_initial_data(lines: list[str]) -> dict[str, list[str]]:
    connections: dict[str, list[str]] = {}

    for line in lines:
        side1, side2 = line.split(": ")
        side2_values = side2.split(" ")

        if side1 in connections:
            connections[side1] += side2_values
        else:
            connections[side1] = side2_values

        for side2_value in side2_values:
            if side2_value in connections:
                connections[side2_value] += [side1]
            else:
                connections[side2_value] = [side1]

    return connections

def generate_neato_dot_file(connections: dict[str, list[str]]):
    # Use command "neato -Tpng -o input-graph.png input.dot" to generate image afterwards
    with open(f"{file_name.removesuffix(".txt")}.dot", "w") as file:
        file.write("graph conections {\n")
        for key in connections:
            for connection in connections[key]:
                file.write(f"    {key} -- {connection}\n")
        file.write("}\n")

def find_group_size(connections: dict[str, list[str]], starting_node: str) -> int:
    group_list: set[str] = set()
    second_pass_list: set[str] = set()

    group_list.add(starting_node)
    for connected_connection in connections[starting_node]:
        group_list.add(connected_connection)

    for connection in connections:
        if connection in group_list or any(set(connections[connection]) & set(group_list)):
            group_list.add(connection)
            for connected_connection in connections[connection]:
                group_list.add(connected_connection)
        else:
            second_pass_list.add(connection)
            for connected_connection in connections[connection]:
                second_pass_list.add(connected_connection)

    # Do a equivalent second pass since first pass might miss some values, which would only be later connected
    for connection in second_pass_list:
        if connection in group_list or any(set(connections[connection]) & set(group_list)):
            group_list.add(connection)
            for connected_connection in connections[connection]:
                group_list.add(connected_connection)

    return len(group_list)

def calculate_disconected_group_answer(connections: dict[str, list[str]]) -> int:
    if "test" in file_name:
        raise Exception("Only possible for real input, since connections were manually set")

    # 3 connections to remove to seperate all connections into 2 separate groups, found by looking at the generate graph image
    THREE_CONNECTIONS = ["qqh", "tbq", "xzn"]

    test_connections = connections.copy()
    for connection in THREE_CONNECTIONS:
        del test_connections[connection]

    for key in test_connections:
        for connection in THREE_CONNECTIONS:
            if connection in test_connections[key]:
                test_connections[key].remove(connection)

    # Random node from the left group to check group size for
    LEFT_GROUP_NONE = "xbl"

    # Out of 3 hardcoded connections, which are for left and for right side
    LEFT_GROUP_ADD = 2
    RIGHT_GROUP_ADD = 1

    group_size = find_group_size(test_connections, LEFT_GROUP_NONE)
    other_group_size = len(test_connections) - group_size

    return (group_size + LEFT_GROUP_ADD) * (other_group_size + RIGHT_GROUP_ADD)

_connections = get_initial_data(lines)
generate_neato_dot_file(_connections)

print(f"{calculate_disconected_group_answer(_connections)=}")
