from enum import Enum
from typing import Optional

class SplitMode(Enum):
    INCLUDE_LEFT = 1
    INCLUDE_RIGHT = 2
    NOT_INCLUDE = 3

class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"[{self.start}; {self.end}]"

    def __repr__(self) -> str:
        return self.__str__()

    def copy(self) -> "Range":
        return Range(self.start, self.end)

    def count(self) -> int:
        return self.end - self.start + 1

    def find_overlap(self, other_range: "Range") -> Optional["Range"]:
        start = max(self.start, other_range.start)
        end = min(self.end, other_range.end)

        return Range(start, end) if start <= end else None

    def remove_overlapping_range(self, range_to_cut: "Range") -> list["Range"]:
        # If range to cut is outside the source range, return just the source range itself
        if range_to_cut.end < self.start or range_to_cut.start > self.end:
            return [self.copy()]

        overlapping_start = max(range_to_cut.start, self.start)
        overlapping_end = min(range_to_cut.end, self.end)

        # Add multiple ranges depending on whether range to cut is at the start, middle or end of source range
        remaining_ranges: list[Range] = []

        if overlapping_start > self.start:
            remaining_ranges.append(Range(self.start, overlapping_start - 1))

        if overlapping_end < self.end:
            remaining_ranges.append(Range(overlapping_end + 1, self.end))

        return remaining_ranges

    @staticmethod
    def split_ranges(original_ranges: list["Range"], critical_ranges: list["Range"]) -> list["Range"]:
        # original_ranges = [Range(79, 92), Range(55, 150)]
        # critical_ranges = [Range(98, 99), Range(50, 95)]
        # result = [(79, 92), (55, 95), (96, 97), (98, 99), (100, 150)]

        modified_ranges = original_ranges[:]
        final_ranges = set()

        for critical_range in critical_ranges:
            for original_range in modified_ranges:
                overlap = original_range.find_overlap(critical_range)
                if not overlap:
                    final_ranges.add(original_range)
                else:
                    if original_range in final_ranges:
                        final_ranges.remove(original_range)

                    final_ranges.add(overlap)
                    final_ranges.update(original_range.remove_overlapping_range(overlap))

            modified_ranges = list(final_ranges)

        return list(final_ranges)

    def is_range_inside(self, inner_range: "Range") -> bool:
        # Whether inner range is in outer range
        return self.start <= inner_range.start <= inner_range.end <= self.end

    def get_number_count(self) -> int:
        return self.end - self.start + 1

    def split_range(self, number: int, mode: SplitMode = SplitMode.NOT_INCLUDE) -> tuple["Range", "Range"]:
        match mode:
            case SplitMode.INCLUDE_LEFT:
                return Range(self.start, number), Range(number + 1, self.end)
            case SplitMode.INCLUDE_RIGHT:
                return Range(self.start, number - 1), Range(number, self.end)
            case SplitMode.NOT_INCLUDE:
                return Range(self.start, number - 1), Range(number + 1, self.end)

    @staticmethod
    def combine_ranges(ranges_to_combine: list["Range"]) -> list["Range"]:
        sorted_ranges = sorted(ranges_to_combine, key=lambda x: (x.start, x.end))

        combined_ranges = [sorted_ranges[0]]
        last_index = 0
        for current_range in sorted_ranges[1:]:
            if current_range.find_overlap(combined_ranges[last_index]) is None:
                combined_ranges.append(current_range)
                last_index += 1
            else:
                combined_ranges[last_index] = Range(
                    combined_ranges[last_index].start,
                    max(combined_ranges[last_index].end, current_range.end)
                )

        return combined_ranges
