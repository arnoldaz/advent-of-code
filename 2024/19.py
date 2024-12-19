# pylint: disable=unused-argument



def parse_input(lines: list[str]) -> tuple[list[str], list[str]]:
    patterns = lines[0].split(", ")
    return patterns, lines[2:]

# def get_paths_bfs(valves: dict[str, ValveData], start_valve: str, end_valves: list[str]) -> list[list[str]]:
#     frontier = queue.Queue[tuple[str, list[str]]]()
#     frontier.put((start_valve, []))
#     visited = set([start_valve])
#     all_paths: list[list[str]] = []

#     while not frontier.empty():
#         current, path = frontier.get()
#         for neighbor in valves[current].tunnels:
#             if neighbor not in visited:
#                 visited.add(neighbor)
#                 new_path = path + [neighbor]
#                 frontier.put((neighbor, new_path))
#                 if neighbor in end_valves:
#                     all_paths.append(new_path)

#     return all_paths

# def find_all_paths(graph: dict[Point, dict[Point, int]], start: Point, end: Point, path: list[Point], visited: list[Point]) -> list[list[Point]]:
#     path = path + [start]
#     if start == end:
#         return [path]

#     if start not in graph or start in visited:
#         return []

#     visited.append(start)

#     paths: list[list[Point]] = []
#     for node in graph[start]:
#         if node not in path:
#             new_paths = find_all_paths(graph, node, end, path, visited.copy())
#             for new_path in new_paths:
#                 paths.append(new_path)

#     visited.remove(start)

#     return paths

cache = {}

def get_key(current_design: str, target_design: str, path: list[str]):
    return current_design + ";" + target_design + ";" + ",".join(path)

def find_arangements(patterns: list[str], current_design: str, target_design: str, path: list[str], visited: list[str]) -> list[list[str]]:
    # print(current_design, path, visited)
    # key = get_key(current_design, target_design, path)
    # print(key)
    # if key in cache:
    #     print("found", key)
    #     return cache[key]

    if current_design != "":
        path = path + [current_design]
    if current_design == target_design:
        return [path]
    
    if current_design in visited:
        return []

    visited.append(current_design)

    paths: list[list[str]] = []
    possible_options: list[str] = []
    for pattern in patterns:
        if target_design.startswith(current_design + pattern):
            possible_options.append(pattern)


    for option in possible_options:
        new_paths = find_arangements(patterns, current_design + option, target_design, path, visited.copy())
        for new_path in new_paths:
            paths.append(new_path)

    visited.remove(current_design)

    # cache[key] = paths

    # print(len(paths))
    return paths


def silver_solution(lines: list[str]) -> int:
    patterns, designs = parse_input(lines)

    # print(patterns)
    # print(designs)

    res = 0
    for design in designs:
        print(design)
        test = find_arangements(patterns, "", design, [], [])
        print(test)
        res += len(test)

    return res

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
