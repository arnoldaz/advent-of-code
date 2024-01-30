DIGIT_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def silver_solution(lines: list[str]) -> int:
    digit_lists = [[int(digit) for digit in line if digit.isdigit()] for line in lines]
    return sum(digit_map[0] * 10 + digit_map[-1] for digit_map in digit_lists)

def gold_solution(lines: list[str]) -> int:
    final_value = 0
    for line in lines:
        digit_list = [(index, int(digit)) for index, digit in enumerate(line) if digit.isdigit()]

        for i, digit_word in enumerate(DIGIT_WORDS):
            index = 0
            while index < len(line):
                index = line.find(digit_word, index)
                if index == -1:
                    break

                digit_list.append((index, i))
                index += len(digit_word)

        digit_list.sort(key=lambda digit_tuple: digit_tuple[0])
        value = digit_list[0][1] * 10 + digit_list[-1][1]
        final_value += value

    return final_value
