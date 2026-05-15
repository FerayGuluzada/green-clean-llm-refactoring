"""
Weighted Job Scheduling

Given a set of jobs with start times, finish times, and profits, find
the maximum profit subset such that no two jobs overlap.

Reference: https://en.wikipedia.org/wiki/Job-shop_scheduling

Complexity:
    Time:  O(n log n) - improved from O(n^2)
    Space: O(n)
"""

from __future__ import annotations


class Job:
    """Represents a job with start time, finish time, and profit."""

    def __init__(self, start: int, finish: int, profit: int) -> None:
        self.start = start
        self.finish = finish
        self.profit = profit


def _find_latest_compatible(jobs: list[Job], current_idx: int) -> int:
    """Find the latest non-conflicting job before current_idx.
    
    Args:
        jobs: List of jobs sorted by finish time.
        current_idx: Index of the current job.
    
    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    left, right = 0, current_idx - 1
    latest_compatible = -1
    
    while left <= right:
        mid = (left + right) // 2
        if jobs[mid].finish <= jobs[current_idx].start:
            latest_compatible = mid
            left = mid + 1
        else:
            right = mid - 1
    return latest_compatible


def _compute_max_profit(jobs: list[Job]) -> int:
    """Compute maximum profit using dynamic programming.
    
    Args:
        jobs: List of Job objects sorted by finish time.
    
    Returns:
        Maximum achievable profit.
    """
    n = len(jobs)
    dp = [0] * n
    dp[0] = jobs[0].profit
    
    # Pre-compute latest compatible jobs
    latest = [-1] * n
    for i in range(1, n):
        latest[i] = _find_latest_compatible(jobs, i)
    
    # Fill DP table
    for i in range(1, n):
        include_profit = jobs[i].profit
        if latest[i] != -1:
            include_profit += dp[latest[i]]
        
        dp[i] = max(include_profit, dp[i - 1])
    
    return dp[n - 1]


def schedule(jobs: list[Job]) -> int:
    """Find the maximum profit from non-overlapping jobs.
    
    Args:
        jobs: List of Job objects.
    
    Returns:
        Maximum achievable profit.
    
    Examples:
        >>> schedule([Job(1, 3, 2), Job(2, 3, 4)])
        4
    """
    if not jobs:
        return 0
    
    jobs.sort(key=lambda j: j.finish)
    return _compute_max_profit(jobs)


if __name__ == "__main__":
    jobs = [
        Job(1, 3, 2),
        Job(2, 5, 4),
        Job(4, 6, 4),
        Job(6, 7, 3),
        Job(5, 8, 5),
        Job(7, 9, 2),
    ]
    print(schedule(jobs))