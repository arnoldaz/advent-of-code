import math
from utils.list import remove_list_indexes

class Point3d:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"{{{self.x}, {self.y}, {self.z}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def euclidean_distance(self, other: "Point3d") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

def parse_input(lines: list[str]) -> None:
    pass

def silver_solution(lines: list[str]) -> int:
    points: list[Point3d] = []
    for line in lines:
        points.append(Point3d(*[int(x) for x in line.split(",")]))

    distances: dict[Point3d, dict[Point3d, float]] = {}
    global_distances: dict[float, tuple[Point3d, Point3d]] = {}
    for point in points:
        for other_point in points:
            if point == other_point:
                continue

            if point in distances and other_point in distances[point]:
                continue

            distance = point.euclidean_distance(other_point)
            global_distances[distance] = (point, other_point)
            distances.setdefault(point, {})[other_point] = distance
            distances.setdefault(other_point, {})[point] = distance


    stuff = sorted(global_distances.keys())
    # print(stuff, len(stuff))

    circuits: list[set[Point3d]] = []

    for dist in stuff[:1000]:
        point1, point2 = global_distances[dist]
        # print(dist, point1, point2)

        added = 0
        for circuit in circuits:
            if point1 in circuit or point2 in circuit:
                circuit.add(point1)
                circuit.add(point2)
                added += 1

        if added == 0:
            circuits.append(set([point1, point2]))
        if added > 1:
            new_set = set[Point3d]()
            index_to_remove = []
            for i, circuit in enumerate(circuits):
                if point1 in circuit:
                    index_to_remove.append(i)
                    new_set.update(circuit)

            remove_list_indexes(circuits, index_to_remove)
            circuits.append(new_set)

    lens = sorted([len(x) for x in circuits], reverse=True)[:3]

    return math.prod(lens)

def gold_solution(lines: list[str]) -> int:
    points: list[Point3d] = []
    for line in lines:
        points.append(Point3d(*[int(x) for x in line.split(",")]))

    distances: dict[Point3d, dict[Point3d, float]] = {}
    global_distances: dict[float, tuple[Point3d, Point3d]] = {}
    for point in points:
        for other_point in points:
            if point == other_point:
                continue

            if point in distances and other_point in distances[point]:
                continue

            distance = point.euclidean_distance(other_point)
            global_distances[distance] = (point, other_point)
            distances.setdefault(point, {})[other_point] = distance
            distances.setdefault(other_point, {})[point] = distance


    stuff = sorted(global_distances.keys())
    # print(stuff, len(stuff))

    circuits: list[set[Point3d]] = []

    for dist in stuff:
        point1, point2 = global_distances[dist]
        # print(dist, point1, point2)

        added = 0
        for circuit in circuits:
            if point1 in circuit or point2 in circuit:
                circuit.add(point1)
                circuit.add(point2)
                added += 1

        if added == 0:
            circuits.append(set([point1, point2]))
        if added > 1:
            new_set = set[Point3d]()
            index_to_remove = []
            for i, circuit in enumerate(circuits):
                if point1 in circuit:
                    index_to_remove.append(i)
                    new_set.update(circuit)

            remove_list_indexes(circuits, index_to_remove)
            circuits.append(new_set)

        if len(circuits) == 1 and len(circuits[0]) == len(points):
            return point1.x * point2.x

    return -1
