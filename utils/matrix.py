from utils.point import INVALID_POINT, Direction, DirectionDiagonal, DirectionOnlyDiagonal, Point

class Matrix[T]:
    _data: list[list[T]]

    def __init__(self, data: list[str] | list[list[str]] | list[list[int]], cast_type: type):
        self.initialize(data, cast_type)

    def height(self) -> int:
        return len(self._data)

    def width(self) -> int:
        return len(self._data[0])

    def get_data(self) -> list[list[T]]:
        return self._data

    def initialize(self, data: list[str] | list[list[str]] | list[list[int]], cast_type: type):
        assert len(data) > 0 and len(data[0]) > 0
        self._data = [[cast_type(char) for char in string] for string in data]

    def get_symbol(self, position: Point) -> T:
        return self._data[position.y][position.x]

    def set_symbol(self, position: Point, symbol: T):
        self._data[position.y][position.x] = symbol

    def in_bounds(self, position: Point) -> bool:
        return 0 <= position.x < self.width() and 0 <= position.y < self.height()

    def get_neighbors(self, position: Point) -> list[tuple[Point, Direction]]:
        return [(position + direction.value, direction) for direction in Direction if direction != Direction.NONE and self.in_bounds(position + direction.value)]

    def get_neighbors_diagonal(self, position: Point) -> list[tuple[Point, DirectionDiagonal]]:
        return [(position + direction.value, direction) for direction in DirectionDiagonal if direction != DirectionDiagonal.NONE and self.in_bounds(position + direction.value)]

    def get_neighbors_only_diagonal(self, position: Point) -> list[tuple[Point, DirectionOnlyDiagonal]]:
        return [(position + direction.value, direction) for direction in DirectionOnlyDiagonal if direction != DirectionOnlyDiagonal.NONE and self.in_bounds(position + direction.value)]

    def find_first_character_instance(self, symbol_to_find: T) -> Point:
        for y, line in enumerate(self.get_data()):
            for x, char in enumerate(line):
                if char == symbol_to_find:
                    return Point(x, y)

        return INVALID_POINT

    def get_row(self, row_index: int) -> list[T]:
        return self._data[row_index]

    def get_column(self, column_index: int) -> list[T]:
        return [row[column_index] for row in self._data]

    def rotate_clockwise(self):
        self._data = [list(row) for row in zip(*reversed(self._data))]

    def print(self, single_symbol_space: int):
        print("\n".join(["".join([f"{item:>{single_symbol_space}}" for item in row]) for row in self._data]))
