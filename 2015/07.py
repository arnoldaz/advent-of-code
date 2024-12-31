from enum import Enum
from typing import NamedTuple, Optional

class Operation(Enum):
    NONE = 0
    AND = 1
    OR = 2
    LSHIFT = 3
    RSHIFT = 4
    NOT = 5

class Instruction(NamedTuple):
    operation: Operation
    left: str
    right: str
    destination: str

def parse_input(lines: list[str]):
    instructions: list[Instruction] = []
    for line in lines:
        data, destination = line.split(" -> ")
        if "AND" in data:
            operation = Operation.AND
            left, right = data.split(" AND ")
        elif "OR" in data:
            operation = Operation.OR
            left, right = data.split(" OR ")
        elif "LSHIFT" in data:
            operation = Operation.LSHIFT
            left, right = data.split(" LSHIFT ")
        elif "RSHIFT" in data:
            operation = Operation.RSHIFT
            left, right = data.split(" RSHIFT ")
        elif "NOT" in data:
            operation = Operation.NOT
            left, right = data.removeprefix("NOT "), ""
        else:
            operation = Operation.NONE
            left, right = data, ""

        instructions.append(Instruction(operation, left, right, destination))

    return instructions

def get_operand_values(instruction: Instruction, current_signals: dict[str, int]) -> tuple[Optional[int], Optional[int]]:
    left, right = None, None

    if instruction.left.isnumeric():
        left = int(instruction.left)
    elif instruction.left in current_signals:
        left = current_signals[instruction.left]

    if instruction.right.isnumeric():
        right = int(instruction.right)
    elif instruction.right in current_signals:
        right = current_signals[instruction.right]

    return left, right

def calculate_signals(instructions: list[Instruction], signals: dict[str, int]):
    while len(signals) < len(instructions):
        for instruction in instructions:
            if instruction.destination in signals:
                continue

            match instruction.operation:
                case Operation.NONE:
                    left, _ = get_operand_values(instruction, signals)
                    if left is not None:
                        signals[instruction.destination] = left
                case Operation.AND:
                    left, right = get_operand_values(instruction, signals)
                    if left is not None and right is not None:
                        signals[instruction.destination] = left & right
                case Operation.OR:
                    left, right = get_operand_values(instruction, signals)
                    if left is not None and right is not None:
                        signals[instruction.destination] = left | right
                case Operation.LSHIFT:
                    left, right = get_operand_values(instruction, signals)
                    if left is not None and right is not None:
                        signals[instruction.destination] = left << right
                case Operation.RSHIFT:
                    left, right = get_operand_values(instruction, signals)
                    if left is not None and right is not None:
                        signals[instruction.destination] = left >> right
                case Operation.NOT:
                    left, _ = get_operand_values(instruction, signals)
                    if left is not None:
                        signals[instruction.destination] = ~left

def silver_solution(lines: list[str]) -> int:
    instructions = parse_input(lines)

    signals: dict[str, int] = {}
    calculate_signals(instructions, signals)

    return signals["a"]

def gold_solution(lines: list[str]) -> int:
    instructions = parse_input(lines)

    signals: dict[str, int] = {}
    calculate_signals(instructions, signals)

    signals = { "b": signals["a"] }
    calculate_signals(instructions, signals)

    return signals["a"]
