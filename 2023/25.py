# 3 connections to remove to seperate all connections into 2 separate groups, found by looking at the generate graph image
THREE_CONNECTIONS = ["qqh", "tbq", "xzn"]

# Random node from the left group to check group size for
LEFT_GROUP_NODE = "xbl"

# Out of 3 hardcoded connections, which are for left and for right side
LEFT_GROUP_ADD = 2
RIGHT_GROUP_ADD = 1

def parse_input(lines: list[str]) -> dict[str, list[str]]:
    connections: dict[str, list[str]] = {}

    for line in lines:
        side1, side2 = line.split(": ")
        side2_values = side2.split(" ")

        connections.setdefault(side1, []).extend(side2_values)

        for side2_value in side2_values:
            connections.setdefault(side2_value, []).append(side1)

    return connections

def generate_neato_dot_file(connections: dict[str, list[str]]):
    # Use command "neato -Tpng -o temp/input-graph.png temp/input.dot" to generate image afterwards

    connection_pairs: list[tuple[str, str]] = []
    for key in connections:
        for connection in connections[key]:
            if (key, connection) not in connection_pairs and (connection, key) not in connection_pairs:
                connection_pairs.append((key, connection))

    with open("temp/input.dot", "w", encoding="utf-8") as file:
        file.write("graph conections {\n")
        for key1, key2 in connection_pairs:
            file.write(f"    {key1} -- {key2}\n")
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

def silver_solution(lines: list[str]) -> int:
    connections = parse_input(lines)
    # generate_neato_dot_file(connections)

    disconnected_connections = connections.copy()
    for connection in THREE_CONNECTIONS:
        del disconnected_connections[connection]

    for value in disconnected_connections.values():
        for connection in THREE_CONNECTIONS:
            if connection in value:
                value.remove(connection)

    group_size = find_group_size(disconnected_connections, LEFT_GROUP_NODE)
    other_group_size = len(disconnected_connections) - group_size

    return (group_size + LEFT_GROUP_ADD) * (other_group_size + RIGHT_GROUP_ADD)

def gold_solution(_lines: list[str]) -> int:
    return 0
