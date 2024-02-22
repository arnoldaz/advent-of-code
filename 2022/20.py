def calculate_mixing_sum(numbers: list[int], iterations: int) -> int:
    length = len(numbers)

    number_keys = list(enumerate(numbers))
    zero_key = (numbers.index(0), 0)

    for number_key in number_keys[:] * iterations:
        initial_index = number_keys.index(number_key)
        amount_to_move = number_key[1]

        number_keys.pop(initial_index)
        new_index = (initial_index + amount_to_move) % (length - 1)
        number_keys.insert(new_index, number_key)

    zero_key_index = number_keys.index(zero_key)
    return sum(number_keys[(zero_key_index + i) % length][1] for i in [1000, 2000, 3000])

def silver_solution(lines: list[str]) -> int:
    numbers = [int(line) for line in lines]
    return calculate_mixing_sum(numbers, 1)

def gold_solution(lines: list[str]) -> int:
    multiply_amount = 811589153
    numbers = [int(line) * multiply_amount for line in lines]
    return calculate_mixing_sum(numbers, 10)
