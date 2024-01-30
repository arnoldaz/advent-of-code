
def get_letter_priority(letter: str) -> int:
    ascii_number = ord(letter)

    # Upper case letter, need to be converted to range 27-52
    if 65 <= ascii_number <= 90:
        return ascii_number - 38

    # Lower case letter, need to be converted to range 1-26
    if 97 <= ascii_number <= 122:
        return ascii_number - 96

    return -1 # impossible to reach

def silver_solution(lines: list[str]) -> int:
    priority_sum = 0
    for line in lines:
        half_line_length = len(line) // 2
        first_half, second_half = line[:half_line_length], line[half_line_length:]
        common_letter = list(set(first_half) & set(second_half))[0]
        priority_sum += get_letter_priority(common_letter)

    return priority_sum

def gold_solution(lines: list[str]) -> int:
    priority_sum = 0
    for line1, line2, line3 in zip(*[iter(lines)] * 3):
        common_letter = list(set(line1) & set(line2) & set(line3))[0]
        priority_sum += get_letter_priority(common_letter)

    return priority_sum
