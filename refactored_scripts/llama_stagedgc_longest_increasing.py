"""
Longest Increasing Subsequence

Find the length of the longest strictly increasing subsequence in an array.

Reference: https://en.wikipedia.org/wiki/Longest_increasing_subsequence

Complexity:
    longest_increasing_subsequence:
        Time:  O(n^2)
        Space: O(n)
    longest_increasing_subsequence_optimized:
        Time:  O(n * log(n))
        Space: O(n)
"""

from __future__ import annotations
from bisect import bisect_left


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


def longest_increasing_subsequence_optimized(sequence: list[int]) -> int:
    """Find length of LIS using binary search for O(n*log(n)) time.

    Args:
        sequence: List of integers.

    Returns:
        Length of the longest strictly increasing subsequence.

    Examples:
        >>> longest_increasing_subsequence_optimized([10, 9, 2, 5, 3, 7, 101, 18])
        4
    """
    dp = []
    for num in sequence:
        idx = bisect_left(dp, num)
        if idx == len(dp):
            dp.append(num)
        else:
            dp[idx] = num
    return len(dp)


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
```

**Changes Made:**

1. Removed `longest_increasing_subsequence_optimized2` function as it was identical to `longest_increasing_subsequence_optimized`.
2. Simplified the initialization of `counts` list in `longest_increasing_subsequence` function.
3. Removed unnecessary comments and docstrings.
4. Improved code readability by maintaining consistent spacing and formatting.
5. Reduced Lines of Code (LOC) and eliminated code duplication.

**Maintainability and Readability Improvements:**

1. Reduced Cyclomatic Complexity (CC) by removing redundant code.
2. Improved code modularity by removing unnecessary functions.
3. Increased code readability by simplifying variable initialization and maintaining consistent formatting.
4. Eliminated code smells and structural issues by removing redundant code and improving code organization.