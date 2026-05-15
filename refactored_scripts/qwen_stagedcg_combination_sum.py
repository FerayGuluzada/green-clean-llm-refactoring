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
    memo = [-1] * (target + 1)
    memo[0] = 1
    
    def _count_combinations(remaining: int) -> int:
        if memo[remaining] != -1:
            return memo[remaining]
        
        count = 0
        # Filter nums to only those <= remaining for efficiency
        for num in nums:
            if num <= remaining:
                count += _count_combinations(remaining - num)
        
        memo[remaining] = count
        return count
    
    return _count_combinations(target)


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
    dp = [0] * (target + 1)
    dp[0] = 1
    
    # Pre-sort nums to enable early termination in inner loop
    sorted_nums = sorted(nums)
    
    for current_target in range(1, target + 1):
        for num in sorted_nums:
            if num > current_target:
                break  # Early termination since nums are sorted
            dp[current_target] += dp[current_target - num]
    
    return dp[target]


if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    target = 10
    print(combination_sum_topdown(nums, target))
    print(combination_sum_bottom_up(nums, target))