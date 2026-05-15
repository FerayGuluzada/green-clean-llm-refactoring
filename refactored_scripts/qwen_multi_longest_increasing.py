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
from typing import List


def longest_increasing_subsequence(sequence: List[int]) -> int:
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
        
    length = len(sequence)
    counts = [1] * length
    
    for i in range(1, length):
        for j in range(i):
            if sequence[j] < sequence[i]:
                counts[i] = max(counts[i], counts[j] + 1)
                
    return max(counts)


def longest_increasing_subsequence_optimized(sequence: List[int]) -> int:
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
    tree = [0] * (max_val << 2)

    def _update(pos: int, left: int, right: int, target: int, vertex: int) -> None:
        if left == right:
            tree[pos] = vertex
            return
        mid = (left + right) >> 1
        if target <= mid:
            _update(pos << 1, left, mid, target, vertex)
        else:
            _update((pos << 1) | 1, mid + 1, right, target, vertex)
        tree[pos] = max(tree[pos << 1], tree[(pos << 1) | 1])

    def _get_max(pos: int, left: int, right: int, start: int, end: int) -> int:
        if left > end or right < start:
            return 0
        if left >= start and right <= end:
            return tree[pos]
        mid = (left + right) >> 1
        return max(
            _get_max(pos << 1, left, mid, start, end),
            _get_max((pos << 1) | 1, mid + 1, right, start, end),
        )

    ans = 0
    for element in sequence:
        cur = _get_max(1, 0, max_val, 0, element - 1) + 1
        if cur > ans:
            ans = cur
        _update(1, 0, max_val, element, cur)
    return ans


def longest_increasing_subsequence_optimized2(sequence: List[int]) -> int:
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
    tree = [0] * (length << 2)
    # Create mapping from value to index in sorted array
    sorted_unique = sorted(set(sequence))
    value_to_index = {v: i for i, v in enumerate(sorted_unique)}
    
    # Sort by value, then by negative index to handle duplicates properly
    indexed_sequence = [(sequence[i], i) for i in range(length)]
    indexed_sequence.sort()

    def _update(pos: int, left: int, right: int, target: int, vertex: int) -> None:
        if left == right:
            tree[pos] = vertex
            return
        mid = (left + right) >> 1
        if target <= mid:
            _update(pos << 1, left, mid, target, vertex)
        else:
            _update((pos << 1) | 1, mid + 1, right, target, vertex)
        tree[pos] = max(tree[pos << 1], tree[(pos << 1) | 1])

    def _get_max(pos: int, left: int, right: int, start: int, end: int) -> int:
        if left > end or right < start:
            return 0
        if left >= start and right <= end:
            return tree[pos]
        mid = (left + right) >> 1
        return max(
            _get_max(pos << 1, left, mid, start, end),
            _get_max((pos << 1) | 1, mid + 1, right, start, end),
        )

    ans = 0
    for value, original_index in indexed_sequence:
        # Map the original index to its rank in the sorted unique values
        compressed_index = value_to_index[value]
        cur = _get_max(1, 0, length - 1, 0, original_index - 1) + 1
        if cur > ans:
            ans = cur
        _update(1, 0, length - 1, original_index, cur)
    return ans


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))