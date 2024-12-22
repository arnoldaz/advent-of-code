def next_secret_number(number: int):
    first_step = (number ^ (number * 64)) % 16777216
    second_step = (first_step ^ (first_step // 32)) % 16777216
    third_step = (second_step ^ (second_step * 2048)) % 16777216
    return third_step

def create_price_mappings(numbers: list[int]) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    digits_map: dict[int, list[int]] = {}
    diffs_map: dict[int, list[int]] = {}
    for number in numbers:
        secret_number = number
        secret_numbers: list[int] = [secret_number % 10]
        for _ in range(2000):
            secret_number = next_secret_number(secret_number)
            secret_numbers.append(secret_number % 10)
        digits_map[number] = secret_numbers

        diffs: list[int] = []
        for first, second in zip(secret_numbers, secret_numbers[1:]):
            diffs.append(second - first)
        diffs_map[number] = diffs

    return digits_map, diffs_map

def get_possible_sequences(digits_map: dict[int, list[int]], diffs_map: dict[int, list[int]]):
    sequence_final: dict[tuple[int, int, int, int], int] = {}
    for key, values in diffs_map.items():
        added_sequences = set()
        for i in range(len(values) - 3):
            sequence = (values[i], values[i+1], values[i+2], values[i+3])
            if sequence in added_sequences:
                continue

            added_sequences.add(sequence)

            sell_price = digits_map[key][i+4]
            sequence_final[sequence] = sequence_final.get(sequence, 0) + sell_price

    return sequence_final

def silver_solution(lines: list[str]) -> int:
    numbers = [int(line) for line in lines]

    result = 0
    for number in numbers:
        for _ in range(2000):
            number = next_secret_number(number)
        result += number
    return result

def gold_solution(lines: list[str]) -> int:
    numbers = [int(line) for line in lines]

    digits_map, diffs_map = create_price_mappings(numbers)
    sequences = get_possible_sequences(digits_map, diffs_map)

    return max(sequences.values())
