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
        tree = self.tree
        while left != right:
            mid = (left + right) >> 1
            child = pos << 1
            if target <= mid:
                pos = child
                right = mid
            else:
                pos = child | 1
                left = mid + 1

        if value <= tree[pos]:
            return

        tree[pos] = value
        while pos > 1:
            pos >>= 1
            child = pos << 1
            new_value = tree[child]
            right_value = tree[child | 1]
            if right_value > new_value:
                new_value = right_value
            if tree[pos] == new_value:
                break
            tree[pos] = new_value

    def query_max(self, pos: int, left: int, right: int, start: int, end: int) -> int:
        if start > end:
            return 0

        tree = self.tree
        result = 0
        stack = [(pos, left, right)]

        while stack:
            pos, left, right = stack.pop()
            if start > right or end < left:
                continue
            if start <= left and right <= end:
                value = tree[pos]
                if value > result:
                    result = value
                continue

            mid = (left + right) >> 1
            child = pos << 1
            stack.append((child | 1, mid + 1, right))
            stack.append((child, left, mid))

        return result


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
    best = 1

    for i, current in enumerate(sequence[1:], start=1):
        current_best = 1
        for j in range(i):
            if current > sequence[j]:
                candidate = counts[j] + 1
                if candidate > current_best:
                    current_best = candidate
        counts[i] = current_best
        if current_best > best:
            best = current_best

    return best


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
    query_max = tree.query_max
    update = tree.update

    for element in sequence:
        current = query_max(1, 0, max_val, 0, element - 1) + 1
        if current > best:
            best = current
        update(1, 0, max_val, element, current)

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
    query_max = tree.query_max
    update = tree.update

    for _, neg_index in sorted_seq:
        index = -neg_index
        current = query_max(1, 0, length - 1, 0, index - 1) + 1
        if current > best:
            best = current
        update(1, 0, length - 1, index, current)

    return best


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))