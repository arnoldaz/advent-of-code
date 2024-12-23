def is_string_nice(string: str) -> bool:
    if sum(map(string.count, ["a", "e", "i", "o", "u"])) < 3:
        return False

    if not any(x == y for x, y in zip(string, string[1:])):
        return False

    if any(x in string for x in ["ab", "cd", "pq", "xy"]):
        return False

    return True

def is_string_nice_updated(string: str) -> bool:
    unique_pairs = set(x + y for x, y in zip(string, string[1:]))
    if not any(x > 1 for x in map(string.count, unique_pairs)):
        return False

    for i in range(1, len(string)-1):
        if string[i-1] == string[i+1]:
            return True
    else:
        return False

def silver_solution(lines: list[str]) -> int:
    return sum(1 for string in lines if is_string_nice(string))

def gold_solution(lines: list[str]) -> int:
    return sum(1 for string in lines if is_string_nice_updated(string))
