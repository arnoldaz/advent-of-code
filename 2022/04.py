
from typing import NamedTuple
from utils.ranges import Range, find_overlap, range_in_range

class AssigmentPair(NamedTuple):
    left: Range
    right: Range

def parse_input(lines: list[str]) -> list[AssigmentPair]:
    assignment_pairs: list[AssigmentPair] = []
    for line in lines:
        left, right = line.split(",")
        left_start, left_end = left.split("-")
        right_start, right_end = right.split("-")
        assignment_pairs.append(AssigmentPair(Range(int(left_start), int(left_end)), Range(int(right_start), int(right_end))))

    return assignment_pairs

def silver_solution(lines: list[str]) -> int:
    return sum(1 for pair in parse_input(lines) if range_in_range(pair.left, pair.right) or range_in_range(pair.right, pair.left))

def gold_solution(lines: list[str]) -> int:
    return sum(1 for pair in parse_input(lines) if find_overlap(pair.left, pair.right))
