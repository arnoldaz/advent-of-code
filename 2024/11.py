from functools import cache

@cache
def blink_number_recursive(number: int, depth: int, required_depth: int) -> int:
    if depth == required_depth:
        return 1

    if number == 0:
        return blink_number_recursive(1, depth + 1, required_depth)

    digits = str(number)
    digit_count = len(digits)
    if digit_count % 2 == 0:
        half = digit_count // 2
        left, right = int(digits[:half]), int(digits[half:])
        return blink_number_recursive(left, depth + 1, required_depth) + blink_number_recursive(right, depth + 1, required_depth)

    return blink_number_recursive(number * 2024, depth + 1, required_depth)

def silver_solution(lines: list[str]) -> int:
    numbers = [int(char) for char in lines[0].split()]
    return sum(blink_number_recursive(number, 0, 25) for number in numbers)

def gold_solution(lines: list[str]) -> int:
    numbers = [int(char) for char in lines[0].split()]
    return sum(blink_number_recursive(number, 0, 75) for number in numbers)
