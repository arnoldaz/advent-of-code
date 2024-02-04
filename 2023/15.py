from functools import reduce

def parse_input(lines: list[str]) -> list[str]:
    return lines[0].split(",")

def calc_hash(step: str) -> int:
    return reduce(lambda value, char: (value + ord(char)) * 17 % 256, step, 0)

def ascii_calculation(sequence: list[str]) -> int:
    return sum(calc_hash(step) for step in sequence)

def hashmap_calculation(sequence: list[str]) -> int:
    hashmap: dict[int, list[tuple[str, int]]] = {}

    for step in sequence:
        if "=" in step:
            label, value = step.split("=")
            box_index = calc_hash(label)
            focal_length = int(value)
            if box_index not in hashmap:
                hashmap[box_index] = [(label, focal_length)]
                continue

            for i, (existing_box_label, _) in enumerate(hashmap[box_index]):
                if existing_box_label == label:
                    hashmap[box_index][i] = (label, focal_length)
                    break
            else:
                hashmap[box_index].append((label, focal_length))
            continue

        if "-" in step:
            label, _ = step.split("-")
            box_index = calc_hash(label)
            if box_index not in hashmap:
                continue

            for i, (existing_box_label, _) in enumerate(hashmap[box_index]):
                if existing_box_label == label:
                    hashmap[box_index].pop(i)
                    break

    return sum((key + 1) * (i + 1) * focal_length for key, value_array in hashmap.items() for i, (_, focal_length) in enumerate(value_array))

def silver_solution(lines: list[str]) -> int:
    sequence = parse_input(lines)
    return ascii_calculation(sequence)

def gold_solution(lines: list[str]) -> int:
    sequence = parse_input(lines)
    return hashmap_calculation(sequence)
