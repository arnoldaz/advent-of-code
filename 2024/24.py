from enum import Enum
from typing import NamedTuple

class Operation(Enum):
    AND = 1
    OR = 2
    XOR = 3

class Instruction(NamedTuple):
    operation: Operation
    left: str
    right: str
    destination: str

def parse_input(lines: list[str]):
    instructions: list[Instruction] = []
    wire_values: dict[str, int] = {}

    is_initial_data = True
    for line in lines:
        if not line:
            is_initial_data = False
            continue

        if is_initial_data:
            wire, value = line.split(": ")
            wire_values[wire] = int(value)
        else:
            data, destination = line.split(" -> ")
            if "AND" in data:
                operation = Operation.AND
                left, right = data.split(" AND ")
            elif "XOR" in data:
                operation = Operation.XOR
                left, right = data.split(" XOR ")
            elif "OR" in data:
                operation = Operation.OR
                left, right = data.split(" OR ")

            instructions.append(Instruction(operation, left, right, destination))

    return instructions, wire_values

def get_instructions_result(instructions: list[Instruction], initial_wire_values: dict[str, int]):
    wire_values = initial_wire_values.copy()
    calculated_values = { *wire_values.keys() }
    final_count = len(instructions) + len(calculated_values)

    while len(calculated_values) < final_count:
        for instruction in instructions:
            if instruction.left in calculated_values and instruction.right in calculated_values:
                match instruction.operation:
                    case Operation.AND:
                        result = wire_values[instruction.left] & wire_values[instruction.right]
                    case Operation.OR:
                        result = wire_values[instruction.left] | wire_values[instruction.right]
                    case Operation.XOR:
                        result = wire_values[instruction.left] ^ wire_values[instruction.right]
                wire_values[instruction.destination] = result
                calculated_values.add(instruction.destination)

    final_result = 0
    for key, value in wire_values.items():
        if key.startswith("z"):
            number = int(key.removeprefix("z"))
            final_result += (2 ** number) * value

    return final_result

def generate_neato_dot_file(instructions: list[Instruction]):
    # Use command "neato -Tpng -o temp/input-graph.png temp/input.dot" to generate image afterwards

    connection_pairs: list[tuple[str, str]] = []
    and_nodes: list[str] = []
    or_nodes: list[str] = []
    xor_nodes: list[str] = []

    for instruction in instructions:
        connection_pairs.append((instruction.left, instruction.destination))
        connection_pairs.append((instruction.right, instruction.destination))

        match instruction.operation:
            case Operation.AND:
                and_nodes.append(instruction.destination)
            case Operation.OR:
                or_nodes.append(instruction.destination)
            case Operation.XOR:
                xor_nodes.append(instruction.destination)

    with open("temp/input.dot", "w", encoding="utf-8") as file:
        file.write("digraph conections {\n")
        file.write("    layout=dot;\n")

        file.write("    subgraph x {\n")
        file.write("        node [style=filled,color=lightgrey];\n")
        string = "        "
        for i in range(45):
            string += f"x{str(i).zfill(2)} -> "
        string = f"{string.rstrip().removesuffix(" ->")};\n"
        file.write(string)
        file.write("    }\n")

        file.write("    subgraph y {\n")
        file.write("        node [style=filled,color=darkgrey];\n")
        string = "        "
        for i in range(45):
            string += f"y{str(i).zfill(2)} -> "
        string = f"{string.rstrip().removesuffix(" ->")};\n"
        file.write(string)
        file.write("    }\n")

        file.write("    subgraph and {\n")
        file.write("        node [style=filled,color=springgreen];\n")
        file.write(f"        {"; ".join(and_nodes)};\n")
        file.write("    }\n")

        file.write("    subgraph or {\n")
        file.write("        node [style=filled,color=lightskyblue];\n")
        file.write(f"        {"; ".join(or_nodes)};\n")
        file.write("    }\n")

        file.write("    subgraph xor {\n")
        file.write("        node [style=filled,color=peachpuff];\n")
        file.write(f"        {"; ".join(xor_nodes)};\n")
        file.write("    }\n")

        file.write("    subgraph z {\n")
        string = "        "
        for i in range(46):
            string += f"z{str(i).zfill(2)} -> "
        string = f"{string.rstrip().removesuffix(" ->")};\n"
        file.write(string)
        file.write("    }\n")

        for key1, key2 in connection_pairs:
            file.write(f"    {key1} -> {key2}\n")
        file.write("}\n")

def silver_solution(lines: list[str]) -> int:
    instructions, wire_values = parse_input(lines)
    return get_instructions_result(instructions, wire_values)

def gold_solution(lines: list[str]) -> str:
    instructions, wire_values = parse_input(lines)

    generate_neato_dot_file(instructions)

    # x_result, y_result = 0, 0
    # for key, value in wire_values.items():
    #     if key.startswith("x"):
    #         number = int(key.removeprefix("x"))
    #         x_result += (2 ** number) * value
    #     elif key.startswith("y"):
    #         number = int(key.removeprefix("y"))
    #         y_result += (2 ** number) * value

    # expected_result = x_result + y_result

    # print(x_result, y_result, "=", expected_result)
    # print("", bin(x_result))
    # print("", bin(y_result))
    # print("=")
    # print(bin(expected_result), "good")
    # print(bin(get_instructions_result(instructions, wire_values)), "current")

    # Found visually from generated graph
    swaps = ["z06", "fkp", "z31", "mfm", "z11", "ngr", "bpt", "krj"]

    return ",".join(sorted(swaps))
