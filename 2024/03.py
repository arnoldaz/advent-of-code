import re

def silver_solution(lines: list[str]) -> int:
    mul_format = r"mul\((\d+),(\d+)\)"
    line = "".join(lines)

    matches = re.findall(mul_format, line)
    return sum(int(match[0]) * int(match[1]) for match in matches)

def gold_solution(lines: list[str]) -> int:
    mul_format = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
    inner_mul_format = r"mul\((\d+),(\d+)\)"
    line = "".join(lines)

    enabled = True
    final_sum = 0

    matches = re.findall(mul_format, line)
    for match in matches:
        if match == "do()":
            enabled = True
        elif match == "don't()":
            enabled = False
        else:
            if not enabled:
                continue

            inner_matches = re.match(inner_mul_format, match)
            if inner_matches:
                final_sum += int(inner_matches.group(1)) * int(inner_matches.group(2))

    return final_sum
