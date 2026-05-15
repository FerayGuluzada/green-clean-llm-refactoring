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
    dp = [0] * (target + 1)
    dp[0] = 1
    
    def dfs(t: int) -> int:
        if dp[t] != 0:
            return dp[t]
        
        count = 0
        for num in nums:
            if t >= num:
                count += dfs(t - num)
        dp[t] = count
        return count
    
    return dfs(target)


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
    
    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                combs[i] += combs[i - num]
    
    return combs[target]


if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    target = 10
    print(combination_sum_topdown(nums, target))
    print(combination_sum_bottom_up(nums, target))