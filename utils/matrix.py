from typing import Optional
from utils.point import Direction, Point

class Matrix[T]:
    _data: list[list[T]]

    def __init__(self, data: list[str], cast_type: type):
        assert len(data) > 0 and len(data[0]) > 0
        self._data = [cast_type(string) for string in data]

    def height(self) -> int:
        return len(self._data)

    def width(self) -> int:
        return len(self._data[0])

    def get_data(self) -> list[list[T]]:
        return self._data

    def get_symbol(self, position: Point) -> Optional[T]:
        return self._data[position.y][position.x] if self.in_bounds(position) else None

    def in_bounds(self, position: Point) -> bool:
        return 0 <= position.x < self.width() and 0 <= position.y < self.height()

    def get_neighbors(self, position: Point) -> list[tuple[Point, Direction]]:
        return [(position + direction.value, direction) for direction in Direction if direction != Direction.NONE and self.in_bounds(position + direction.value)]

    def find_first_character_instance(self, symbol_to_find: T) -> Optional[Point]:
        for y, line in enumerate(self.get_data()):
            for x, char in enumerate(line):
                if char == symbol_to_find:
                    return Point(x, y)

        return None

def rotate_matrix(lines: list[str]):
    return ["".join(line) for line in zip(*lines[::-1])]
