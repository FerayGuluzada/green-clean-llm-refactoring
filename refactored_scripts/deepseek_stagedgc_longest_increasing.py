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
    n = len(sequence)
    if n <= 1:
        return n
    
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if sequence[i] > sequence[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


def _segment_tree_size(max_val: int) -> int:
    """Calculate next power of two for segment tree size."""
    size = 1
    while size <= max_val:
        size <<= 1
    return size


def _query_max(tree: list[int], size: int, left: int, right: int) -> int:
    """Query maximum value in segment tree range [left, right]."""
    left += size
    right += size
    result = 0
    
    while left <= right:
        if left & 1:
            result = max(result, tree[left])
            left += 1
        if not (right & 1):
            result = max(result, tree[right])
            right -= 1
        left >>= 1
        right >>= 1
    
    return result


def _update_tree(tree: list[int], size: int, pos: int, value: int) -> None:
    """Update segment tree at position pos with value."""
    idx = size + pos
    tree[idx] = value
    idx >>= 1
    
    while idx:
        left_child = tree[idx << 1]
        right_child = tree[(idx << 1) | 1]
        new_val = max(left_child, right_child)
        
        if tree[idx] == new_val:
            break
        tree[idx] = new_val
        idx >>= 1


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
    size = _segment_tree_size(max_val)
    tree = [0] * (size << 1)
    answer = 0
    
    for num in sequence:
        # Query max in range [0, num-1]
        best = _query_max(tree, size, 0, num - 1)
        current = best + 1
        answer = max(answer, current)
        
        # Update tree at position num
        _update_tree(tree, size, num, current)
    
    return answer


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