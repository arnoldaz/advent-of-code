def split_ranges_corrected(original_ranges, critical_ranges):
    # Extracting all critical points (start and end) from the critical_ranges
    critical_points = set()
    for start, end in critical_ranges:
        critical_points.add(start)
        critical_points.add(end)

    # Splitting the original ranges based on these critical points
    split_ranges = []
    for start, end in original_ranges:
        # Finding critical points within the current range
        points_in_range = sorted([p for p in critical_points if start <= p <= end])

        # If there are no critical points in the range, add the range as it is
        if not points_in_range:
            split_ranges.append((start, end))
            continue

        # Splitting the range based on the critical points
        current_start = start
        for point in points_in_range:
            # Adjusting the end of the current split range
            current_end = point if current_start == point else point - 1
            if current_start <= current_end:
                split_ranges.append((current_start, current_end))
            current_start = point + 1
        if current_start <= end:
            split_ranges.append((current_start, end))

    # Removing any duplicate or empty ranges
    return sorted(set(split_ranges))


# Example usage
original_ranges = [(79, 92), (55, 150)]
critical_ranges = [(98, 99), (50, 95)]
result = split_ranges_corrected(original_ranges, critical_ranges)

print(result)