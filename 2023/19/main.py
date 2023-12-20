
from typing import NamedTuple, Optional
from itertools import chain

with open("input-test.txt") as file:
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


# def recursive_combinations(condition: Condition, commands: dict[str, list[Condition]], result: Optional[list[list[Condition]]] = None):
#     print(f"{condition=}")

#     if condition.destination == "A":
#         return [condition]
#     if condition.destination == "R":
#         return [condition]

#     further_conditions = commands[condition.destination]

#     stuff = []
#     for further_condition in further_conditions: # [A, R, A]
#         x = recursive_combinations(further_condition, commands, result)
#         if x != None:
#             stuff.append(x + [condition])

#     return stuff


def calculate_all_accepted_combinationss(data: list[Data], commands: dict[str, list[Condition]]) -> int:
    result = 0
    current_conditions = commands["in"]

    for condition in current_conditions:
        condition.destination

    return result


print(f"{calculate_accepted_sum(data, commands)=}")

# px{a<2006:qkq,m>2090:A,rfg}
# qkq                   A                rfg
# A   crn                        gd     R         A
#    A    R                   R     R


lists: list[list[Condition]] = []
def printPathsRec(root: Condition, path: list[Condition], pathLen, commands: dict[str, list[Condition]]):
    if root is None:
        return

    if(len(path) > pathLen): 
        path[pathLen] = root
    else:
        path.append(root)

    pathLen = pathLen + 1

    if root.destination == "A":
        lists.append(path[:pathLen])
        # printArray(path, pathLen)
    elif root.destination == "R":
        return
    else:
        for new_root in commands[root.destination]:
            printPathsRec(new_root, path, pathLen, commands)

def printArray(ints, len):
    for i in ints[0 : len]:
        print(i," ",end="")
    print()



current_conditions = commands["in"]

for condition in current_conditions:
    path = []
    printPathsRec(condition, path, 0, commands)


print(":=====")
for a in lists:
    print(a)
print(":=====")

def find_overlap(range1: tuple[int, int], range2: tuple[int, int]) -> Optional[tuple[int, int]]:
    start = max(range1[0], range2[0])
    end = min(range1[1], range2[1])

    if start <= end:
        return (start, end)
    else:
        return None

def remove_overlapping_range(range_to_cut: tuple[int, int], source_range: tuple[int, int]) -> list[tuple[int, int]]:
    start1, end1 = range_to_cut
    start2, end2 = source_range

    if end1 >= start2 and start1 <= end2:
        overlapping_start = max(start1, start2)
        overlapping_end = min(end1, end2)

        if overlapping_end == end2:
            remaining_ranges = []
        else:
            remaining_ranges = [(overlapping_end + 1, end2)]

        if overlapping_start > start2:
            remaining_ranges.insert(0, (start2, overlapping_start - 1))

        return remaining_ranges
    else:
        return [source_range]

x_mins: list[int] = []
x_maxs: list[int] = []
m_mins: list[int] = []
m_maxs: list[int] = []
a_mins: list[int] = []
a_maxs: list[int] = []
s_mins: list[int] = []
s_maxs: list[int] = []

