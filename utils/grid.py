from collections.abc import Iterator
from itertools import zip_longest
from typing import Optional
from utils.point2d import Point2d, Direction2d

class Grid[T]:
    _data: list[list[T]]

    def __init__(self, data: list[T] | list[list[T]]):
        self._data = [list(row) for row in data] # type: ignore

    def height(self) -> int:
        return len(self._data)

    def width(self) -> int:
        return len(self._data[0])

    def get_data(self) -> list[list[T]]:
        return self._data

    @staticmethod
    def create_empty[K](symbol: K, width: int, height: int) -> "Grid[K]":
        return Grid[K]([[symbol for _ in range(width)] for _ in range(height)])

    def get_symbol(self, position: Point2d) -> T:
        return self._data[position.y][position.x]

    def set_symbol(self, position: Point2d, symbol: T):
        self._data[position.y][position.x] = symbol

    def in_bounds(self, position: Point2d) -> bool:
        return 0 <= position.x < self.width() and 0 <= position.y < self.height()

    def get_neighbors(self, position: Point2d, include_diagonal: bool = False, exclude_orthogonal: bool = False) -> list[Point2d]:
        return [
            neighbor
            for direction in Direction2d.get_all_directions(include_diagonal, exclude_orthogonal)
            if (neighbor := position + direction) and self.in_bounds(neighbor)
        ]

    def get_neighbors_with_directions(self, position: Point2d, include_diagonal: bool = False, exclude_orthogonal: bool = False) -> list[tuple[Point2d, Direction2d]]:
        return [
            (neighbor, direction)
            for direction in Direction2d.get_all_directions(include_diagonal, exclude_orthogonal)
            if (neighbor := position + direction) and self.in_bounds(neighbor)
        ]

    def find_first_character_instance(self, symbol_to_find: T) -> Point2d:
        return next(
            Point2d(x, y)
            for y, line in enumerate(self._data)
            for x, char in enumerate(line)
            if char == symbol_to_find
        )

    def find_all_character_instances(self, symbol_to_find: T) -> list[Point2d]:
        return [
            Point2d(x, y)
            for y, line in enumerate(self._data)
            for x, char in enumerate(line)
            if char == symbol_to_find
        ]

    def count_all_character_instances(self, symbol_to_count: T) -> int:
        return sum(
            char == symbol_to_count
            for line in self._data
            for char in line
        )

    def get_row(self, row_index: int) -> list[T]:
        return self._data[row_index]

    def get_column(self, column_index: int) -> list[T]:
        return [row[column_index] for row in self._data]

    def get_columns(self, fill_value: T) -> list[list[T]]:
        return [list(column) for column in zip_longest(*self._data, fillvalue=fill_value)]

    def copy(self) -> "Grid[T]":
        return Grid([list(row) for row in self._data])

    def rotate_clockwise(self):
        # TODO: check whether this should change to zip_longest
        self._data = [list(row) for row in zip(*reversed(self._data))]

    def print(self, single_symbol_space: int = 1):
        print(
            "\n".join(
                [
                    "".join([f"{item:>{single_symbol_space}}" for item in row])
                    for row in self._data
                ]
            )
        )

    def iterate(self, start: Optional[Point2d] = None, end: Optional[Point2d] = None) -> Iterator[tuple[Point2d, T]]:
        start = start if start is not None else Point2d(0, 0)
        end = end if end is not None else Point2d(self.width(), self.height())
        for y in range(start.y, end.y):
            for x in range(start.x, end.x):
                point = Point2d(x, y)
                yield (point, self.get_symbol(point))

    @staticmethod
    def iterate_lines(lines: list[str]) -> Iterator[tuple[Point2d, str]]:
        width, height = len(lines[0]), len(lines)
        for y in range(height):
            for x in range(width):
                yield (Point2d(x, y), lines[y][x])

