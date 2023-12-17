
file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

histories: list[list[int]] = []
for line in lines:
    histories.append([int(x) for x in line.split(" ")])

def count_extrapolated_values(histories: list[list[int]]) -> int:
    final_sum = 0
    for history in histories:
        sequences: list[list[int]] = [history]
        current_sequence = history
        while True:
            if all(x == 0 for x in current_sequence):
                break

            sequence: list[int] = []
            for i in range(1, len(current_sequence)):
                sequence.append(current_sequence[i] - current_sequence[i-1])
            sequences.append(sequence)
            current_sequence = sequence[:]

        sum = 0
        for sequence in sequences:
            sum += sequence[-1]

        final_sum += sum

    return final_sum

def count_extrapolated_backwards_values(histories: list[list[int]]) -> int:
    final_sum = 0
    for history in histories:
        sequences: list[list[int]] = [history]
        current_sequence = history
        while True:
            if all(x == 0 for x in current_sequence):
                break

            sequence: list[int] = []
            for i in range(1, len(current_sequence)):
                sequence.append(current_sequence[i] - current_sequence[i-1])
            sequences.append(sequence)
            current_sequence = sequence[:]

        sum = 0
        sequences.reverse()
        for i in range(1, len(sequences)):
            sum = sequences[i][0] - sum

        final_sum += sum

    return final_sum

print(f"{count_extrapolated_values(histories)=}")
print(f"{count_extrapolated_backwards_values(histories)=}")