from functools import cache
from typing import NamedTuple

class Arangement(NamedTuple):
    data: str
    records: list[int]

def parse_input(lines: list[str], unfold: bool) -> list[Arangement]:
    arangements = []
    unfold_amount = 5

    for line in lines:
        data, records = line.split()
        arangement_data = data if not unfold else "?".join([data] * unfold_amount)
        arangement_records = [int(record) for record in records.split(",")] * (1 if not unfold else unfold_amount)
        arangements.append(Arangement(arangement_data, arangement_records))

    return arangements

@cache
def count_arangements(data: str, groups: tuple[int, ...], group_location = 0, indent=0) -> int:
    if not data:
        # print(indent*"    ", "return", groups, group_location, 1 if len(groups) == 0 and group_location == 0 else 0)
        if len(groups) == 0 and group_location == 0:
            return 1
        if len(groups) == 1 and groups[0] == group_location:
            return 1
        return 0

    # print(indent*"    ", "START", data, groups, group_location)

    counter = 0
    current_symbol = data[0]
    current_group = groups[0] if groups else -1

    for symbol in [current_symbol] if current_symbol != "?" else [".", "#"]:
        if symbol == "#":
            # print(indent*"    ", '"', symbol, '"', "adding counter", data, current_symbol, current_group, group_location)
            counter += count_arangements(data[1:], groups, group_location + 1, indent+1)
        else:
            if group_location > 0:
                if group_location == current_group:
                    # print(indent*"    ", '"', symbol, '"', "adding counter2", data, current_symbol, current_group, group_location)
                    counter += count_arangements(data[1:], groups[1:], 0, indent+1)
                else:
                    # print(indent*"    ", '"', symbol, '"', "not adding", data, current_symbol, current_group, group_location)
                    pass
            else:
                # print(indent*"    ", '"', symbol, '"', "adding counter3", data, current_symbol, current_group, group_location)
                counter += count_arangements(data[1:], groups, group_location, indent+1)

    return counter

# pylint: disable=unused-argument

def silver_solution(lines: list[str]) -> int:
    arangements = parse_input(lines, False)

    final_counter = 0
    for arangement in arangements:
        count = count_arangements(arangement.data, tuple(arangement.records))
        final_counter += count

    return final_counter

def gold_solution(lines: list[str]) -> int:
    arangements = parse_input(lines, True)

    final_counter = 0
    for arangement in arangements:
        count = count_arangements(arangement.data, tuple(arangement.records))
        final_counter += count

    return final_counter
