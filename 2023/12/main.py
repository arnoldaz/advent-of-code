from functools import cache
from typing import NamedTuple
import time

file_name = "unfolded-input-test.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

# print(lines)

class Arangement(NamedTuple):
    data: str
    records: list[int]

arangements = []
for line in lines:
    split_data = line.split(" ")
    arangement_data = split_data[0]
    arangements_records = [int(record) for record in split_data[1].split(",")]
    arangements.append(Arangement(arangement_data, arangements_records))

# print(arangements)


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

@cache
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
            # if len(data) >= i + 1 and data[i] == "#":
            #     return False 

            group_index += 1
            continue

    return True
    
global_counter = 0
def count_arangements_recursive(input: str, records: list[int]):
    # start_time = time.perf_counter()
    possibly = check_arangement_possibly_correct(input.split("?")[0], tuple(records))
    # end_time = time.perf_counter()
    if not possibly:
        return

    print(f"{input=} {possibly=}")


    if "?" in input:
        test1 = input.replace("?", ".", 1)
        count_arangements_recursive(test1, records)

        test2 = input.replace("?", "#", 1)
        count_arangements_recursive(test2, records)
        return
    
    # start_time = time.perf_counter()
    is_correct = check_arangement_correct(Arangement(input, records))
    # end_time = time.perf_counter()
    # print(f"check {end_time-start_time=}")
    if is_correct:
        global global_counter
        global_counter += 1

def count_arangements(arangement: Arangement) -> int:
    global global_counter
    global_counter = 0

    count_arangements_recursive(arangement.data, arangement.records)

    return global_counter



# final_counter = 0
# for arangement in arangements:
#     print(f"{arangement=}")
#     count = count_arangements(arangement)
#     print(f"{count=}")
#     final_counter += count
# print(f"{final_counter=}")


# arangement = Arangement('#.?????????#?', [1, 8])
# arangement = Arangement(".??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.", [1,1,3,1,1,3,1,1,3,1,1,3,1,1,3])
# arangement = Arangement(".??..??...?##.", [1,1,3])

# arangement = Arangement("?###????????", [3,2,1])

arangement = Arangement("?###??????????###??????????###??????????###??????????###????????", [3,2,1,3,2,1,3,2,1,3,2,1,3,2,1])
# arangement = Arangement(".###.......#", [3,2,1,3,2,1,3,2,1,3,2,1,3,2,1])
# arangement = Arangement("?#????????????###????#????????????###????#????????????###????#????????????###????#????????????###??", [1,3,9,1,1,3,9,1,1,3,9,1,1,3,9,1,1,3,9,1])


arangements = count_arangements(arangement)
print(f"{arangements=}")


# arangement = Arangement(".###....###?", [3,2,1])
# arangement = Arangement(".####???????", [3,2,1])
# print(f"{check_arangement_possibly_correct(arangement)}")