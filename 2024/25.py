from itertools import groupby

def parse_input(lines: list[str]) -> tuple[list[list[int]], list[list[int]]]:
    schematics = [list(group) for key, group in groupby(lines, key=bool) if key]
    lock_schematics = [line for line in schematics if all(char == "#" for char in line[0])]
    key_schematics = [line for line in schematics if all(char == "#" for char in line[-1])]

    locks = [[str(column).count("#") - 1 for column in zip(*lock)] for lock in lock_schematics]
    keys = [[str(column).count("#") - 1 for column in zip(*key)] for key in key_schematics]

    return locks, keys

def silver_solution(lines: list[str]) -> int:
    locks, keys = parse_input(lines)
    pin_amount = len(locks[0])

    fit_together_counter = 0

    for lock in locks:
        for key in keys:
            for i in range(pin_amount):
                if key[i] + lock[i] >= 6:
                    break
            else:
                fit_together_counter += 1

    return fit_together_counter

def gold_solution(_lines: list[str]) -> int:
    return 0
