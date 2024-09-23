def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge overlapping intervals of integers. The intervals are given as a list of two-element lists,
    where each two-element list contains the start and end of the interval.
    The intervals are merged if they overlap, and the result is a sorted list of non-overlapping intervals.
    The time complexity is O(n log n), since a sort operation is required.
    The space complexity is O(n), since in the worst case all intervals are merged into a single interval.
    The intervals are given as a list of two-element lists, where each two-element list contains the start and end of the interval.
    The intervals are merged if they overlap, and the result is a sorted list of non-overlapping intervals.

    :param intervals: A list of two-element lists, where each two-element list contains the start and end of the interval.
    :return: A sorted list of non-overlapping intervals.
    """

    # Check if there are no intervals
    if len(intervals) < 1:
        return []

    # Sort the intervals by the start time
    intervals.sort(key=lambda x: x[0])

    merged_intervals = [intervals[0]]

    # Merge overlapping intervals
    for i in range(1, len(intervals)):
        # Check if the current interval overlaps with the previous one
        if intervals[i][0] <= merged_intervals[-1][1]:
            merged_intervals[-1][1] = max(merged_intervals[-1][1], intervals[i][1])
        else:
            merged_intervals.append(intervals[i])

    return merged_intervals


merged_intervals = merge_intervals(
    [[20, 22], [2, 6], [1, 3], [4, 5], [8, 10], [12, 18]]
)

print(merged_intervals)
