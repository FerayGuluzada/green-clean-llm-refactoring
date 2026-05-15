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
    """Segment tree for range maximum queries."""
    
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size * 4)
    
    def update(self, target: int, value: int) -> None:
        """Update value at position target."""
        self._update(1, 0, self.size - 1, target, value)
    
    def query(self, start: int, end: int) -> int:
        """Get maximum value in range [start, end]."""
        return self._query(1, 0, self.size - 1, start, end)
    
    def _update(self, pos: int, left: int, right: int, target: int, value: int) -> None:
        if left == right:
            self.tree[pos] = value
            return
        
        mid = (left + right) // 2
        if target <= mid:
            self._update(pos * 2, left, mid, target, value)
        else:
            self._update(pos * 2 + 1, mid + 1, right, target, value)
        
        self.tree[pos] = max(self.tree[pos * 2], self.tree[pos * 2 + 1])
    
    def _query(self, pos: int, left: int, right: int, start: int, end: int) -> int:
        if left > end or right < start:
            return 0
        if start <= left and right <= end:
            return self.tree[pos]
        
        mid = (left + right) // 2
        left_max = self._query(pos * 2, left, mid, start, end)
        right_max = self._query(pos * 2 + 1, mid + 1, right, start, end)
        
        return max(left_max, right_max)


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
        cur = tree.query(0, element - 1) + 1
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
    
    # Sort by value, then by negative index to maintain stability
    sorted_indices = sorted(range(length), key=lambda i: (sequence[i], -i))
    ans = 0
    
    for i in sorted_indices:
        cur = tree.query(0, i - 1) + 1
        ans = max(ans, cur)
        tree.update(i, cur)
    
    return ans


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))