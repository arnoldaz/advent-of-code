import re
from typing import NamedTuple, Optional
from utils.ranges import Range, SplitMode

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

class DataRange(NamedTuple):
    x: Range
    m: Range
    a: Range
    s: Range

    def copy(self, x: Optional[Range] = None, m: Optional[Range] = None, a: Optional[Range] = None, s: Optional[Range] = None) -> "DataRange":
        return DataRange(x or self.x, m or self.m, a or self.a, s or self.s)

def parse_input(lines: list[str]) -> tuple[list[Data], dict[str, list[Condition]]]:
    commands: dict[str, list[Condition]] = {}
    data: list[Data] = []

    data_format = r"^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$"

    read_commands = True
    for line in lines:
        if not line:
            read_commands = False
            continue

        if read_commands:
            name, command_data = line.split("{")
            conditions = command_data.removesuffix("}").split(",")
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
            match = re.match(data_format, line)
            assert match, "Regex match should always find data"
            data.append(Data(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))))

    return data, commands

def check_accepted(data: Data, commands: dict[str, list[Condition]]) -> bool:
    current_conditions = commands["in"]

    found = False
    while not found:
        for condition in current_conditions:
            condition_passed = False
            variable = -1

            match condition.variable:
                case "x":
                    variable = data.x
                case "m":
                    variable = data.m
                case "a":
                    variable = data.a
                case "s":
                    variable = data.s

            match condition.sign:
                case "<":
                    condition_passed = variable < condition.number
                case ">":
                    condition_passed = variable > condition.number

            if not condition.variable: # no condition
                condition_passed = True

            if condition_passed:
                if condition.destination == "A":
                    return True
                if condition.destination == "R":
                    return False
                current_conditions = commands[condition.destination]
                break

    return False

def count_distinct_accepted_combinations(destination: str, commands: dict[str, list[Condition]], ranges: DataRange) -> int:
    if destination == "A":
        return ranges.x.get_number_count() * ranges.m.get_number_count() * ranges.a.get_number_count() * ranges.s.get_number_count()
    if destination == "R":
        return 0

    result = 0
    for condition in commands[destination]:
        match condition.variable:
            case "x":
                if condition.sign == "<":
                    left, right = ranges.x.split_range(condition.number, SplitMode.INCLUDE_RIGHT)
                    cloned_range = ranges.copy(x=left)
                    leftover_ranges = ranges.copy(x=right)
                else:
                    left, right = ranges.x.split_range(condition.number, SplitMode.INCLUDE_LEFT)
                    cloned_range = ranges.copy(x=right)
                    leftover_ranges = ranges.copy(x=left)
            case "m":
                if condition.sign == "<":
                    left, right = ranges.m.split_range(condition.number, SplitMode.INCLUDE_RIGHT)
                    cloned_range = ranges.copy(m=left)
                    leftover_ranges = ranges.copy(m=right)
                else:
                    left, right = ranges.m.split_range(condition.number, SplitMode.INCLUDE_LEFT)
                    cloned_range = ranges.copy(m=right)
                    leftover_ranges = ranges.copy(m=left)
            case "a":
                if condition.sign == "<":
                    left, right = ranges.a.split_range(condition.number, SplitMode.INCLUDE_RIGHT)
                    cloned_range = ranges.copy(a=left)
                    leftover_ranges = ranges.copy(a=right)
                else:
                    left, right = ranges.a.split_range(condition.number, SplitMode.INCLUDE_LEFT)
                    cloned_range = ranges.copy(a=right)
                    leftover_ranges = ranges.copy(a=left)
            case "s":
                if condition.sign == "<":
                    left, right = ranges.s.split_range(condition.number, SplitMode.INCLUDE_RIGHT)
                    cloned_range = ranges.copy(s=left)
                    leftover_ranges = ranges.copy(s=right)
                else:
                    left, right = ranges.s.split_range(condition.number, SplitMode.INCLUDE_LEFT)
                    cloned_range = ranges.copy(s=right)
                    leftover_ranges = ranges.copy(s=left)
            case _:
                cloned_range = ranges.copy()
                leftover_ranges = ranges.copy()

        result += count_distinct_accepted_combinations(condition.destination, commands, cloned_range)
        ranges = leftover_ranges.copy()

    return result

def silver_solution(lines: list[str]) -> int:
    data, commands = parse_input(lines)
    return sum(entry.x + entry.m + entry.a + entry.s for entry in data if check_accepted(entry, commands))

def gold_solution(lines: list[str]) -> int:
    _, commands = parse_input(lines)
    initial_ranges = DataRange(Range(1, 4000), Range(1, 4000), Range(1, 4000), Range(1, 4000))

    return count_distinct_accepted_combinations("in", commands, initial_ranges)
