def parse_input(lines: list[str]) -> list[str]:
    line = lines[0] # only single line
    return line.split(",")

def calc_hash(step: str) -> int:
    current_value = 0
    for char in step:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value

def ascii_calculation(sequence: list[str]) -> int:
    final_value = 0
    for step in sequence:
        final_value += calc_hash(step)
    return final_value

def hashmap_calculation(sequence: list[str]) -> int:
    hashmap: dict[int, list[tuple[str, int]]] = {}

    for step in sequence:
        equals = step.split("=")
        if len(equals) > 1:
            index = calc_hash(equals[0])
            value = int(equals[1])
            if index in hashmap:
                for i, iter_value in enumerate(hashmap[index]):
                    first, _ = iter_value
                    if first == equals[0]:
                        found = True
                        secondary_index = i
                        break
                else:
                    found = False
                    secondary_index = -1 # impossible to use

                if not found:
                    hashmap[index].append((equals[0], value))
                else:
                    hashmap[index][secondary_index] = (equals[0], value)
            else:
                hashmap[index] = [(equals[0], value)]

            continue

        equals = step.split("-")
        if len(equals) > 1:
            index = calc_hash(equals[0])
            if index in hashmap:
                for i, iter_value in enumerate(hashmap[index]):
                    first, _ = iter_value
                    if first == equals[0]:
                        found = True
                        secondary_index = i
                        break
                else:
                    found = False
                    secondary_index = -1 # impossible to use

                if found:
                    hashmap[index].pop(secondary_index)

            continue

    final_value = 0

    for key in hashmap:
        value_array = hashmap[key]
        for i, value in enumerate(value_array):
            final_value += (key + 1) * (i + 1) * value[1]

    return final_value

def silver_solution(lines: list[str]) -> int:
    sequence = parse_input(lines)
    return ascii_calculation(sequence)

def gold_solution(lines: list[str]) -> int:
    sequence = parse_input(lines)
    return hashmap_calculation(sequence)
