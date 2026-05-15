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
    best = 1

    for i, value in enumerate(sequence[1:], start=1):
        best_here = 1
        for j in range(i):
            if value > sequence[j]:
                best_here = max(best_here, counts[j] + 1)
        counts[i] = best_here
        best = max(best, best_here)

    return best


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

    max_value = max(sequence)
    if max_value < 0:
        return 0

    size = max_value + 1
    tree = [0] * (size << 1)

    def query(end: int) -> int:
        if end <= 0:
            return 0

        left = size
        right = end + size
        result = 0

        while left < right:
            if left & 1:
                result = max(result, tree[left])
                left += 1
            if right & 1:
                right -= 1
                result = max(result, tree[right])
            left >>= 1
            right >>= 1

        return result

    def update(index: int, value: int) -> None:
        pos = index + size
        if tree[pos] >= value:
            return

        tree[pos] = value
        pos >>= 1

        while pos:
            new_value = max(tree[pos << 1], tree[(pos << 1) | 1])
            if tree[pos] == new_value:
                return
            tree[pos] = new_value
            pos >>= 1

    best = 0
    for value in sequence:
        current = query(value) + 1
        best = max(best, current)
        update(value, current)

    return best


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
    tails: list[int] = []

    for value in sequence:
        left = 0
        right = len(tails)

        while left < right:
            mid = (left + right) >> 1
            if tails[mid] < value:
                left = mid + 1
            else:
                right = mid

        if left == len(tails):
            tails.append(value)
        else:
            tails[left] = value

    return len(tails)


if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))