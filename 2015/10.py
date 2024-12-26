from functools import reduce
from itertools import groupby

def transform_number(number: str) -> str:
    same_digit_groups = ["".join(group) for _, group in groupby(number)]
    return "".join(str(len(digits)) + digits[0] for digits in same_digit_groups)

def get_transformed_number_length(number: str, loop_amount: int) -> int:
    return len(reduce(lambda x, _: transform_number(x), range(loop_amount), number))

def silver_solution(lines: list[str]) -> int:
    return get_transformed_number_length(lines[0], 40)

def gold_solution(lines: list[str]) -> int:
    return get_transformed_number_length(lines[0], 50)
