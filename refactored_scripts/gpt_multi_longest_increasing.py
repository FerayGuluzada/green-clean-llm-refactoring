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
        best = 1
        for j in range(i):
            if current > sequence[j]:
                candidate = counts[j] + 1
                if candidate > best:
                    best = candidate
        counts[i] = best
    return max(counts)


def _segment_tree_update(
    tree: list[int], pos: int, left: int, right: int, target: int, value: int
) -> None:
    if left == right:
        tree[pos] = value
        return

    mid = (left + right) >> 1
    child = pos << 1
    if target <= mid:
        _segment_tree_update(tree, child, left, mid, target, value)
    else:
        _segment_tree_update(tree, child | 1, mid + 1, right, target, value)
    tree[pos] = max(tree[child], tree[child | 1])


def _segment_tree_query(
    tree: list[int], pos: int, left: int, right: int, start: int, end: int
) -> int:
    if start > right or end < left:
        return 0
    if start <= left and right <= end:
        return tree[pos]

    mid = (left + right) >> 1
    child = pos << 1
    return max(
        _segment_tree_query(tree, child, left, mid, start, end),
        _segment_tree_query(tree, child | 1, mid + 1, right, start, end),
    )


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
    tree = [0] * ((max_val + 1) << 2)
    ans = 0

    for element in sequence:
        cur = _segment_tree_query(tree, 1, 0, max_val, 0, element - 1) + 1
        if cur > ans:
            ans = cur
        _segment_tree_update(tree, 1, 0, max_val, element, cur)

    return ans


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
    length = len(sequence)
    if length == 0:
        return 0

    tree = [0] * (length << 2)
    sorted_seq = sorted((value, -index) for index, value in enumerate(sequence))
    ans = 0

    for _, neg_index in sorted_seq:
        index = -neg_index
        cur = _segment_tree_query(tree, 1, 0, length - 1, 0, index - 1) + 1
        if cur > ans:
            ans = cur
        _segment_tree_update(tree, 1, 0, length - 1, index, cur)

    return ans


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))