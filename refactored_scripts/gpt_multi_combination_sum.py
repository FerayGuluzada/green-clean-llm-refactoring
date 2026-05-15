"""
Combination Sum IV

Given an array of distinct positive integers and a target, find the number
of possible combinations (order matters) that add up to the target.

Reference: https://leetcode.com/problems/combination-sum-iv/

Complexity:
    combination_sum_topdown:
        Time:  O(target * n)
        Space: O(target)
    combination_sum_bottom_up:
        Time:  O(target * n)
        Space: O(target)
"""

from __future__ import annotations


def _prepare_nums(nums: list[int], target: int) -> list[int]:
    """Return sorted candidates that can contribute to the target."""
    return sorted(num for num in nums if num <= target)


def _helper_topdown(nums: list[int], target: int, dp: list[int]) -> int:
    """Recursive helper that fills the dp table top-down.

    Args:
        nums: Positive integer array without duplicates.
        target: Remaining target value.
        dp: Memoisation table.

    Returns:
        Number of combinations that sum to target.
    """
    cached = dp[target]
    if cached != -1:
        return cached

    total = 0
    for num in nums:
        if num > target:
            break
        total += _helper_topdown(nums, target - num, dp)

    dp[target] = total
    return total


def combination_sum_topdown(nums: list[int], target: int) -> int:
    """Find number of combinations that add up to target (top-down DP).

    Args:
        nums: Positive integer array without duplicates.
        target: Target sum.

    Returns:
        Number of ordered combinations that sum to target.

    Examples:
        >>> combination_sum_topdown([1, 2, 3], 4)
        7
    """
    nums = _prepare_nums(nums, target)
    dp = [-1] * (target + 1)
    dp[0] = 1
    return _helper_topdown(nums, target, dp)


def combination_sum_bottom_up(nums: list[int], target: int) -> int:
    """Find number of combinations that add up to target (bottom-up DP).

    Args:
        nums: Positive integer array without duplicates.
        target: Target sum.

    Returns:
        Number of ordered combinations that sum to target.

    Examples:
        >>> combination_sum_bottom_up([1, 2, 3], 4)
        7
    """
    nums = _prepare_nums(nums, target)
    combs = [0] * (target + 1)
    combs[0] = 1

    for current in range(1, target + 1):
        total = 0
        for num in nums:
            if num > current:
                break
            total += combs[current - num]
        combs[current] = total

    return combs[target]


if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    target = 10
    print(combination_sum_topdown(nums, target))
    print(combination_sum_bottom_up(nums, target))