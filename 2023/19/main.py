
from typing import NamedTuple, Optional
from itertools import chain

with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

class Condition(NamedTuple):
    variable: str
    sign: str
    number: int
    destination: str

class Data(NamedTuple):
    x: int
    m: int
    a: int
    s: int

commands: dict[str, list[Condition]] = {}
data = []

read_commands = True
for line in lines:
    if line == "":
        read_commands = False
        continue

    if read_commands:
        name, command_data = line.split("{")
        conditions = command_data.strip("}").split(",")
        final_conditions: list[Condition] = []
        for condition in conditions:
            if ":" in condition:
                comparison, destination = condition.split(":")
                final_condition = Condition(comparison[0], comparison[1], int(comparison[2:]), destination)
            else:
                final_condition = Condition("", "", -1, condition)
            final_conditions.append(final_condition)
        commands[name] = final_conditions
    else:
        x, m, a, s = line.strip("{").strip("}").split(",")
        data.append(Data(int(x.removeprefix("x=")), int(m.removeprefix("m=")), int(a.removeprefix("a=")), int(s.removeprefix("s="))))

def check_accepted(data: Data, commands: dict[str, list[Condition]]) -> bool:
    current_conditions = commands["in"]
    
    final_result = False
    found = False
    while not found:
        for condition in current_conditions:
            condition_passed = False
            match condition.variable:
                case "x":
                    match condition.sign:
                        case "<":
                            condition_passed = data.x < condition.number
                        case ">":
                            condition_passed = data.x > condition.number
                case "m":
                    match condition.sign:
                        case "<":
                            condition_passed = data.m < condition.number
                        case ">":
                            condition_passed = data.m > condition.number
                case "a":
                    match condition.sign:
                        case "<":
                            condition_passed = data.a < condition.number
                        case ">":
                            condition_passed = data.a > condition.number
                case "s":
                    match condition.sign:
                        case "<":
                            condition_passed = data.s < condition.number
                        case ">":
                            condition_passed = data.s > condition.number
                case "":
                    condition_passed = True
            
            if condition_passed:
                if condition.destination == "A":
                    final_result = True
                    found = True
                    break
                elif condition.destination == "R":
                    final_result = False
                    found = True
                    break
                else:
                    current_conditions = commands[condition.destination]
                    break

    
    return final_result
        
def calculate_accepted_sum(data: list[Data], commands: dict[str, list[Condition]]) -> int:
    result = 0
    
    for entry in data:
        if check_accepted(entry, commands):
            result += entry.x + entry.m + entry.a + entry.s
    
    return result


print(f"{calculate_accepted_sum(data, commands)=}")

lists: list[list[Condition]] = []
def populare_paths_recursive(root: Condition, path: list[Condition], pathLen, commands: dict[str, list[Condition]]):
    if root is None:
        return

    if(len(path) > pathLen): 
        path[pathLen] = root
    else:
        path.append(root)

    pathLen = pathLen + 1

    if root.destination == "A":
        lists.append(path[:pathLen])
    elif root.destination == "R":
        return
    else:
        for new_root in commands[root.destination]:
            populare_paths_recursive(new_root, path, pathLen, commands)

current_conditions = commands["in"]
for condition in current_conditions:
    path = []
    populare_paths_recursive(condition, path, 0, commands)

