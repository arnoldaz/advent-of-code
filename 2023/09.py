from functools import reduce

def parse_input(lines: list[str]) -> list[list[int]]:
    return [[int(x) for x in line.split(" ")] for line in lines]

def get_sequence_tree(history: list[int]) -> list[list[int]]:
    sequences: list[list[int]] = [history]
    current_sequence = history
    while any(x != 0 for x in current_sequence):
        sequence = [current_sequence[i] - current_sequence[i-1] for i in range(1, len(current_sequence))]
        sequences.append(sequence)
        current_sequence = sequence

    return sequences

def silver_solution(lines: list[str]) -> int:
    histories = parse_input(lines)
    return sum(sequence[-1] for history in histories for sequence in get_sequence_tree(history))

def gold_solution(lines: list[str]) -> int:
    histories = parse_input(lines)
    return sum(reduce(lambda acc, sequence: sequence[0] - acc, reversed(get_sequence_tree(history)), 0) for history in histories)
