def parse_input(lines: list[str]) -> tuple[list[int], list[int]]:
    left_list, right_list = zip(*[(int(left), int(right)) for line in lines for left, right in [line.split()]])
    return list(left_list), list(right_list)

def silver_solution(lines: list[str]) -> int:
    left_list, right_list = parse_input(lines)

    left_list.sort()
    right_list.sort()
    
    return sum(abs(left - right) for left, right in zip(left_list, right_list))

def gold_solution(lines: list[str]) -> int:
    left_list, right_list = parse_input(lines)

    return sum(left * right_list.count(left) for left in left_list)
