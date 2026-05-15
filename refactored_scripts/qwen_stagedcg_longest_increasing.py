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
import bisect


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
    
    # Process each element starting from the second one
    for i in range(1, length):
        # Check all previous elements to find the best subsequence to extend
        for j in range(i):
            if sequence[j] < sequence[i]:
                counts[i] = max(counts[i], counts[j] + 1)
                
    return max(counts)


def longest_increasing_subsequence_optimized(sequence: List[int]) -> int:
    """Find length of LIS using binary search for O(n*log(n)) time.

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
        
    # tails[i] stores the smallest tail of all increasing subsequences of length i+1
    tails = []
    
    for element in sequence:
        # Find the position where element should be inserted to keep tails sorted
        pos = bisect.bisect_left(tails, element)
        
        # If element is larger than all elements in tails, extend the sequence
        if pos == len(tails):
            tails.append(element)
        else:
            # Replace the first element that is >= element to maintain smallest possible tails
            tails[pos] = element
            
    return len(tails)


def longest_increasing_subsequence_optimized2(sequence: List[int]) -> int:
    """Alternative implementation of optimized LIS using manual binary search.

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
        
    # tails[i] stores the smallest tail of all increasing subsequences of length i+1
    tails = []
    
    for element in sequence:
        # Binary search for insertion point
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) >> 1
            if tails[mid] < element:
                left = mid + 1
            else:
                right = mid
                
        # If element is larger than all elements in tails, extend the sequence
        if left == len(tails):
            tails.append(element)
        else:
            # Replace the first element that is >= element to maintain smallest possible tails
            tails[left] = element
            
    return len(tails)


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))