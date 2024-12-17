from dataclasses import dataclass

@dataclass
class Computer():
    a: int
    b: int
    c: int
    program: list[int]
    
def parse_input(lines: list[str]) -> Computer:
    a_string, b_string, c_string, _, program_string = lines
    a = int(a_string.split(":")[1].strip())
    b = int(b_string.split(":")[1].strip())
    c = int(c_string.split(":")[1].strip())
    program = [int(x) for x in program_string.split(":")[1].strip().split(",")]

    return Computer(a, b, c, program)

def get_combo(number: int, computer: Computer) -> int:
    if number >= 0 and number <= 3:
        return number
    
    if number == 4:
        return computer.a
    
    if number == 5:
        return computer.b
    
    if number == 6:
        return computer.c
    
    return -1

def silver_solution(lines: list[str]) -> str:
    computer = parse_input(lines)

    result = []

    computer.a = 190384609508367

    current_index = 0
    while current_index < len(computer.program):
        # print(current_index, len(computer.program))
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
    
    print(computer)
    return ",".join(str(x) for x in result)

def get_result(computer: Computer) -> list[int]:
    result = []
    current_index = 0
    while current_index < len(computer.program):
        # print(current_index, computer)
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

def gold_solution(lines: list[str]) -> int:
    computer = parse_input(lines)

    # [7, 1, 4, 7, 3, 0, 1, 6, 5, 6, 4, 3, 0, 0, 6, 5]

    # for 5 -> 0-7
    # for 6 -> 40-47 cuz 40/8 = 5, 47/8=5

    ats: list[int] = []
    ats_i = -1
    
    for ix, command in enumerate(reversed(computer.program)):
        print(ats_i, ats, "start")
        if ats_i == -1:
            test = 0
        else:
            test = ats[ats_i] * 8
        
        print("range", test, test + 8)

        for i in range(test, test + 400):
            copy_computer = Computer(i, 0, 0, computer.program)
            result = get_result(copy_computer)
            print("Res", -(ix+1), result, computer.program[-(ix+1):])
            if result == computer.program[-(ix+1):]:
                print("wohoo")
                ats.append(i)
                break
        else:
            print("wtf")
        
        ats_i += 1
        print(ats_i, ats)

    # ats.reverse()

    result = 0
    for i, x in enumerate(ats):
        print(i, 8 ** i, x)
        result += 8 ** i + x

    print(ats)

    for i in range(8):
        print(i, i ^ 2)

    return result

# 2 4 -> b = a % 8
# 1 2 -> b = b XOR 2
# 7 5 -> c = a / 2^b
# 4 3 -> b = b XOR c
# 0 3 -> a = a / 8
# 1 7 -> b = b XOR 7
# 5 5 -> print b % 8
# 3 0 -> goto 0
