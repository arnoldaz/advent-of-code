def parse_input(lines: list[str]) -> list[list[int]]:
    return [[int(symbol) for symbol in line] for line in lines]

def get_total_joltage(number_lists: list[list[int]], total_digits: int) -> int:
    answer = 0
    for number_list in number_lists:
        current_index = -1
        for i in range(total_digits - 1, -1, -1):
            start, end = current_index + 1, len(number_list) - i
            digit = max(number_list[start:end])
            answer += digit * (10 ** i)
            current_index = number_list.index(digit, start, end)

    return answer

def silver_solution(lines: list[str]) -> int:
    number_lists = parse_input(lines)
    return get_total_joltage(number_lists, 2)

def gold_solution(lines: list[str]) -> int:
    number_lists = parse_input(lines)
    return get_total_joltage(number_lists, 12)
