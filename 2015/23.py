from enum import Enum
from typing import NamedTuple

class Operation(Enum):
    HALF = 1
    TRIPLE = 2
    INCREMENT = 3
    JUMP = 4
    JUMP_IF_EVEN = 5
    JUMP_IF_ODD = 6

class Instruction(NamedTuple):
    operation: Operation
    register: str
    offset: int

def parse_input(lines: list[str]):
    instructions: list[Instruction] = []
    for line in lines:
        operation_string, others = line.split(maxsplit=1)
        match operation_string:
            case "hlf":
                operation = Operation.HALF
                register, offset = others, 0
            case "tpl":
                operation = Operation.TRIPLE
                register, offset = others, 0
            case "inc":
                operation = Operation.INCREMENT
                register, offset = others, 0
            case "jmp":
                operation = Operation.JUMP
                register, offset = "", int(others)
            case "jie":
                operation = Operation.JUMP_IF_EVEN
                register, offset_string = others.split(", ")
                offset = int(offset_string)
            case "jio":
                operation = Operation.JUMP_IF_ODD
                register, offset_string = others.split(", ")
                offset = int(offset_string)

        instructions.append(Instruction(operation, register, offset))

    return instructions

def run_instructions(registers: dict[str, int], instructions: list[Instruction]):
    i = 0
    while i < len(instructions):
        instruction = instructions[i]

        match instruction.operation:
            case Operation.HALF:
                registers[instruction.register] //= 2
            case Operation.TRIPLE:
                registers[instruction.register] *= 3
            case Operation.INCREMENT:
                registers[instruction.register] += 1
            case Operation.JUMP:
                i += instruction.offset
                continue
            case Operation.JUMP_IF_EVEN:
                if registers[instruction.register] % 2 == 0:
                    i += instruction.offset
                    continue
            case Operation.JUMP_IF_ODD:
                if registers[instruction.register] == 1:
                    i += instruction.offset
                    continue

        i += 1

def silver_solution(lines: list[str]) -> int:
    instructions = parse_input(lines)
    registers = {"a": 0, "b": 0}

    run_instructions(registers, instructions)
    return registers["b"]

def gold_solution(lines: list[str]) -> int:
    instructions = parse_input(lines)
    registers = {"a": 1, "b": 0}

    run_instructions(registers, instructions)
    return registers["b"]
