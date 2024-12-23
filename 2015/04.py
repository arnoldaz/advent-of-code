from hashlib import md5

def find_md5_postfix_with_leading_zeroes(key: str, zeroes_amount: int) -> int:
    leading_zeroes = "0" * zeroes_amount
    i = 0

    while True:
        key_hash = md5(f"{key}{i}".encode()).hexdigest()
        if key_hash.startswith(leading_zeroes):
            return i

        i += 1

def silver_solution(lines: list[str]) -> int:
    return find_md5_postfix_with_leading_zeroes(lines[0], 5)

def gold_solution(lines: list[str]) -> int:
    return find_md5_postfix_with_leading_zeroes(lines[0], 6)
