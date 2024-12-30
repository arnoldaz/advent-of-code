def increment_password(password: str) -> str:
    new_password = list(password)
    for i in range(len(password) - 1, -1, -1):
        if new_password[i] != "z":
            new_password[i] = chr(ord(new_password[i]) + 1)
            return "".join(new_password)

        new_password[i] = "a"

    return "a" + "".join(new_password)

def has_two_non_overlapping_pairs(password: str) -> bool:
    pair_symbols = set()
    i = 0
    while i < len(password) - 1:
        if password[i] == password[i+1] and password[i] not in pair_symbols:
            pair_symbols.add(password[i])
            i += 2
        else:
            i += 1

    return len(pair_symbols) >= 2

def has_increasing_three_letter_straight(password: str) -> bool:
    for i in range(len(password) - 2):
        if ord(password[i]) + 1 == ord(password[i+1]) and ord(password[i+1]) + 1 == ord(password[i+2]):
            return True

    return False

def check_password(password: str) -> bool:
    if "i" in password or "o" in password or "l" in password:
        return False

    if not has_increasing_three_letter_straight(password):
        return False

    if not has_two_non_overlapping_pairs(password):
        return False

    return True

def silver_solution(lines: list[str]) -> str:
    password = lines[0]

    while True:
        password = increment_password(password)
        if check_password(password):
            break

    return password

def gold_solution(lines: list[str]) -> str:
    password = lines[0]

    correct_passwords_count = 0
    while True:
        password = increment_password(password)
        if check_password(password):
            correct_passwords_count += 1
            if correct_passwords_count == 2:
                break

    return password
