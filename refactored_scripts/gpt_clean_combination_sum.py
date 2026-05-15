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


def _helper_topdown(nums: list[int], remaining: int, memo: list[int]) -> int:
    """Recursive helper that fills the dp table top-down.

    Args:
        nums: Positive integer array without duplicates.
        remaining: Remaining target value.
        memo: Memoisation table.

    Returns:
        Number of combinations that sum to target.
    """
    cached = memo[remaining]
    if cached != -1:
        return cached

    total_combinations = 0
    for num in nums:
        if num <= remaining:
            total_combinations += _helper_topdown(nums, remaining - num, memo)

    memo[remaining] = total_combinations
    return total_combinations


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
    memo = [-1] * (target + 1)
    memo[0] = 1
    return _helper_topdown(nums, target, memo)


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
    combinations = [0] * (target + 1)
    combinations[0] = 1

    for current_target in range(1, target + 1):
        total_combinations = 0
        for num in nums:
            if num <= current_target:
                total_combinations += combinations[current_target - num]
        combinations[current_target] = total_combinations

    return combinations[target]


if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    target = 10
    print(combination_sum_topdown(nums, target))
    print(combination_sum_bottom_up(nums, target))