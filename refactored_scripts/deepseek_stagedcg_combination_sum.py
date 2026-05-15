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
    # Sort nums to enable early termination in recursion
    nums_sorted = sorted(nums)
    dp = [-1] * (target + 1)
    dp[0] = 1

    def solve(remaining: int) -> int:
        if dp[remaining] != -1:
            return dp[remaining]

        total = 0
        # Iterate only through numbers <= remaining
        for num in nums_sorted:
            if num > remaining:
                break
            total += solve(remaining - num)

        dp[remaining] = total
        return total

    return solve(target)


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
    combs = [0] * (target + 1)
    combs[0] = 1
    
    # Sort nums to enable range-based optimization
    nums_sorted = sorted(nums)
    
    for i in range(1, target + 1):
        # Use local variable to avoid repeated list access
        current = 0
        for num in nums_sorted:
            if num > i:
                break
            current += combs[i - num]
        combs[i] = current

    return combs[target]


if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    target = 10
    print(combination_sum_topdown(nums, target))
    print(combination_sum_bottom_up(nums, target))