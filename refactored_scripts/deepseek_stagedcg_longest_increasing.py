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
import bisect


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
    if length <= 1:
        return length
    
    counts = [1] * length
    
    for i in range(1, length):
        seq_i = sequence[i]
        count_i = counts[i]
        for j in range(i):
            if seq_i > sequence[j]:
                new_count = counts[j] + 1
                if new_count > count_i:
                    count_i = new_count
        counts[i] = count_i
    
    return max(counts)


class SegmentTree:
    """Segment tree for range maximum queries."""
    
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size * 2)
    
    def update(self, target: int, value: int) -> None:
        """Update value at position target."""
        pos = target + self.size
        self.tree[pos] = value
        pos //= 2
        while pos >= 1:
            self.tree[pos] = max(self.tree[pos * 2], self.tree[pos * 2 + 1])
            pos //= 2
    
    def query(self, start: int, end: int) -> int:
        """Get maximum value in range [start, end]."""
        if start > end:
            return 0
        
        left = start + self.size
        right = end + self.size
        result = 0
        
        while left <= right:
            if left % 2 == 1:
                result = max(result, self.tree[left])
                left += 1
            if right % 2 == 0:
                result = max(result, self.tree[right])
                right -= 1
            left //= 2
            right //= 2
        
        return result


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
        if cur > ans:
            ans = cur
        tree.update(element, cur)
    
    return ans


def longest_increasing_subsequence_optimized2(sequence: list[int]) -> int:
    """Find length of LIS using patience sorting for O(n*log(n)).

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
    
    tails = []
    
    for num in sequence:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))