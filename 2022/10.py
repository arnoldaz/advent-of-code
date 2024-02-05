from typing import NamedTuple

class Instruction(NamedTuple):
    operation: str
    value: int

def parse_input(lines: list[str]) -> list[Instruction]:
    instructions = []

    for line in lines:
        if " " in line:
            operation, value = line.split()
        else:
            operation, value = line, None
        instructions.append(Instruction(operation, int(value) if value else 0))

    return instructions

def get_signal_strength_sum(instructions: list[Instruction]) -> int:
    critical_cycles = (20, 60, 100, 140, 180, 220)
    x_register = 1
    cycle = 1

    strength = 0

    for instruction in instructions:
        if cycle in critical_cycles:
            strength += cycle * x_register

        match instruction.operation:
            case "noop":
                cycle += 1
            case "addx":
                cycle += 1
                if cycle in critical_cycles:
                    strength += cycle * x_register
                cycle += 1
                x_register += instruction.value

    return strength

def print_stuff(x_register: int, cycle: int) -> bool:

    if x_register <= cycle <= x_register + 2:
        print("\u2593", end="")
    else:
        print(" ", end="")

    if cycle % 40 == 0:
        print()
        return True

    return False


def get_signal_strength_sum_uhhh(instructions: list[Instruction]) -> int:
    print()

    x_register = 1
    cycle = 1

    for instruction in instructions:
        if print_stuff(x_register, cycle):
            cycle = 0

        match instruction.operation:
            case "noop":
                cycle += 1
            case "addx":
                cycle += 1
                if print_stuff(x_register, cycle):
                    cycle = 0
                cycle += 1
                x_register += instruction.value

    print()
    print()
    return 0


def silver_solution(lines: list[str]) -> int:
    instructions = parse_input(lines)
    return get_signal_strength_sum(instructions)

def gold_solution(lines: list[str]) -> int:
    instructions = parse_input(lines)
    return get_signal_strength_sum_uhhh(instructions)
