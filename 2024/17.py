from dataclasses import dataclass

from utils.string import get_ints

@dataclass
class Computer():
    a: int
    b: int
    c: int
    program: list[int]

    def copy(self) -> "Computer":
        return Computer(self.a, self.b, self.c, self.program)

    def reset(self, new_a: int):
        self.a = new_a
        self.b = 0
        self.c = 0

def parse_input(lines: list[str]) -> Computer:
    a_string, b_string, c_string, _, program_string = lines
    a, b, c = (int(s.split(": ")[1]) for s in [a_string, b_string, c_string])
    program = get_ints(program_string)

    return Computer(a, b, c, program)

def get_combo(number: int, computer: Computer) -> int:
    if 0 <= number <= 3:
        return number
    if number == 4:
        return computer.a
    if number == 5:
        return computer.b
    if number == 6:
        return computer.c

    return -1

def get_program_result(computer: Computer) -> list[int]:
    result: list[int] = []
    current_index = 0
    while current_index < len(computer.program):
        instruction = computer.program[current_index]
        match instruction:
            case 0: # adv
                combo = get_combo(computer.program[current_index + 1], computer)
                computer.a //= 2 ** combo
                current_index += 2
            case 1: # bxl
                literal = computer.program[current_index + 1]
                computer.b ^= literal
                current_index += 2
            case 2: # bst
                combo = get_combo(computer.program[current_index + 1], computer)
                computer.b = combo % 8
                current_index += 2
            case 3: # jnz
                if computer.a != 0:
                    literal = computer.program[current_index + 1]
                    current_index = literal
                else:
                    current_index += 2
            case 4: # bxc
                computer.b ^= computer.c
                current_index += 2
            case 5: # out
                combo = get_combo(computer.program[current_index + 1], computer)
                result.append(combo % 8)
                current_index += 2
            case 6: # bdv
                combo = get_combo(computer.program[current_index + 1], computer)
                computer.b = computer.a // (2 ** combo)
                current_index += 2
            case 7: # cdv
                combo = get_combo(computer.program[current_index + 1], computer)
                computer.c = computer.a // (2 ** combo)
                current_index += 2

    return result

def silver_solution(lines: list[str]) -> str:
    computer = parse_input(lines)
    return ",".join(str(x) for x in get_program_result(computer))

def gold_solution(lines: list[str]) -> int:
    computer = parse_input(lines)

    answer = 0
    for number in range(len(computer.program)):
        answer *= 8
        for i in range(answer, answer + 1000):
            computer.reset(i)
            result = get_program_result(computer)
            if result == computer.program[-(number+1):]:
                answer = i
                break

    return answer
