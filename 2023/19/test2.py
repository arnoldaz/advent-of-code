def find_overlap(range1, range2):
    start = max(range1[0], range2[0])
    end = min(range1[1], range2[1])

    # Check if there is an actual overlap
    if start <= end:
        return (start, end)
    else:
        return None

# Example usage
range1 = (8, 15)
range2 = (5, 20)

overlap = find_overlap(range1, range2)

if overlap:
    print(f"Overlap found: {overlap}")
else:
    print("No overlap")