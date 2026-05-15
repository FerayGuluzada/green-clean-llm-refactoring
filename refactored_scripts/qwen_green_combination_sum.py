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


def _helper_topdown(
    nums: list[int], target: int, dp: list[int]
) -> int:
    """Recursive helper that fills the dp table top-down.

    Args:
        nums: Positive integer array without duplicates.
        target: Remaining target value.
        dp: Memoisation table.

    Returns:
        Number of combinations that sum to target.
    """
    # Check if already computed
    if dp[target] != -1:
        return dp[target]
    
    result = 0
    # Process only valid numbers (early pruning)
    for num in nums:
        if num <= target:
            result += _helper_topdown(nums, target - num, dp)
    
    dp[target] = result
    return result


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
    # Initialize DP table
    dp = [-1] * (target + 1)
    dp[0] = 1  # Base case: one way to make 0 (use no elements)
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
    # Initialize combinations array
    combs = [0] * (target + 1)
    combs[0] = 1  # Base case: one way to make 0
    
    # Sort nums for early termination optimization
    nums.sort()
    
    # Build combinations for each sum from 1 to target
    for i in range(1, target + 1):
        for num in nums:
            # Early termination: if num > i, all subsequent nums will also be > i
            if num > i:
                break
            combs[i] += combs[i - num]
    
    return combs[target]



if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    target = 10
    print(combination_sum_topdown(nums, target))
    print(combination_sum_bottom_up(nums, target))