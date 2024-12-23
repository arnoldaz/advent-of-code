def silver_solution(lines: list[str]) -> int:
    instructions = lines[0]
    return instructions.count("(") - instructions.count(")")

def gold_solution(lines: list[str]) -> int:
    instructions = lines[0]

    floor = 0
    for i, instruction in enumerate(instructions):
        floor += 1 if instruction == "(" else -1
        if floor == -1:
            return i + 1

    return -1
