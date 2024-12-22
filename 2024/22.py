


def next_secret_number(number: int):
    first_step = (number ^ (number * 64)) % 16777216
    second_step = (first_step ^ (first_step // 32)) % 16777216
    third_step = (second_step ^ (second_step * 2048)) % 16777216
    return third_step

def silver_solution(lines: list[str]) -> int:
    numbers = [int(line) for line in lines]

    result = 0
    for number in numbers:
        for _ in range(2000):
            number = next_secret_number(number)
        result += number
    return result

def find_sublist_index(main_list: list[int], sublist: tuple[int, int, int, int]):
    main_len = len(main_list)
    
    for i in range(main_len - 3):
        if main_list[i] != sublist[0]:
            continue
        if main_list[i+1] != sublist[1]:
            continue
        if main_list[i+2] != sublist[2]:
            continue
        if main_list[i+3] == sublist[3]:
            return i
    
    return -1

def get_sell_price_sum(digits_dict: dict[int, list[int]], diffs_dict: dict[int, list[int]], numbers: list[int], sequence: tuple[int, int, int, int]):
    a = []
    result = 0
    for number in numbers:
        index = find_sublist_index(diffs_dict[number], sequence)
        if index == -1:
            a.append(-9999)
            # print("nop")
            continue
        real_index = index + len(sequence) - 1
        
        sell_price = digits_dict[number][real_index + 1]
        # print(sell_price)
        a.append(sell_price)
        result += sell_price

    # print("old", a)

    return result, a

def create_dicts(numbers: list[int]) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    digits_dict: dict[int, list[int]] = {}
    diffs_dict: dict[int, list[int]] = {}
    for number in numbers:
        secret_number = number
        secret_numbers: list[int] = [secret_number % 10]
        for _ in range(2000):
            secret_number = next_secret_number(secret_number)
            secret_numbers.append(secret_number % 10)
        digits_dict[number] = secret_numbers

        diffs: list[int] = []
        for first, second in zip(secret_numbers, secret_numbers[1:]):
            diffs.append(second - first)
        diffs_dict[number] = diffs

    return digits_dict, diffs_dict

def get_possible_sequences(digits_dict: dict[int, list[int]], diffs_dict: dict[int, list[int]], numbers: list[int]):
    sequence_set = set()
    sequences_of_sequences: dict[int, dict[tuple[int, int, int, int], int]] = {}
    for key, values in diffs_dict.items():
        sequences: dict[tuple[int, int, int, int], int] = {}
        # print(values)
        # print("===")
        for i in range(len(values)-3):
            sequence = (values[i], values[i+1], values[i+2], values[i+3])
            
            sequence_set.add(sequence)
            # if sequence == (4, -4, 4, 0):
            #     print("nx", i)

            sell_price = digits_dict[key][i+4]

            if sequence not in sequences:
                sequences[sequence] = sell_price

        sequences_of_sequences[key] = sequences

    #     print("====")
    #     print(sequences)

    # print("len", len(sequences))

    return sequences_of_sequences, sequence_set

def gold_solution(lines: list[str]) -> int:
    numbers = [int(line) for line in lines]

    # numbers = [7444558]

    digits_dict, diffs_dict = create_dicts(numbers)

    # print(digits_dict)
    # for x, y in diffs_dict.items():
    #     print(x, y)

    sequences, sequence_set = get_possible_sequences(digits_dict, diffs_dict, numbers)
    
    print(len(sequence_set), "leneeene")
    # for a in sequences:
    #     print("AAA")
    #     print(a)

    max_result = 0
    max_sequence = []
    i=0
    f=0

    # test_sequences =[
    #     # (-2,1,-1,3),
    #     # (-2, 1, 1, 2),
    #     # (-1, 1, -3, 3),
    #     # (5, -4, -2, 1),
    #     # (-1, -2, 5, -3),
    #     # (-9, 9, -7, 6),
    #     # (0, 5, 0, 0),
    #     (4, -4, 4, 0),
    #     (0, -4, 4, -8),
    #     (-4, 4, -8, 9),
    #     (4, -8, 9, -3),
    #     (-8, 9, -3, 3),
    #     (9, -3, 3, -2),
    # ]

    
    # for test_sequence in test_sequences:
    #     result, b = get_sell_price_sum(digits_dict, diffs_dict, numbers, test_sequence)
    #     print("old", result)

    #     a = []
    #     sum_value = 0
    #     for number in numbers:
    #         value = sequences[number].get(test_sequence, -9999)
    #         a.append(value)
    #         if value == -9999:
    #             value = 0
    #         sum_value += value

    #     # print("new", a)
    #     for c in zip(b, a):
    #         print(c, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" if c[0] != c[1] else "")

    #     print("new", sum_value)
    #     print("---")

    # return 1

    # sequence_number = number to mappings from sequence to value
    # sequence_values = mappings between sequence to value for that number
    # sequence        = one of the sequences for that number


    for sequence in sequence_set:
        sum_value = 0
        for number in numbers:
            value = sequences[number].get(sequence, 0)
            sum_value += value

        if sum_value > max_result:
            print("new max found", sum_value, sequence)
            max_result = sum_value
            max_sequence = sequence

    # for sequence_number, sequence_values in sequences.items():
    #     f+=1
    #     i=0
    #     print("===", f, len(sequences), len(sequence_values))
    #     for sequence in sequence_values.keys():
    #         i+=1
    #         sum_value = 0
    #         for number in numbers:
    #             value = sequences[number].get(sequence, 0)
    #             sum_value += value

    #         if sum_value > max_result:
    #             print("new max found", sum_value, sequence)
    #             max_result = sum_value
    #             max_sequence = sequence

            # result = get_sell_price_sum(digits_dict, diffs_dict, numbers, sequence)
            # if result > max_result:
            #     max_result = result
            #     max_sequence = sequence

    print(max_sequence)

    return max_result


# 1461 too high
# 1435 too low