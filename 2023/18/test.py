def flood_fill(matrix, row, col, fill_char, boundary_char):
    if row < 0 or row >= len(matrix) or col < 0 or col >= len(matrix[0]) or matrix[row][col] != '.':
        return

    matrix[row][col] = fill_char

    flood_fill(matrix, row + 1, col, fill_char, boundary_char)  # Down
    flood_fill(matrix, row - 1, col, fill_char, boundary_char)  # Up
    flood_fill(matrix, row, col + 1, fill_char, boundary_char)  # Right
    flood_fill(matrix, row, col - 1, fill_char, boundary_char)  # Left

def find_cells_inside_polygon(matrix):
    fill_char = '+'  # You can use any character to represent cells inside the polygon
    boundary_char = '#'

    # Find a point inside the polygon (centroid)
    total_rows, total_cols = len(matrix), len(matrix[0])
    total_points = 0
    centroid_row, centroid_col = 0, 0

    for row in range(total_rows):
        for col in range(total_cols):
            if matrix[row][col] == '.':
                centroid_row += row
                centroid_col += col
                total_points += 1

    centroid_row = 2
    centroid_col = 4

    flood_fill(matrix, centroid_row, centroid_col, fill_char, boundary_char)

if __name__ == "__main__":
    matrix = [
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

    matrix = [list(row) for row in matrix]

    find_cells_inside_polygon(matrix)

    for row in matrix:
        print(''.join(row))
