from enum import Enum

with open("input-area2.txt") as file:
    lines = [line.rstrip() for line in file]
    

start_x = 0
start_y = 0

for y in range(0, len(lines)):
    line = lines[y]
    for x in range(0, len(line)):
        if line[x] == "S":
            start_x = x
            start_y = y
            
print(f"Starting pos {start_x=} {start_y=}")

current = (start_x, start_y)
current_length = 0

class Direction(Enum):
    No = 0
    Up = 1
    Down = 2
    Left = 3
    Right = 4

direction = Direction.No

# top
if direction == Direction.No and current[1] - 1 >= 0:
    symbol = lines[current[1] - 1][current[0]]
    if symbol == "|" or symbol == "F" or symbol == "7":
        direction = Direction.Up
        current = (current[0], current[1] - 1)

# bot
if direction == Direction.No and current[1] + 1 <= len(lines):
    symbol = lines[current[1] + 1][current[0]]
    if symbol == "|" or symbol == "L" or symbol == "J":
        direction = Direction.Down
        current = (current[0], current[1] + 1)

# left
if direction == Direction.No and current[0] - 1 >= 0:
    symbol = lines[current[1]][current[0] - 1]
    if symbol == "-" or symbol == "J" or symbol == "7":
        direction = Direction.Left
        current = (current[0] - 1, current[1])
        
# right
if direction == Direction.No and current[0] + 1 <= len(lines[0]):
    symbol = lines[current[1]][current[0] + 1]
    if symbol == "-" or symbol == "F" or symbol == "L":
        direction = Direction.Right
        current = (current[0] + 1, current[1])
        
# print(direction)
# print(current)


final_path = []

while True:
    symbol = lines[current[1]][current[0]]
    final_path.append(current)
    
    if symbol == "|":
        if direction == Direction.Up:
            current = (current[0], current[1] - 1)
            direction = Direction.Up
        elif direction == Direction.Down:
            current = (current[0], current[1] + 1)
            direction = Direction.Down
            
        current_length += 1
        continue
    elif symbol == "-":
        if direction == Direction.Left:
            current = (current[0] - 1, current[1])
            direction = Direction.Left
        elif direction == Direction.Right:
            current = (current[0] + 1, current[1])
            direction = Direction.Right

        current_length += 1
        continue
    elif symbol == "L":
        if direction == Direction.Left:
            current = (current[0], current[1] - 1)
            direction = Direction.Up
        elif direction == Direction.Down:
            current = (current[0] + 1, current[1])
            direction = Direction.Right
        
        current_length += 1
        continue
    elif symbol == "J":
        if direction == Direction.Right:
            current = (current[0], current[1] - 1)
            direction = Direction.Up
        elif direction == Direction.Down:
            current = (current[0] - 1, current[1])
            direction = Direction.Left
        
        current_length += 1
        continue
    elif symbol == "7":
        if direction == Direction.Right:
            current = (current[0], current[1] + 1)
            direction = Direction.Down
        elif direction == Direction.Up:
            current = (current[0] - 1, current[1])
            direction = Direction.Left
        
        current_length += 1
        continue
    elif symbol == "F":
        if direction == Direction.Left:
            current = (current[0], current[1] + 1)
            direction = Direction.Down
        elif direction == Direction.Up:
            current = (current[0] + 1, current[1])
            direction = Direction.Right
        
        current_length += 1
        continue
    elif symbol == ".":
        print("wtf")
        continue
    elif symbol == "S":
        print("found start")
        current_length += 1
        break

print(f"Ending stuff {current_length=}")   
print(f"Answer {current_length // 2}")   

test = 0
result = []

# print(final_path)

for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        if (x, y) in final_path:
            continue

        vertical_counter_pos = [coord for coord in final_path if coord[0] == x and coord[1] > y]
        vertical_counter_neg = [coord for coord in final_path if coord[0] == x and coord[1] < y]
        # horizontal_counter_pos = sum(1 for coord in final_path if coord[1] == y and coord[0] > x)
        # horizontal_counter_neg = sum(1 for coord in final_path if coord[1] == y and coord[0] < x)
        
        # print(f"{x=} {y=} {vertical_counter_pos=} {vertical_counter_neg=}")
        
        # vertical_counter = [coord for coord in final_path if coord[0] == x and coord[1] > y]
        if len(vertical_counter_pos) == 0 or len(vertical_counter_neg) == 0:
            continue
        
        # vertical_counter_pos.sort()
        # vertical_counter_neg.sort()
        
        real_counter_pos1 = 1
        for i in range(1, len(vertical_counter_pos)):
            if vertical_counter_pos[i][1] != vertical_counter_pos[i - 1][1] + 1:
                real_counter_pos1 += 1
        
        real_counter_pos2 = 1
        for i in range(1, len(vertical_counter_pos)):
            if vertical_counter_pos[i][1] != vertical_counter_pos[i - 1][1] - 1:
                real_counter_pos2 += 1
        
        real_counter_pos = min(real_counter_pos1, real_counter_pos2)
        
        real_counter_neg1 = 1
        for i in range(1, len(vertical_counter_neg)):
            if vertical_counter_neg[i][1] != vertical_counter_neg[i - 1][1] + 1:
                real_counter_neg1 += 1
        
        real_counter_neg2 = 1
        for i in range(1, len(vertical_counter_neg)):
            if vertical_counter_neg[i][1] != vertical_counter_neg[i - 1][1] - 1:
                real_counter_neg2 += 1
        
        real_counter_neg = min(real_counter_neg1, real_counter_neg2)
        
        print(f"{x=} {y=} {vertical_counter_pos=} {real_counter_pos=} {vertical_counter_neg=} {real_counter_neg=}")
        
        if real_counter_pos % 2 != 0 and real_counter_neg % 2 != 0:
            test += 1
            result.append((x, y))
        
        # if vertical_counter_pos == 0 or vertical_counter_neg == 0 or horizontal_counter_pos == 0 or horizontal_counter_neg == 0:
        #     continue
        
        # if vertical_counter_pos % 2 != 0 and vertical_counter_pos != 0 and horizontal_counter_pos % 2 != 0 and horizontal_counter_pos != 0:
        #     test += 1
        #     result.append((x, y))



print(f"{test=}")
print(f"{result=}")

