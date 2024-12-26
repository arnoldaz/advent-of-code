def silver_solution(lines: list[str]) -> int:
    return sum(len(line) - len(eval(line)) for line in lines) # pylint: disable=eval-used

def gold_solution(lines: list[str]) -> int:
    return sum(2 + line.count("\\") + line.count("\"") for line in lines)