full_variations = 0
for condition_list in lists:
    print("\n\n")

    result = 0

    x_min = 1
    x_max = 4000
    m_min = 1
    m_max = 4000
    a_min = 1
    a_max = 4000
    s_min = 1
    s_max = 4000

    for condition in condition_list:
        match condition.variable:
            case "x":
                match condition.sign:
                    case "<":
                        x_max = min(x_max, condition.number - 1)
                    case ">":
                        x_min = max(x_min, condition.number + 1)
            case "m":
                match condition.sign:
                    case "<":
                        m_max = min(m_max, condition.number - 1)
                    case ">":
                        m_min = max(m_min, condition.number + 1)
            case "a":
                match condition.sign:
                    case "<":
                        a_max = min(a_max, condition.number - 1)
                    case ">":
                        a_min = max(a_min, condition.number + 1)
            case "s":
                match condition.sign:
                    case "<":
                        s_max = min(s_max, condition.number - 1)
                    case ">":
                        s_min = max(s_min, condition.number + 1)

    print(f"{condition_list=}")
    print(f"{x_min=} {x_max=}")
    print(f"{m_min=} {m_max=}")
    print(f"{a_min=} {a_max=}")
    print(f"{s_min=} {s_max=}")

    x_range: list[tuple[int, int]] = []
    m_range: list[tuple[int, int]] = []
    a_range: list[tuple[int, int]] = []
    s_range: list[tuple[int, int]] = []

    print("=a=a=a=a==a=a=")
    for aaa in range(len(x_mins)):
        print(f"{x_mins[aaa]=} {x_maxs[aaa]=}")
        print(f"{m_mins[aaa]=} {m_maxs[aaa]=}")
        print(f"{a_mins[aaa]=} {a_maxs[aaa]=}")
        print(f"{s_mins[aaa]=} {s_maxs[aaa]=}")
    print("=a=a=a=a==a=a=")

    test = False

    for i in range(len(x_mins)):

        x_overlap = find_overlap((x_min, x_max), (x_mins[i], x_maxs[i]))
        m_overlap = find_overlap((m_min, m_max), (m_mins[i], m_maxs[i]))
        a_overlap = find_overlap((a_min, a_max), (a_mins[i], a_maxs[i]))
        s_overlap = find_overlap((s_min, s_max), (s_mins[i], s_maxs[i]))

        print("-x-x-x-x-")
        print(f"{x_overlap=}, {(x_min, x_max)=}, {(x_mins[i], x_maxs[i])=}")
        print(f"{m_overlap=}, {(m_min, m_max)=}, {(m_mins[i], m_maxs[i])=}")
        print(f"{a_overlap=}, {(a_min, a_max)=}, {(a_mins[i], a_maxs[i])=}")
        print(f"{s_overlap=}, {(s_min, s_max)=}, {(s_mins[i], s_maxs[i])=}")
        print("-x-x-x-x-")


        if x_overlap != None and m_overlap != None and a_overlap != None and s_overlap != None:
            test = True
            print("-----")
            print(x_overlap)
            print(m_overlap)
            print(a_overlap)
            print(s_overlap)
            print("-----")
            x_range = remove_overlapping_range(x_overlap, (x_min, x_max)) if len(x_range) == 0 else list(chain.from_iterable([remove_overlapping_range(x_overlap, f) for f in x_range]))
            m_range = remove_overlapping_range(m_overlap, (m_min, m_max)) if len(m_range) == 0 else list(chain.from_iterable([remove_overlapping_range(m_overlap, f) for f in m_range]))
            a_range = remove_overlapping_range(a_overlap, (a_min, a_max)) if len(a_range) == 0 else list(chain.from_iterable([remove_overlapping_range(a_overlap, f) for f in a_range]))
            s_range = remove_overlapping_range(s_overlap, (s_min, s_max)) if len(s_range) == 0 else list(chain.from_iterable([remove_overlapping_range(s_overlap, f) for f in s_range]))
            print("----++-")
            print(x_range)
            print(m_range)
            print(a_range)
            print(s_range)
            print("----++-")


    x_mins.append(x_min)
    x_maxs.append(x_max)
    m_mins.append(m_min)
    m_maxs.append(m_max)
    a_mins.append(a_min)
    a_maxs.append(a_max)
    s_mins.append(s_min)
    s_maxs.append(s_max)

    # print("-------------------===================")
    # print(x_range)
    # print(m_range)
    # print(a_range)
    # print(s_range)
    # print("-------------------===================")

    if not test:
        x = x_max - x_min + 1
        m = m_max - m_min + 1
        a = a_max - a_min + 1
        s = s_max - s_min + 1

        variations = x * m * a * s
        print(f"{variations=}")
        full_variations += variations
        print("=================================")
    else:
        range_count = 0
        range_count += 1 if len(x_range) > 0 else 0    
        range_count += 1 if len(m_range) > 0 else 0    
        range_count += 1 if len(a_range) > 0 else 0    
        range_count += 1 if len(s_range) > 0 else 0    

        variations = 0

        range_current_counter = 0
        if len(x_range) > 0:
            range_current_counter += 1

            temp_variations = 1
            temp = 0
            for p in x_range:
                temp += p[1] - p[0] + 1
            temp_variations *= temp

            temp_variations *= m_max - m_min + 1
            temp_variations *= a_max - a_min + 1
            temp_variations *= s_max - s_min + 1

            variations += temp_variations

        if len(m_range) > 0:
            range_current_counter += 1

            temp_variations = 1
            temp = 0
            for p in m_range:
                temp += p[1] - p[0] + 1
            temp_variations *= temp

            if len(x_range) > 0:
                og = [(x_min, x_max)]
                for x in x_range:
                    temp = []
                    for o in og:
                        temp += remove_overlapping_range(x, o)
                    og = temp

                temp = 0
                for o in og:
                    if len(o) > 0:
                        temp += o[1] - o[0] + 1
                temp_variations *= temp
            else:
                temp_variations *= x_max - x_min + 1
            temp_variations *= a_max - a_min + 1
            temp_variations *= s_max - s_min + 1

            variations += temp_variations

        if len(a_range) > 0:
            range_current_counter += 1

            temp_variations = 1
            temp = 0
            for p in a_range:
                temp += p[1] - p[0] + 1
            temp_variations *= temp

            if len(x_range) > 0:
                og = [(x_min, x_max)]
                for x in x_range:
                    temp = []
                    for o in og:
                        temp += remove_overlapping_range(x, o)
                    og = temp

                temp = 0
                for o in og:
                    if len(o) > 0:
                        temp += o[1] - o[0] + 1
                temp_variations *= temp
            else:
                temp_variations *= x_max - x_min + 1

            if len(m_range) > 0:
                og = [(m_min, m_max)]
                for x in m_range:
                    temp = []
                    for o in og:
                        temp += remove_overlapping_range(x, o)
                    og = temp

                temp = 0
                for o in og:
                    if len(o) > 0:
                        temp += o[1] - o[0] + 1
                temp_variations *= temp
            else:
                temp_variations *= m_max - m_min + 1
            temp_variations *= s_max - s_min + 1

            variations += temp_variations

        if len(s_range) > 0:
            range_current_counter += 1

            temp_variations = 1
            temp = 0
            for p in s_range:
                temp += p[1] - p[0] + 1
            temp_variations *= temp

            if len(x_range) > 0:
                og = [(x_min, x_max)]
                for x in x_range:
                    temp = []
                    for o in og:
                        temp += remove_overlapping_range(x, o)
                    og = temp

                temp = 0
                for o in og:
                    if len(o) > 0:
                        temp += o[1] - o[0] + 1
                temp_variations *= temp
            else:
                temp_variations *= x_max - x_min + 1

            if len(m_range) > 0:
                og = [(m_min, m_max)]
                for x in m_range:
                    temp = []
                    for o in og:
                        temp += remove_overlapping_range(x, o)
                    og = temp

                temp = 0
                for o in og:
                    if len(o) > 0:
                        temp += o[1] - o[0] + 1
                temp_variations *= temp
            else:
                temp_variations *= m_max - m_min + 1

            if len(a_range) > 0:
                og = [(a_min, a_max)]
                for x in a_range:
                    temp = []
                    for o in og:
                        temp += remove_overlapping_range(x, o)
                    og = temp

                temp = 0
                for o in og:
                    if len(o) > 0:
                        temp += o[1] - o[0] + 1
                temp_variations *= temp
            else:
                temp_variations *= a_max - a_min + 1

            variations += temp_variations


        # if len(x_range) == 0:
        #     variations *= x_max - x_min + 1
        # else:
        #     temp = 0
        #     for p in x_range:
        #         temp += p[1] - p[0] + 1
        #     variations *= temp
        
        # if len(m_range) == 0:
        #     variations *= m_max - m_min + 1
        # else:
        #     temp = 0
        #     for p in m_range:
        #         temp += p[1] - p[0] + 1
        #     variations *= temp
        
        # if len(a_range) == 0:
        #     variations *= a_max - a_min + 1
        # else:
        #     temp = 0
        #     for p in a_range:
        #         temp += p[1] - p[0] + 1
        #     variations *= temp
        
        # if len(s_range) == 0:
        #     variations *= s_max - s_min + 1
        # else:
        #     temp = 0
        #     for p in s_range:
        #         temp += p[1] - p[0] + 1
        #     variations *= temp
        
        print(f"{variations=}")
        full_variations += variations

        print("-------------------===================")
        print(x_range)
        print(m_range)
        print(a_range)
        print(s_range)
        print("-------------------===================")



print(f"            {full_variations=}")
print(f"Copied answer from example: 167409079868000")

# 167409079868000 good
# 496534091000000 mine