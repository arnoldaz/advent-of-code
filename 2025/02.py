import re

def parse_input(lines: list[str]) -> list[tuple[int, int]]:
    line = "".join(lines)
    ranges: list[tuple[int, int]] = []

    for range in line.split(","):
        start, end = range.split("-")
        ranges.append((int(start), int(end)))

    return ranges

def find_invalid_sum(ranges: list[tuple[int, int]], allow_multiple_repeats: bool) -> int:
    invalid_number_regex = r"^([0-9]+)\1+$" if allow_multiple_repeats else r"^([0-9]+)\1$"
    answer = 0

    for start, end in ranges:
        for number in range(start, end + 1):
            matches = re.match(invalid_number_regex, str(number))
            if matches is not None:
                answer += number

    return answer

def silver_solution(lines: list[str]) -> int:
    ranges = parse_input(lines)
    return find_invalid_sum(ranges, False)

def gold_solution(lines: list[str]) -> int:
    ranges = parse_input(lines)
    return find_invalid_sum(ranges, True)
