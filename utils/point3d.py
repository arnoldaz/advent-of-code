class Point3d:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"{{{self.x}, {self.y}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other) -> "Point3d":
        if other is None:
            raise RuntimeError(f"Adding 'None' to 'Point3d' - {self}")

        if isinstance(other, Point3d):
            return Point3d(self.x + other.x, self.y + other.y, self.z + other.z)

        if isinstance(other, int):
            return Point3d(self.x + other, self.y + other, self.z + other)

        # if isinstance(other, Direction2d):
        #     return Point3d(self.x + other.value.x, self.y + other.value.y)

        raise RuntimeError(f"Unrecognized variable added to 'Point3d' - {other}")

    def __sub__(self, other) -> "Point3d":
        if other is None:
            raise RuntimeError(f"Subtracting 'None' from 'Point3d' - {self}")

        if isinstance(other, Point3d):
            return Point3d(self.x - other.x, self.y - other.y, self.z - other.z)

        if isinstance(other, int):
            return Point3d(self.x - other, self.y - other, self.z - other)

        # if isinstance(other, Direction2d):
        #     return Point3d(self.x - other.value.x, self.y - other.value.y)

        raise RuntimeError(f"Unrecognized variable subtracted from 'Point3d' - {other}")

    def __mul__(self, other):
        if isinstance(other, int):
            return Point3d(self.x * other, self.y * other, self.z * other)

        raise RuntimeError(f"Unrecognized variable multiplied with 'Point3d' - {other}")

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        if isinstance(other, Point3d):
            return self.x == other.x and self.y == other.y

        raise RuntimeError(f"Unrecognized variable compared to 'Point3d' - {other}")

    def copy(self) -> "Point3d":
        return Point3d(self.x, self.y, self.z)

    def abs(self) -> "Point3d":
        return Point3d(abs(self.x), abs(self.y), abs(self.z))

    def euclidean_distance_squared(self, other: "Point3d") -> float:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
