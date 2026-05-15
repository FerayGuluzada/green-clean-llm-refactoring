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


class SegmentTree:
    """Segment tree implementation for range max queries and point updates."""
    
    def __init__(self, size: int):
        self.tree = [0] * (size << 2)
        self.size = size
    
    def update(self, pos: int, left: int, right: int, target: int, value: int) -> None:
        """Update the tree at target position with value."""
        if left == right:
            self.tree[pos] = value
            return
            
        mid = (left + right) >> 1
        if target <= mid:
            self.update(pos << 1, left, mid, target, value)
        else:
            self.update((pos << 1) | 1, mid + 1, right, target, value)
            
        self.tree[pos] = max(self.tree[pos << 1], self.tree[(pos << 1) | 1])
    
    def query(self, pos: int, left: int, right: int, start: int, end: int) -> int:
        """Query maximum value in range [start, end]."""
        if left > end or right < start:
            return 0
        if left >= start and right <= end:
            return self.tree[pos]
            
        mid = (left + right) >> 1
        return max(
            self.query(pos << 1, left, mid, start, end),
            self.query((pos << 1) | 1, mid + 1, right, start, end)
        )


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
    tree = SegmentTree(max_val + 1)
    
    result = 0
    for element in sequence:
        current_length = tree.query(1, 0, max_val, 0, element - 1) + 1
        result = max(result, current_length)
        tree.update(1, 0, max_val, element, current_length)
        
    return result


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
    tree = SegmentTree(length)
    
    # Create mapping from values to their sorted indices
    indexed_sequence = [(value, -i) for i, value in enumerate(sequence)]
    indexed_sequence.sort()
    
    result = 0
    for value, neg_index in indexed_sequence:
        i = -neg_index
        current_length = tree.query(1, 0, length - 1, 0, i - 1) + 1
        result = max(result, current_length)
        tree.update(1, 0, length - 1, i, current_length)
        
    return result


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))