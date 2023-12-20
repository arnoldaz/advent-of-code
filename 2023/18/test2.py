vertices = [(0, 0), (10, 0), (10, -20), (0, -20)]

def shoelace_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2
    return area

area = shoelace_area(vertices)
print(area)