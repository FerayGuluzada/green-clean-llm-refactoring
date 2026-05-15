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
        
    length = len(sequence)
    counts = [1] * length  # Use list multiplication instead of comprehension
    max_length = 1  # Track maximum during iteration to avoid final max() call
    
    for i in range(1, length):
        for j in range(i):  # Remove redundant 0 start
            if sequence[i] > sequence[j]:
                candidate = counts[j] + 1
                if candidate > counts[i]:
                    counts[i] = candidate
        if counts[i] > max_length:
            max_length = counts[i]
            
    return max_length


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
    tree = [0] * (max_val * 4)  # Use * instead of << for clarity

    def _update(pos: int, left: int, right: int, target: int, vertex: int) -> None:
        if left == right:
            tree[pos] = vertex
            return
        mid = (left + right) >> 1
        if target <= mid:
            _update(pos << 1, left, mid, target, vertex)
        else:
            _update((pos << 1) | 1, mid + 1, right, target, vertex)
        # Inline max operation
        left_val = tree[pos << 1]
        right_val = tree[(pos << 1) | 1]
        tree[pos] = left_val if left_val > right_val else right_val

    def _get_max(pos: int, left: int, right: int, start: int, end: int) -> int:
        if left > end or right < start:
            return 0
        if left >= start and right <= end:
            return tree[pos]
        mid = (left + right) >> 1
        left_result = _get_max(pos << 1, left, mid, start, end)
        right_result = _get_max((pos << 1) | 1, mid + 1, right, start, end)
        return left_result if left_result > right_result else right_result

    ans = 0
    for element in sequence:
        cur = _get_max(1, 0, max_val, 0, element - 1) + 1
        if cur > ans:
            ans = cur
        _update(1, 0, max_val, element, cur)
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
    tree = [0] * (length * 4)  # Use * instead of << for clarity
    # Precompute sorted indices to avoid tuple creation overhead
    indexed_sequence = [(sequence[i], i) for i in range(length)]
    indexed_sequence.sort()
    
    def _update(pos: int, left: int, right: int, target: int, vertex: int) -> None:
        if left == right:
            tree[pos] = vertex
            return
        mid = (left + right) >> 1
        if target <= mid:
            _update(pos << 1, left, mid, target, vertex)
        else:
            _update((pos << 1) | 1, mid + 1, right, target, vertex)
        # Inline max operation
        left_val = tree[pos << 1]
        right_val = tree[(pos << 1) | 1]
        tree[pos] = left_val if left_val > right_val else right_val

    def _get_max(pos: int, left: int, right: int, start: int, end: int) -> int:
        if left > end or right < start:
            return 0
        if left >= start and right <= end:
            return tree[pos]
        mid = (left + right) >> 1
        left_result = _get_max(pos << 1, left, mid, start, end)
        right_result = _get_max((pos << 1) | 1, mid + 1, right, start, end)
        return left_result if left_result > right_result else right_result

    ans = 0
    for value, original_index in indexed_sequence:
        cur = _get_max(1, 0, length - 1, 0, original_index - 1) + 1
        if cur > ans:
            ans = cur
        _update(1, 0, length - 1, original_index, cur)
    return ans

if __name__ == "__main__":
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    print(longest_increasing_subsequence(sequence))
    print(longest_increasing_subsequence_optimized(sequence))
    print(longest_increasing_subsequence_optimized2(sequence))