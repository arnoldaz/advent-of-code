def get_letter_priority(letter: str) -> int:
    return ord(letter) - 38 if letter.isupper() else ord(letter) - 96

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
