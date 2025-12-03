def parse_input(lines: list[str]) -> list[list[int]]:
    number_lists: list[list[int]] = []
    for line in lines:
        numbers = [int(x) for x in line]
        number_lists.append(numbers)
        
    return number_lists

def get_total_joltage(number_lists: list[list[int]], total_digits: int) -> int:
    answer = 0
    for number_list in number_lists:
        global_indices: list[int] = []
        previous_index = -1
        for i in range(total_digits - 1, -1, -1):
            search_part = number_list[previous_index+1:len(number_list)-i]
            digit = max(search_part)
            global_found_indices = [index for index, value in enumerate(number_list) if value == digit]
            corrent_index = next(index for index in global_found_indices if index not in global_indices and index > max(global_indices)) if len(global_indices) > 0 else global_found_indices[0]
            global_indices.append(corrent_index)
            answer += digit * (10 ** i)
            previous_index = corrent_index
    
    return answer   

def silver_solution(lines: list[str]) -> int:
    number_lists = parse_input(lines)
    return get_total_joltage(number_lists, 2)

def gold_solution(lines: list[str]) -> int:
    number_lists = parse_input(lines)
    return get_total_joltage(number_lists, 12)
