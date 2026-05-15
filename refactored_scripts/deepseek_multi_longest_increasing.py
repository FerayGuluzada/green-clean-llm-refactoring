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
    length = len(sequence)
    counts = [1] * length
    
    for i in range(1, length):
        for j in range(i):
            if sequence[i] > sequence[j]:
                counts[i] = max(counts[i], counts[j] + 1)
    
    return max(counts)


class SegmentTree:
    """Segment tree for range maximum queries and point updates."""
    
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size * 4)
    
    def _update(self, pos: int, left: int, right: int, target: int, value: int) -> None:
        if left == right:
            self.tree[pos] = value
            return
        
        mid = (left + right) >> 1
        if target <= mid:
            self._update(pos << 1, left, mid, target, value)
        else:
            self._update((pos << 1) | 1, mid + 1, right, target, value)
        
        self.tree[pos] = max(self.tree[pos << 1], self.tree[(pos << 1) | 1])
    
    def _query(self, pos: int, left: int, right: int, start: int, end: int) -> int:
        if left > end or right < start:
            return 0
        if left >= start and right <= end:
            return self.tree[pos]
        
        mid = (left + right) >> 1
        return max(
            self._query(pos << 1, left, mid, start, end),
            self._query((pos << 1) | 1, mid + 1, right, start, end)
        )
    
    def update(self, index: int, value: int) -> None:
        self._update(1, 0, self.size - 1, index, value)
    
    def query_range(self, start: int, end: int) -> int:
        return self._query(1, 0, self.size - 1, start, end)


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
    tree = SegmentTree(max_val + 1)
    ans = 0
    
    for element in sequence:
        cur = tree.query_range(0, element - 1) + 1
        ans = max(ans, cur)
        tree.update(element, cur)
    
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
    if not sequence:
        return 0
    
    length = len(sequence)
    tree = SegmentTree(length)
    
    # Create sorted list of (value, -index) pairs for stable sorting
    sorted_pairs = sorted((x, -i) for i, x in enumerate(sequence))
    ans = 0
    
    for value, neg_idx in sorted_pairs:
        i = -neg_idx
        cur = tree.query_range(0, i - 1) + 1
        ans = max(ans, cur)
        tree.update(i, cur)
    
    return ans


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))