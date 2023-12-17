

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

MULTIPLY_COUNT = 5

with open("unfolded-" + file_name, "w") as file:
    for line in lines:
        split_data = line.split(" ")
        arangement_data = "?".join([split_data[0] for _ in range(0, MULTIPLY_COUNT)])
        arangements_records = ",".join([split_data[1] for _ in range(0, MULTIPLY_COUNT)])

        file.write(f"{arangement_data} {arangements_records}\n")