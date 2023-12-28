from typing import NamedTuple

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

class Arangement(NamedTuple):
    data: str
    records: list[int]

arangements = []
for line in lines:
    split_data = line.split(" ")
    arangement_data = split_data[0]
    arangements_records = [int(record) for record in split_data[1].split(",")]
    arangements.append(Arangement(arangement_data, arangements_records))

def check_arangement_correct(arangement: Arangement) -> bool:
    data = arangement.data

    if "?" in data:
        print(f"Questionmark in {arangement=}")
        return False
    
    group_index = 0
    i = 0
    while i != len(data):
        if data[i] == ".":
            i += 1
            continue
        elif data[i] == "#":
            if group_index >= len(arangement.records):
                return False

            if i != 0 and data[i - 1] == "#":
                return False

            record = arangement.records[group_index]
            for j in range(1, record):
                if len(data) <= i + j or data[i + j] != "#":
                    return False

            i += record
            group_index += 1
            continue

    if group_index < len(arangement.records):
        return False

    return True

def check_arangement_possibly_correct(data: str, records: tuple[int, ...]) -> bool:
    group_index = 0
    i = 0
    while i != len(data):
        if data[i] == "?":
            return True
        elif data[i] == ".":
            i += 1
            continue
        elif data[i] == "#":
            if group_index >= len(records):
                return False

            if i != 0 and data[i - 1] == "#":
                return False

            record = records[group_index]
            for j in range(1, record):
                if len(data) <= i + j:
                    return True
                elif data[i + j] == ".":
                    return False

            i += record
            group_index += 1
            continue

    return True
    
global_counter = 0
def count_arangements_recursive(input: str, records: list[int]):
    possibly = check_arangement_possibly_correct(input.split("?")[0], tuple(records))
    if not possibly:
        return

    if "?" in input:
        test1 = input.replace("?", ".", 1)
        count_arangements_recursive(test1, records)

        test2 = input.replace("?", "#", 1)
        count_arangements_recursive(test2, records)
        return
    
    is_correct = check_arangement_correct(Arangement(input, records))
    if is_correct:
        global global_counter
        global_counter += 1

def count_arangements(arangement: Arangement) -> int:
    global global_counter
    global_counter = 0

    count_arangements_recursive(arangement.data, arangement.records)

    return global_counter

final_counter = 0
for arangement in arangements:
    count = count_arangements(arangement)
    final_counter += count
print(f"{final_counter=}")
