def find_starting_point(matrix):
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == '#':
                return (j, i)  # Return coordinates as (x, y)
    return None

def get_next_direction(matrix, x, y, direction, visited):
    # Directions are in the order of right, down, left, up to rotate clockwise
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    idx = directions.index(direction)

    for _ in range(4):
        idx = (idx + 1) % 4
        new_direction = directions[idx]
        new_x, new_y = x + new_direction[0], y + new_direction[1]

        if (0 <= new_x < len(matrix[0]) and 0 <= new_y < len(matrix) and
                matrix[new_y][new_x] == '#' and (new_x, new_y) not in visited):
            return new_direction
    return None

def convert_to_vertices(matrix):
    start = find_starting_point(matrix)
    if not start:
        return []

    vertices = [start]
    direction = (1, 0)  # Initially move to the right
    x, y = start
    visited = {start}

    while True:
        next_direction = get_next_direction(matrix, x, y, direction, visited)
        if next_direction is None:
            break

        if next_direction != direction:
            vertices.append((x, y))  # Add vertex when direction changes
            direction = next_direction

        x += direction[0]
        y += direction[1]
        visited.add((x, y))

        # If we have returned to the start, break
        if (x, y) == start:
            break

    return vertices

input_matrix = [
    "........",
    ".#######",
    ".#.....#",
    ".###...#",
    "...#...#",
    "...#...#",
    ".###.###",
    ".#...#..",
    ".##..###",
    "..#....#",
    "..######"
]

a=convert_to_vertices(input_matrix)

print(a)