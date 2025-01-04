def silver_solution(lines: list[str]) -> int:
    min_present_number = int(lines[0])
    limit = 1_000_000

    sigma_cache = [0] * (limit + 1)
    for i in range(1, limit + 1):
        for j in range(i, limit + 1, i):
            sigma_cache[j] += i

    for i in range(limit + 1):
        if sigma_cache[i] * 10 > min_present_number:
            return i

    return -1

def gold_solution(lines: list[str]) -> int:
    min_present_number = int(lines[0])
    limit = 1_000_000

    sigma_cache = [0] * (limit + 1)
    for i in range(1, limit + 1):
        for j in range(i, min(i * 50 + 1, limit + 1), i):
            sigma_cache[j] += i

    for i in range(limit + 1):
        if sigma_cache[i] * 11 > min_present_number:
            return i

    return -1
