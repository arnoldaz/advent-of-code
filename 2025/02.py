def parse_input(lines: list[str]) -> list[tuple[int, int]]:
    return [
        (int(start), int(end))
        for start, end
        in (number_range.split("-") for number_range in "".join(lines).split(","))
    ]

def silver_solution(lines: list[str]) -> int:
    ranges = parse_input(lines)

    min_digits = len(str(min(start for start, _ in ranges)))
    max_digits = len(str(max(end for _, end in ranges)))

    values = set[int]()
    for digits_count in range(min_digits, max_digits + 1):
        block_length, remainder = divmod(digits_count, 2)
        if remainder != 0:
            continue

        block_start = 10 ** (block_length - 1)
        block_end = (10 ** block_length) - 1

        for repeatable_number in range(block_start, block_end + 1):
            possible_value = int(str(repeatable_number) * 2)
            if any(s <= possible_value <= e for s, e in ranges):
                values.add(possible_value)

    return sum(values)

def gold_solution(lines: list[str]) -> int:
    ranges = parse_input(lines)

    min_digits = len(str(min(start for start, _ in ranges)))
    max_digits = len(str(max(end for _, end in ranges)))

    values = set[int]()
    for digits_count in range(min_digits, max_digits + 1):
        for block_length in range(1, digits_count // 2 + 1):
            repeat_amount, remainder = divmod(digits_count, block_length)
            if remainder != 0:
                continue

            block_start = 10 ** (block_length - 1)
            block_end = (10 ** block_length) - 1

            for repeatable_number in range(block_start, block_end + 1):
                possible_value = int(str(repeatable_number) * repeat_amount)
                if any(s <= possible_value <= e for s, e in ranges):
                    values.add(possible_value)

    return sum(values)
