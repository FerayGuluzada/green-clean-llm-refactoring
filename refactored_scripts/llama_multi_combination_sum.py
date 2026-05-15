"""
Combination Sum IV

Given an array of distinct positive integers and a target, find the number
of possible combinations (order matters) that add up to the target.

Reference: https://leetcode.com/problems/combination-sum-iv/

Complexity:
    combination_sum:
        Time:  O(target * n)
        Space: O(target)
"""

from __future__ import annotations


def combination_sum(nums: list[int], target: int) -> int:
    """Find number of combinations that add up to target (bottom-up DP).

    Args:
        nums: Positive integer array without duplicates.
        target: Target sum.

    Returns:
        Number of ordered combinations that sum to target.

    Examples:
        >>> combination_sum([1, 2, 3], 4)
        7
    """
    # Initialize dp table with base case dp[0] = 1
    dp = [1] + [0] * target
    
    # Fill dp table in bottom-up manner
    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]
    
    return dp[target]


if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    target = 10
    print(combination_sum(nums, target))