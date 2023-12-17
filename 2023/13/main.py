with open("input.txt") as file:
    lines = [line.rstrip() for line in file]
    
patterns = []
temp_pattern = []
for line in lines:
    if line.strip() == "":
        patterns.append(temp_pattern)
        temp_pattern = []
        continue
    
    temp_pattern.append(line)
patterns.append(temp_pattern)

def check_horizontal(pattern):
    line_length = len(pattern)

    for i in range(0, line_length - 1):
        if pattern[i] == pattern[i + 1]:
            mirror = i
            
            j = 1
            while True:
                if i - j < 0 or i + j + 1 > line_length - 1:
                    return mirror + 1
                
                if pattern[i - j] != pattern[i + j + 1]:
                    break
                
                j += 1
        
    return -1

def check_horizontal_single_change(pattern):
    line_length = len(pattern)
    
    diff_amount = 0
    for i in range(0, line_length - 1):
        if pattern[i] == pattern[i + 1]:
            mirror = i
            
            j = 1
            while True:
                if i - j < 0 or i + j + 1 > line_length - 1:
                    if diff_amount > 0:
                        return mirror + 1
                    else:
                        break
                
                if diff_amount == 0 and nearly_equal(pattern[i - j], pattern[i + j + 1]):
                    diff_amount += 1
                    j += 1
                    continue
                
                if pattern[i - j] != pattern[i + j + 1]:
                    break
                
                j += 1
        
        
    diff_amount = 0
    for i in range(0, line_length - 1):
        if nearly_equal(pattern[i], pattern[i + 1]):
            mirror = i
            
            j = 1
            while True:
                if i - j < 0 or i + j + 1 > line_length - 1:
                    return mirror + 1
                
                if pattern[i - j] != pattern[i + j + 1]:
                    break
                
                j += 1
    
    return -1

def check_vertical(pattern):
    transposed_pattern = [''.join(s) for s in zip(*pattern)]
    return check_horizontal(transposed_pattern)
        
def check_vertical_single_change(pattern):
    transposed_pattern = [''.join(s) for s in zip(*pattern)]
    return check_horizontal_single_change(transposed_pattern)
        
def nearly_equal(string1, string2):
    count_diffs = 0
    for a, b in zip(string1, string2):
        if a != b:
            if count_diffs > 1: 
                return False
            count_diffs += 1
    return count_diffs == 1

sum = 0
for pattern in patterns:
    horizontal = check_horizontal_single_change(pattern)
    # print(f"single change {horizontal=}")
    if horizontal != -1:
        sum += horizontal * 100
        continue
    
    vertical = check_vertical_single_change(pattern)
    # print(f"single change {vertical=}")
    if vertical != -1:
        sum += vertical
    
    
print(f"{sum=}")