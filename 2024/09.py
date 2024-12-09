# pylint: disable=unused-argument

def create_disk_array(line: str) -> list[int]:
    array: list[int] = []

    current_id = 0
    is_free_space = False
    for char in line:
        if not is_free_space:
            array += [current_id] * int(char)
            current_id += 1
            is_free_space = True
        else:
            array += [-1] * int(char)
            is_free_space = False

    return array

def move_disk_blocks(array: list[int]):
    for i in range(len(array) - 1, -1, -1):
        element = array[i]
        if element == -1:
            continue

        for j in range(i):
            possible_element = array[j]
            if possible_element == -1:
                array[i], array[j] = array[j], array[i]
                break
        else:
            break

        if i % 5000 == 0:
            print(i)

def move_disk_blocks_gold(array: list[int]):
    block_start_index = -1
    block_end_index = len(array) - 1
    block_started = True
    previous_element = array[block_end_index]

    blocks: list[tuple[int, int, int]] = []

    # (9, 40, 41)
    # (8, 36, 39)
    # (7, 32, 34)
    # (6, 27, 30)
    # (5, 22, 25)
    # (4, 19, 20)
    # (3, 15, 17)
    # (2, 11, 11)
    # (1, 5, 7)
    # (0, 0, 1)

    # (9, 40, 41)
    # (8, 36, 39)
    # (-1, 35, 35)
    # (7, 32, 34)
    # (-1, 31, 31)
    # (6, 27, 30)
    # (-1, 26, 26)
    # (5, 22, 25)
    # (-1, 21, 21)
    # (4, 19, 20)
    # (-1, 18, 18)
    # (3, 15, 17)
    # (-1, 12, 14)
    # (2, 11, 11)
    # (-1, 8, 10)
    # (1, 5, 7)
    # (-1, 2, 4)
    # (0, 0, 1)

    for i in range(len(array) - 1, -1, -1):
        element = array[i]

        # print(f"{element=} {i=}")

        if block_started:
            if element != previous_element:
                block_start_index = i + 1
                block_started = False
                blocks.append((previous_element, block_start_index, block_end_index))
                # if element != -1:
                block_end_index = i
                block_started = True
            else:
                if i == 0:
                    block_start_index = i
                    block_started = False
                    blocks.append((element, block_start_index, block_end_index))
        else:
            if element != -1:
                block_end_index = i
                block_started = True
            else:
                continue

        previous_element = element

    # print("blocks")
    # for block in blocks:
    #     print(block)

    print_array(array)
    print("START")

    blocks.reverse()

    for i in range(len(blocks) - 1, -1, -1):
        element, start, end = blocks[i]
        length = max(end - start + 1, 0)
        # print(f"{element=} {start=} {end=} {length=}")
        if element != -1:
            for j in range(i):
                possible_element, possible_start, possible_end = blocks[j]
                possible_length = max(possible_end - possible_start + 1, 0)
                if possible_element == -1:
                    if length <= possible_length:
                        for k in range(length):
                            array[k + start], array[k + possible_start] = array[k + possible_start], array[k + start]

                        blocks[j] = (possible_element, possible_start + length, possible_end)
                        # print(blocks[j])
                        break

        # print_array(array)
    print_array(array)


# 8532024062389
# 6408966547049

def print_array(array: list[int]):
    for x in array:
        if x == -1:
            print(" .", end="")
        else:
            print(f" {x}", end="")
    print()

def calculate_checksum(array: list[int]) -> int:
    final_sum = 0
    for i, element in enumerate(array):
        if element != -1:
            final_sum += i * element

    return final_sum

def silver_solution(lines: list[str]) -> int:
    line = lines[0]

    print("creating")
    array = create_disk_array(line)
    # print_array(array)
    print("created")

    print("moving")
    move_disk_blocks(array)
    print("moved")

    # print_array(array)

    print("checksum")
    return calculate_checksum(array)

def gold_solution(lines: list[str]) -> int:
    line = lines[0]

    print("creating")
    array = create_disk_array(line)
    print_array(array)
    print("created")

    print("moving")
    move_disk_blocks_gold(array)
    print("moved")

    # print_array(array)

    print("checksum")
    return calculate_checksum(array)

