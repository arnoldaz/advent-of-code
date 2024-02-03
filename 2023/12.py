from functools import cache

def parse_input(lines: list[str], unfold: bool) -> list[tuple[str, list[int]]]:
    arangements: list[tuple[str, list[int]]] = []
    unfold_amount = 5

    for line in lines:
        data, records = line.split()
        arangement_data = data if not unfold else "?".join([data] * unfold_amount)
        arangement_records = [int(record) for record in records.split(",")] * (1 if not unfold else unfold_amount)
        arangements.append((arangement_data, arangement_records))

    return arangements

@cache
def count_arangements(data: str, groups: tuple[int, ...], group_location = 0) -> int:
    if not data:
        if len(groups) == 0 and group_location == 0:
            return 1
        if len(groups) == 1 and groups[0] == group_location:
            return 1
        return 0

    counter = 0
    current_symbol = data[0]
    current_group = groups[0] if groups else -1

    for symbol in [current_symbol] if current_symbol != "?" else [".", "#"]:
        if symbol == "#":
            counter += count_arangements(data[1:], groups, group_location + 1)
        else:
            if group_location > 0:
                if group_location == current_group:
                    counter += count_arangements(data[1:], groups[1:], 0)
            else:
                counter += count_arangements(data[1:], groups, group_location)

    return counter

def silver_solution(lines: list[str]) -> int:
    arangements = parse_input(lines, False)
    return sum(count_arangements(data, tuple(groups)) for data, groups in arangements)

def gold_solution(lines: list[str]) -> int:
    arangements = parse_input(lines, True)
    return sum(count_arangements(data, tuple(groups)) for data, groups in arangements)
