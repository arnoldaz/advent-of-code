import math
from typing import NamedTuple

from utils.ranges import Range, find_overlap, get_number_amount, remove_overlapping_range, split_range

class Condition(NamedTuple):
    variable: str
    sign: str
    number: int
    destination: str

ACCEPTED_DESTINATION = "A"
REJECTED_DESTINATION = "R"

class Data(NamedTuple):
    x: int
    m: int
    a: int
    s: int

class DataRange:
    def __init__(self, x: Range, m: Range, a: Range, s: Range):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def copy(self) -> "DataRange":
        return DataRange(self.x, self.m, self.a, self.s)

def parse_input(lines: list[str]) -> tuple[list[Data], dict[str, list[Condition]]]:
    commands: dict[str, list[Condition]] = {}
    data = []

    read_commands = True
    for line in lines:
        if line == "":
            read_commands = False
            continue

        if read_commands:
            name, command_data = line.split("{")
            conditions = command_data.strip("}").split(",")
            final_conditions: list[Condition] = []
            for condition in conditions:
                if ":" in condition:
                    comparison, destination = condition.split(":")
                    final_condition = Condition(comparison[0], comparison[1], int(comparison[2:]), destination)
                else:
                    final_condition = Condition("", "", -1, condition)
                final_conditions.append(final_condition)
            commands[name] = final_conditions
        else:
            x, m, a, s = line.strip("{").strip("}").split(",")
            data.append(Data(int(x.removeprefix("x=")), int(m.removeprefix("m=")), int(a.removeprefix("a=")), int(s.removeprefix("s="))))

    return data, commands

def check_accepted(data: Data, commands: dict[str, list[Condition]]) -> bool:
    current_conditions = commands["in"]

    final_result = False
    found = False
    while not found:
        for condition in current_conditions:
            condition_passed = False
            match condition.variable:
                case "x":
                    match condition.sign:
                        case "<":
                            condition_passed = data.x < condition.number
                        case ">":
                            condition_passed = data.x > condition.number
                case "m":
                    match condition.sign:
                        case "<":
                            condition_passed = data.m < condition.number
                        case ">":
                            condition_passed = data.m > condition.number
                case "a":
                    match condition.sign:
                        case "<":
                            condition_passed = data.a < condition.number
                        case ">":
                            condition_passed = data.a > condition.number
                case "s":
                    match condition.sign:
                        case "<":
                            condition_passed = data.s < condition.number
                        case ">":
                            condition_passed = data.s > condition.number
                case "":
                    condition_passed = True

            if condition_passed:
                if condition.destination == "A":
                    final_result = True
                    found = True
                    break
                elif condition.destination == "R":
                    final_result = False
                    found = True
                    break
                else:
                    current_conditions = commands[condition.destination]
                    break

    return final_result

def calculate_accepted_sum(data: list[Data], commands: dict[str, list[Condition]]) -> int:
    result = 0

    for entry in data:
        if check_accepted(entry, commands):
            result += entry.x + entry.m + entry.a + entry.s

    return result


# pylint: disable=unused-argument

def silver_solution(lines: list[str]) -> int:
    data, commands = parse_input(lines)
    return calculate_accepted_sum(data, commands)

def gold_solution(lines: list[str]) -> int:
    _, commands = parse_input(lines)

    ranges = DataRange(Range(1, 4000), Range(1, 4000), Range(1, 4000), Range(1, 4000))

    return recursive_shit("in", commands, ranges)

def recursive_shit(root: str, commands: dict[str, list[Condition]], ranges: DataRange) -> int:
    if root == "A":
        return get_number_amount(ranges.x) * get_number_amount(ranges.m) * get_number_amount(ranges.a) * get_number_amount(ranges.s)
    if root == "R":
        return 0

    result = 0
    for line in commands[root]:
        cloned_range = ranges.copy()
        leftover_ranges = ranges.copy()
        match line.variable:
            case "x":
                if line.sign == "<":
                    cloned_range.x = Range(ranges.x.start, line.number - 1)
                    leftover_ranges.x = Range(line.number, ranges.x.end)
                else:
                    cloned_range.x = Range(line.number + 1, ranges.x.end)
                    leftover_ranges.x = Range(ranges.x.start, line.number)
            case "m":
                if line.sign == "<":
                    cloned_range.m = Range(ranges.m.start, line.number - 1)
                    leftover_ranges.m = Range(line.number, ranges.m.end)
                else:
                    cloned_range.m = Range(line.number + 1, ranges.m.end)
                    leftover_ranges.m = Range(ranges.m.start, line.number)
            case "a":
                if line.sign == "<":
                    cloned_range.a = Range(ranges.a.start, line.number - 1)
                    leftover_ranges.a = Range(line.number, ranges.a.end)
                else:
                    cloned_range.a = Range(line.number + 1, ranges.a.end)
                    leftover_ranges.a = Range(ranges.a.start, line.number)
            case "s":
                if line.sign == "<":
                    cloned_range.s = Range(ranges.s.start, line.number - 1)
                    leftover_ranges.s = Range(line.number, ranges.s.end)
                else:
                    cloned_range.s = Range(line.number + 1, ranges.s.end)
                    leftover_ranges.s = Range(ranges.s.start, line.number)

        result += recursive_shit(line.destination, commands, cloned_range)
        ranges = leftover_ranges.copy()

    return result
