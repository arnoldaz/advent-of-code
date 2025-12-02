
def parse_input(lines: list[str]) -> list[tuple[int, int]]:
    line = "".join(lines)
    result: list[tuple[int, int]] = []
    
    ranges = line.split(",")
    for range in ranges:
        left, right = range.split("-")
        result.append((int(left), int(right)))

    return result

def check_repeating(digits: list[int], amount: int, limit_twice: bool) -> bool:
    split_lists: list[list[int]] = []

    i = 0
    while i < len(digits):
        new_list: list[int] = []
        for _ in range(amount):
            if i == len(digits):
                break
            new_list.append(digits[i])
            i += 1
        split_lists.append(new_list)

    if limit_twice and len(split_lists) > 2:
        return False

    for split_list in split_lists:
        if split_list != split_lists[0]:
            return False

    return True

def silver_solution(lines: list[str]) -> int: # runs for ~6s
    ranges = parse_input(lines)
    result = 0

    for left, right in ranges:
        for i in range(left, right + 1):
            digits = [int(digit) for digit in str(i)]
            # print(left, "-", right, "->", digits)
            repeating = False
            
            for amount in range(1, len(digits) // 2 + 1):
                # print(amount)
                is_repeating = check_repeating(digits, amount, True)
                if is_repeating:
                    repeating = True
                    break
            
            if repeating:
                result += i

    return result

def gold_solution(lines: list[str]) -> int: # runs for ~6s
    ranges = parse_input(lines)
    result = 0

    for left, right in ranges:
        for i in range(left, right + 1):
            digits = [int(digit) for digit in str(i)]
            # print(left, "-", right, "->", digits)
            repeating = False
            
            for amount in range(1, len(digits) // 2 + 1):
                # print(amount)
                is_repeating = check_repeating(digits, amount, False)
                if is_repeating:
                    repeating = True
                    break
            
            if repeating:
                result += i

    return result