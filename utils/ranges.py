from typing import NamedTuple, Optional

class Range(NamedTuple):
    start: int
    end: int

def find_overlap(range1: Range, range2: Range) -> Optional[Range]:
    start = max(range1.start, range2.start)
    end = min(range1.end, range2.end)

    return Range(start, end) if start <= end else None

def remove_overlapping_range(source_range: Range, range_to_cut: Range) -> list[Range]:
    # If range to cut is outside the source range, return just the source range itself
    if range_to_cut.end < source_range.start or range_to_cut.start > source_range.end:
        return [source_range]

    overlapping_start = max(range_to_cut.start, source_range.start)
    overlapping_end = min(range_to_cut.end, source_range.end)

    # Add multiple ranges depending on whether range to cut is at the start, middle or end of source range
    remaining_ranges: list[Range] = []

    if overlapping_start > source_range.start:
        remaining_ranges.append(Range(source_range.start, overlapping_start - 1))

    if overlapping_end < source_range.end:
        remaining_ranges.append(Range(overlapping_end + 1, source_range.end))

    return remaining_ranges

def split_ranges(original_ranges: list[Range], critical_ranges: list[Range]) -> list[Range]:
    # original_ranges = [Range(79, 92), Range(55, 150)]
    # critical_ranges = [Range(98, 99), Range(50, 95)]
    # result = [(79, 92), (55, 95), (96, 97), (98, 99), (100, 150)]

    modified_ranges = original_ranges[:]
    final_ranges = set()

    for critical_range in critical_ranges:
        for original_range in modified_ranges:
            overlap = find_overlap(original_range, critical_range)
            if not overlap:
                final_ranges.add(original_range)
            else:
                if original_range in final_ranges:
                    final_ranges.remove(original_range)

                final_ranges.add(overlap)
                final_ranges.update(remove_overlapping_range(original_range, overlap))

        modified_ranges = list(final_ranges)

    return list(final_ranges)

def range_in_range(outer_range: Range, inner_range: Range) -> bool:
    # Whether inner range is in outer range
    return outer_range.start <= inner_range.start <= inner_range.end <= outer_range.end
