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
        si = sequence[i]
        ci = counts[i]
        for j in range(i):
            if si > sequence[j]:
                cj = counts[j] + 1
                if cj > ci:
                    ci = cj
        counts[i] = ci
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
    size = 1
    while size <= max_val:
        size <<= 1
    tree = [0] * (size << 1)
    
    ans = 0
    for element in sequence:
        # Query max in range [0, element-1]
        left = size
        right = size + element - 1
        cur = 0
        while left <= right:
            if left & 1:
                if tree[left] > cur:
                    cur = tree[left]
                left += 1
            if not (right & 1):
                if tree[right] > cur:
                    cur = tree[right]
                right -= 1
            left >>= 1
            right >>= 1
        
        cur += 1
        if cur > ans:
            ans = cur
        
        # Update tree at position element
        pos = size + element
        tree[pos] = cur
        pos >>= 1
        while pos:
            left_val = tree[pos << 1]
            right_val = tree[(pos << 1) | 1]
            new_val = left_val if left_val > right_val else right_val
            if tree[pos] == new_val:
                break
            tree[pos] = new_val
            pos >>= 1
    
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