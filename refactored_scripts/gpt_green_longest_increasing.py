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
    if length == 0:
        return 0

    counts = [1] * length
    best = 1

    for i in range(1, length):
        seq_i = sequence[i]
        best_i = 1
        for j in range(i):
            if seq_i > sequence[j]:
                candidate = counts[j] + 1
                if candidate > best_i:
                    best_i = candidate
        counts[i] = best_i
        if best_i > best:
            best = best_i

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

    max_val = max(sequence)
    if max_val < 0:
        return 0

    size = max_val + 1
    tree = [0] * (size << 1)

    def _query(end: int) -> int:
        if end < 0:
            return 0
        left = size
        right = end + size
        result = 0
        while left < right:
            if left & 1:
                value = tree[left]
                if value > result:
                    result = value
                left += 1
            if right & 1:
                right -= 1
                value = tree[right]
                if value > result:
                    result = value
            left >>= 1
            right >>= 1
        return result

    def _update(index: int, value: int) -> None:
        pos = index + size
        if tree[pos] >= value:
            return
        tree[pos] = value
        pos >>= 1
        while pos:
            left_val = tree[pos << 1]
            right_val = tree[(pos << 1) | 1]
            new_val = left_val if left_val >= right_val else right_val
            if tree[pos] == new_val:
                break
            tree[pos] = new_val
            pos >>= 1

    ans = 0
    for element in sequence:
        cur = _query(element) + 1
        if cur > ans:
            ans = cur
        _update(element, cur)
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
    length = len(sequence)
    if length == 0:
        return 0

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