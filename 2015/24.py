from math import prod
from itertools import combinations

def find_smallest_entanglement(weights: list[int], group_count: int) -> int:
    group_weight = sum(weights) // group_count

    for i in range(len(weights)):
        entanglement = [prod(group) for group in combinations(weights, i) if sum(group) == group_weight]
        if entanglement:
            return min(entanglement)

    return -1

def silver_solution(lines: list[str]) -> int:
    weights = [int(line) for line in lines]
    return find_smallest_entanglement(weights, 3)

def gold_solution(lines: list[str]) -> int:
    weights = [int(line) for line in lines]
    return find_smallest_entanglement(weights, 4)
