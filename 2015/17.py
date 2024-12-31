import sys

def find_different_container_combinations(current_liters: int, target_liters: int, left_containers: list[int], current_container_count: int, target_container_count: int) -> int:
    if current_liters == target_liters:
        if target_container_count != -1:
            return int(current_container_count == target_container_count)

        return 1

    if current_liters > target_liters:
        return 0

    if not left_containers:
        return 0

    return sum(
        find_different_container_combinations(current_liters + container, target_liters, left_containers[i+1:], current_container_count + 1, target_container_count)
        for i, container in enumerate(left_containers)
    )

def find_minimum_container_count(current_liters: int, target_liters: int, left_containers: list[int], current_container_count: int) -> int:
    if current_liters == target_liters:
        return current_container_count

    if current_liters > target_liters:
        return sys.maxsize

    if not left_containers:
        return sys.maxsize

    return min(
        find_minimum_container_count(current_liters + container, target_liters, left_containers[i+1:], current_container_count + 1)
        for i, container in enumerate(left_containers)
    )

def silver_solution(lines: list[str]) -> int:
    containers = [int(line) for line in lines]
    return find_different_container_combinations(0, 150, containers, 0, -1)

def gold_solution(lines: list[str]) -> int:
    containers = [int(line) for line in lines]
    min_container_count = find_minimum_container_count(0, 150, containers, 0)
    return find_different_container_combinations(0, 150, containers, 0, min_container_count)
