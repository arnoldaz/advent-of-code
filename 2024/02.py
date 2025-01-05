def parse_input(lines: list[str]) -> list[list[int]]:
    return [[int(x) for x in line.split()] for line in lines]

def check_safe(number_list: list[int]) -> bool:
    ascending = sorted(number_list) == number_list
    descending = sorted(number_list, reverse=True) == number_list

    if not ascending and not descending:
        return False

    for i in range(len(number_list) - 1):
        diff = abs(number_list[i] - number_list[i+1])
        if diff < 1 or diff > 3:
            return False

    return True

def silver_solution(lines: list[str]) -> int:
    number_lists = parse_input(lines)
    return sum(1 for number_list in number_lists if check_safe(number_list))

def gold_solution(lines: list[str]) -> int:
    number_lists = parse_input(lines)

    counter = 0
    for number_list in number_lists:
        if check_safe(number_list):
            counter += 1
        else:
            for i in range(len(number_list)):
                new_list = number_list[:i] + number_list[i+1:]
                if check_safe(new_list):
                    counter += 1
                    break

    return counter
