from functools import lru_cache

with open("input-test.txt") as file:
    lines = [line.rstrip() for line in file]

@lru_cache
def slide_north(lines):
    new_lines = list(lines[:])
    
    changed = False
    for i in range(1, len(new_lines)):
        for j in range(0, len(new_lines[i])):
            if new_lines[i][j] == "O" and new_lines[i-1][j] == ".":
                new_lines[i] = new_lines[i][:j] + "." + new_lines[i][j+1:]
                new_lines[i-1] = new_lines[i-1][:j] + "O" + new_lines[i-1][j+1:]
                changed = True
                
    return new_lines, changed

def calculate_points(final_lines):
    line_count = len(final_lines)
    answer = 0

    for i, line in enumerate(final_lines):
        count = line.count("O")
        answer += (line_count - i) * count

    return answer

def rotate_matrix(lines):
    return ["".join(line) for line in zip(*lines[::-1])]

def slide_cycle(lines):
    new_lines = lines[:]
    changed = True
    
    # north
    while changed:
        new_lines, changed = slide_north(tuple(new_lines))
        
    # print_matrix(new_lines)
        
    # west
    changed = True
    new_lines = rotate_matrix(tuple(new_lines))
    while changed:
        new_lines, changed = slide_north(tuple(new_lines))
        
    # print_matrix(new_lines)
        
    # sount
    changed = True
    new_lines = rotate_matrix(tuple(new_lines))
    while changed:
        new_lines, changed = slide_north(tuple(new_lines))
        
    # print_matrix(new_lines)
    
    # east
    changed = True
    new_lines = rotate_matrix(tuple(new_lines))
    while changed:
        new_lines, changed = slide_north(tuple(new_lines))
        
    # print_matrix(new_lines)
        
    new_lines = rotate_matrix(tuple(new_lines))
    return new_lines
        
def print_matrix(lines):
    print("==================================")
    for line in lines:
        print(line)
    print("==================================")



# points = calculate_points(lines)
# print(f"{points=}")




# new_lines = slide_cycle(lines)
# print_matrix(new_lines)
# new_lines = slide_cycle(new_lines)
# print_matrix(new_lines)
# new_lines = slide_cycle(new_lines)
# print_matrix(new_lines)


new_lines = lines[:]
for i in range(0, 1000000):
    new_lines = slide_cycle(new_lines)
    print(f"----- {i} -----")
    print_matrix(new_lines)




# for line in lines:
#     print(line)
# print("==============================")
    
# lines = ["".join(line) for line in zip(*lines[::-1])]

# for line in lines:
#     print(line)
# print("==============================")
    
    
# lines = ["".join(line) for line in zip(*lines[::-1])]

# for line in lines:
#     print(line)
# print("==============================")
    
# lines = ["".join(line) for line in zip(*lines[::-1])]

# for line in lines:
#     print(line)
# print("==============================")