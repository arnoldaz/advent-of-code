
file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

with open("5x5-" + file_name, "w") as file:
    for _ in range(5):
        for line in lines:
            file.write(line * 5 + "\n")