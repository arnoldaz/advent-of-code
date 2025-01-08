from itertools import groupby

def create_disk_array(lines: list[str]) -> list[int]:
    single_line = lines[0]
    array: list[int] = []

    current_id = 0
    for i, char in enumerate(single_line):
        amount = int(char)
        is_file = i % 2 == 0
        array += [current_id] * amount if is_file else [-1] * amount
        if is_file:
            current_id += 1

    return array

def move_file_blocks(array: list[int]):
    start_index = 0
    end_index = len(array) - 1

    while True:
        if start_index >= end_index - 1:
            break

        end_element = array[end_index]
        if end_element == -1:
            end_index -= 1
            continue

        start_element = array[start_index]
        while start_element != -1:
            start_index += 1
            start_element = array[start_index]

        array[start_index], array[end_index] = array[end_index], array[start_index]
        end_index -= 1

def move_file_block_groups(array: list[int]):
    blocks: list[tuple[int, int, int]] = []
    i = 0
    for key, group in groupby(array):
        length = sum(1 for _ in group)
        blocks.append((key, i, i + length - 1))
        i += length

    for back_index in range(len(blocks) - 1, -1, -1):
        back_element, back_start_index, back_end_index = blocks[back_index]
        back_length = back_end_index - back_start_index + 1
        if back_element == -1:
            continue

        for front_index in range(back_index):
            front_element, front_start_index, front_end_index = blocks[front_index]
            front_length = front_end_index - front_start_index + 1
            if front_element != -1:
                continue

            if back_length > front_length:
                continue

            for i in range(back_length):
                array[i + back_start_index], array[i + front_start_index] = array[i + front_start_index], array[i + back_start_index]

            blocks[front_index] = (front_element, front_start_index + back_length, front_end_index)
            break

def calculate_checksum(array: list[int]) -> int:
    return sum(i * element for i, element in enumerate(array) if element != -1)

def silver_solution(lines: list[str]) -> int:
    array = create_disk_array(lines)
    move_file_blocks(array)

    return calculate_checksum(array)

def gold_solution(lines: list[str]) -> int:
    array = create_disk_array(lines)
    move_file_block_groups(array)

    return calculate_checksum(array)
