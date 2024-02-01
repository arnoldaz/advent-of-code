import re
from typing import NamedTuple

class Move(NamedTuple):
    amount: int
    from_crate: int
    to_crate: int

def parse_input(lines: list[str]) -> tuple[list[list[str]], list[Move]]:
    column_end_line_index, column_count = next((index, int(line.rstrip()[-1])) for index, line in enumerate(lines) if line.replace(" ", "").isdigit())
    column_x_indexes = [1 + 4 * x for x in range(column_count)]
    crates: list[list[str]] = [[] for _ in range(column_count)]

    for y in range(column_end_line_index):
        line = lines[y]
        for i, index in enumerate(column_x_indexes):
            char = line[index] if len(line) > index else ""
            if char.strip():
                crates[i].insert(0, char)

    moves: list[Move] = []
    move_format = r"move (\d+) from (\d+) to (\d+)"
    for line in lines[column_end_line_index+2:]:
        match = re.match(move_format, line)
        if not match:
            continue

        moves.append(Move(int(match.group(1)), int(match.group(2)), int(match.group(3))))

    return crates, moves

def silver_solution(lines: list[str]) -> str:
    crates, moves = parse_input(lines)

    for move in moves:
        for _ in range(move.amount):
            crates[move.to_crate - 1].append(crates[move.from_crate - 1].pop())

    return "".join(stack[-1] for stack in crates)

def gold_solution(lines: list[str]) -> str:
    crates, moves = parse_input(lines)

    for move in moves:
        moved_crate_stack = reversed([crates[move.from_crate - 1].pop() for _ in range(move.amount)])
        crates[move.to_crate - 1] += moved_crate_stack

    return "".join(stack[-1] for stack in crates)
