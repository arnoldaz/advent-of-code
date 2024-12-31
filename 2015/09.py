from itertools import permutations

def parse_input(lines: list[str]) -> dict[str, dict[str, int]]:
    distance_map: dict[str, dict[str, int]] = {}
    for line in lines:
        start, _, end, _, distance = line.split()
        distance_map.setdefault(start, {})[end] = int(distance)
        distance_map.setdefault(end, {})[start] = int(distance)

    return distance_map

def get_all_distances(distance_map: dict[str, dict[str, int]]) -> list[int]:
    return [sum(distance_map[location][next_location] for location, next_location in zip(permutation, permutation[1:]))
            for permutation in permutations(distance_map.keys())]

def silver_solution(lines: list[str]) -> int:
    distance_map = parse_input(lines)
    return min(get_all_distances(distance_map))

def gold_solution(lines: list[str]) -> int:
    distance_map = parse_input(lines)
    return max(get_all_distances(distance_map))
