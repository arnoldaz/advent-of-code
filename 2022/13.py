import json
from typing import NamedTuple, Optional
from functools import cmp_to_key

RecursiveList = int | list["int | RecursiveList"]

class Pair(NamedTuple):
    left: RecursiveList
    right: RecursiveList

def parse_input(lines: list[str]) -> list[Pair]:
    input_lines = [line for line in lines if line.strip()]
    return [Pair(json.loads(left), json.loads(right)) for left, right in zip(input_lines[::2], input_lines[1::2])]

def compare_data(left: RecursiveList, right: RecursiveList) -> Optional[bool]:
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            result = compare_data(left[i], right[i])
            if result is not None:
                return result

        return len(right) > len(left) if len(left) != len(right) else None

    if isinstance(left, int) and isinstance(right, int):
        return left < right if left != right else None

    if isinstance(left, int) and isinstance(right, list):
        return compare_data([left], right)

    if isinstance(left, list) and isinstance(right, int):
        return compare_data(left, [right])

    raise ValueError("Impossible to reach")

def silver_solution(lines: list[str]) -> int:
    pairs = parse_input(lines)
    return sum(i + 1 for i, pair in enumerate(pairs) if compare_data(pair.left, pair.right))

def gold_solution(lines: list[str]) -> int:
    pairs = parse_input(lines)
    all_packets = [packet for pair in pairs for packet in (pair.left, pair.right)]

    divider1: RecursiveList = [[2]]
    divider2: RecursiveList = [[6]]
    all_packets += [divider1, divider2]

    all_packets.sort(key=cmp_to_key(lambda a, b: -1 if compare_data(a, b) else 1))

    divider_index1 = all_packets.index(divider1) + 1
    divider_index2 = all_packets.index(divider2) + 1
    return divider_index1 * divider_index2
