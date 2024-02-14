from typing import NamedTuple
from utils.ranges import Range

class AssignmentPair(NamedTuple):
    left: Range
    right: Range

def parse_input(lines: list[str]) -> list[AssignmentPair]:
    assignment_pairs: list[AssignmentPair] = []
    for line in lines:
        left, right = line.split(",")
        left_start, left_end = left.split("-")
        right_start, right_end = right.split("-")
        assignment_pairs.append(AssignmentPair(Range(int(left_start), int(left_end)), Range(int(right_start), int(right_end))))

    return assignment_pairs

def silver_solution(lines: list[str]) -> int:
    return sum(1 for pair in parse_input(lines) if pair.left.is_range_inside(pair.right) or pair.right.is_range_inside(pair.left))

def gold_solution(lines: list[str]) -> int:
    return sum(1 for pair in parse_input(lines) if pair.left.find_overlap(pair.right))
