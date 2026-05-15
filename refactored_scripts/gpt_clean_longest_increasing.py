"""
Longest Increasing Subsequence

Find the length of the longest strictly increasing subsequence in an array.

Reference: https://en.wikipedia.org/wiki/Longest_increasing_subsequence

Complexity:
    longest_increasing_subsequence:
        Time:  O(n^2)
        Space: O(n)
    longest_increasing_subsequence_optimized:
        Time:  O(n * log(x))  where x is the max element
        Space: O(x)
    longest_increasing_subsequence_optimized2:
        Time:  O(n * log(n))
        Space: O(n)
"""

from __future__ import annotations


class _SegmentTree:
    def __init__(self, size: int) -> None:
        self.tree = [0] * (size << 2)

    def update(self, pos: int, left: int, right: int, target: int, value: int) -> None:
        if left == right:
            self.tree[pos] = value
            return

        mid = (left + right) >> 1
        child = pos << 1
        if target <= mid:
            self.update(child, left, mid, target, value)
        else:
            self.update(child | 1, mid + 1, right, target, value)

        self.tree[pos] = max(self.tree[child], self.tree[child | 1])

    def query_max(self, pos: int, left: int, right: int, start: int, end: int) -> int:
        if start > right or end < left:
            return 0
        if start <= left and right <= end:
            return self.tree[pos]

        mid = (left + right) >> 1
        child = pos << 1
        return max(
            self.query_max(child, left, mid, start, end),
            self.query_max(child | 1, mid + 1, right, start, end),
        )


def longest_increasing_subsequence(sequence: list[int]) -> int:
    """Find length of the longest increasing subsequence using O(n^2) DP.

    Args:
        sequence: List of integers.

    Returns:
        Length of the longest strictly increasing subsequence.

    Examples:
        >>> longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
        4
    """
    if not sequence:
        return 0

    counts = [1] * len(sequence)
    for i, current in enumerate(sequence[1:], start=1):
        for j in range(i):
            if current > sequence[j]:
                counts[i] = max(counts[i], counts[j] + 1)
    return max(counts)


def longest_increasing_subsequence_optimized(sequence: list[int]) -> int:
    """Find length of LIS using a segment tree for O(n*log(x)) time.

    Args:
        sequence: List of integers.

    Returns:
        Length of the longest strictly increasing subsequence.

    Examples:
        >>> longest_increasing_subsequence_optimized([10, 9, 2, 5, 3, 7, 101, 18])
        4
    """
    if not sequence:
        return 0

    max_val = max(sequence)
    tree = _SegmentTree(max_val + 1)
    best = 0

    for element in sequence:
        current = tree.query_max(1, 0, max_val, 0, element - 1) + 1
        best = max(best, current)
        tree.update(1, 0, max_val, element, current)

    return best


def longest_increasing_subsequence_optimized2(sequence: list[int]) -> int:
    """Find length of LIS using coordinate-compressed segment tree for O(n*log(n)).

    Args:
        sequence: List of integers.

    Returns:
        Length of the longest strictly increasing subsequence.

    Examples:
        >>> longest_increasing_subsequence_optimized2([10, 9, 2, 5, 3, 7, 101, 18])
        4
    """
    if not sequence:
        return 0

    length = len(sequence)
    tree = _SegmentTree(length)
    sorted_seq = sorted((value, -index) for index, value in enumerate(sequence))
    best = 0

    for _, neg_index in sorted_seq:
        index = -neg_index
        current = tree.query_max(1, 0, length - 1, 0, index - 1) + 1
        best = max(best, current)
        tree.update(1, 0, length - 1, index, current)

    return best


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))