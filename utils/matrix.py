from typing import Optional
from utils.point import Direction, Point

class Matrix:
    _data: list[list[str]]

    def __init__(self, data: list[str]):
        assert len(data) > 0 and len(data[0]) > 0
        self._data = [list(string) for string in data]

    def height(self) -> int:
        return len(self._data)

    def width(self) -> int:
        return len(self._data[0])

    def get_data(self) -> list[list[str]]:
        return self._data

    def get_symbol(self, position: Point) -> Optional[str]:
        return self._data[position.y][position.x] if self.in_bounds(position) else None

    def in_bounds(self, position: Point) -> bool:
        return 0 <= position.x < self.width() and 0 <= position.y < self.height()

    def get_neighbors(self, position: Point) -> list[tuple[Point, Direction]]:
        return [(position + direction.value, direction) for direction in Direction if direction != Direction.Default and self.in_bounds(position + direction.value)]
