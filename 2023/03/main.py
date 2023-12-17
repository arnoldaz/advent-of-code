import re

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

def is_valid_symbol(char: str) -> bool:
    return char != "." and not char.isdigit()

def is_gear_symbol(char: str) -> bool:
    return char == "*"

def calculate_part_sum(lines: list[str]) -> int:
    final_sum = 0

    for y, line in enumerate(lines):
        numbers = [(int(number.group(0)), number.start(0), number.end(0)-1) for number in re.finditer(r'\b\d+\b', line)]
        for number in numbers:
            start_index = number[1] - 1
            end_index = number[2] + 1

            is_number_valid = False

            # top line
            if y != 0:
                test_line = lines[y-1]
                for i in range(max(start_index, 0), min(end_index + 1, len(line))):
                    if is_valid_symbol(test_line[i]):
                        is_number_valid = True
                        break

            # bot line
            if y != len(lines) - 1 and not is_number_valid:
                test_line = lines[y+1]
                for i in range(max(start_index, 0), min(end_index + 1, len(line))):
                    if is_valid_symbol(test_line[i]):
                        is_number_valid = True
                        break
        
            # left side
            if start_index >= 0 and is_valid_symbol(line[start_index]) and not is_number_valid:
                is_number_valid = True

            # right side
            if end_index <= len(line) - 1 and is_valid_symbol(line[end_index]) and not is_number_valid:
                is_number_valid = True

            if is_number_valid:
                final_sum += number[0]

    return final_sum

def calculate_gear_ratio(lines: list[str]) -> int:
    final_sum = 0

    gear_map: dict[tuple[int, int], list[int]] = {}

    for y, line in enumerate(lines):
        numbers = [(int(number.group(0)), number.start(0), number.end(0)-1) for number in re.finditer(r'\b\d+\b', line)]
        for number in numbers:
            start_index = number[1] - 1
            end_index = number[2] + 1

            is_number_valid = False
            gear_location = (-1, -1)

            # top line
            if y != 0:
                test_line = lines[y-1]
                for i in range(max(start_index, 0), min(end_index + 1, len(line))):
                    if is_gear_symbol(test_line[i]):
                        is_number_valid = True
                        gear_location = (y-1, i)
                        break

            # bot line
            if y != len(lines) - 1 and not is_number_valid:
                test_line = lines[y+1]
                for i in range(max(start_index, 0), min(end_index + 1, len(line))):
                    if is_gear_symbol(test_line[i]):
                        is_number_valid = True
                        gear_location = (y+1, i)
                        break
        
            # left side
            if start_index >= 0 and is_gear_symbol(line[start_index]) and not is_number_valid:
                is_number_valid = True
                gear_location = (y, start_index)

            # right side
            if end_index <= len(line) - 1 and is_gear_symbol(line[end_index]) and not is_number_valid:
                is_number_valid = True
                gear_location = (y, end_index)

            if is_number_valid:
                if gear_location in gear_map:
                    gear_map[gear_location].append(number[0])
                else:
                    gear_map[gear_location] = [number[0]]

    for key in gear_map:
        values = gear_map[key]
        if len(values) == 2:
            final_sum += values[0] * values[1]

    return final_sum

print(f"{calculate_part_sum(lines)=}")
print(f"{calculate_gear_ratio(lines)=}")



