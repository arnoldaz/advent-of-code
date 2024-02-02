def are_chars_unique(string: str):
    return len(string) == len(set(string))

def get_marker_start(datastream: str, marker_size: int) -> int:
    for i in range(marker_size - 1, len(datastream)):
        possible_marker = datastream[i-(marker_size-1):i+1]
        if are_chars_unique(possible_marker):
            return i + 1

    return -1

def silver_solution(lines: list[str]) -> int:
    return get_marker_start(lines[0], 4)

def gold_solution(lines: list[str]) -> int:
    return get_marker_start(lines[0], 14)
