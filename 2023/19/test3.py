def remove_overlapping_range(range1, range2):
    start1, end1 = range1
    start2, end2 = range2

    # Check if there is an overlap between the two ranges
    if end1 >= start2 and start1 <= end2:
        # Identify the overlapping range
        overlapping_start = max(start1, start2)
        overlapping_end = min(end1, end2)

        # Remove the overlapping range from the second range
        if overlapping_end == end2:
            remaining_ranges = []  # No remaining range
        else:
            remaining_ranges = [(overlapping_end + 1, end2)]

        # Check if there is a range before the overlapping part
        if overlapping_start > start2:
            remaining_ranges.insert(0, (start2, overlapping_start - 1))

        return remaining_ranges
    else:
        # No overlap, return the second range as a list
        return [range2]

# Example usage:
range1 = (2, 21)
range2 = (5, 15)

remaining_ranges = remove_overlapping_range(range1, range2)
print("Remaining Ranges:", remaining_ranges)