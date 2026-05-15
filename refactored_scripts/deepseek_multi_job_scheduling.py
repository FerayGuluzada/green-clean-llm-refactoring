"""
Weighted Job Scheduling

Given a set of jobs with start times, finish times, and profits, find
the maximum profit subset such that no two jobs overlap.

Reference: https://en.wikipedia.org/wiki/Job-shop_scheduling

Complexity:
    Time:  O(n log n) with binary search optimization
    Space: O(n)
"""

from __future__ import annotations


class Job:
    """Represents a job with start time, finish time, and profit."""

    def __init__(self, start: int, finish: int, profit: int) -> None:
        self.start = start
        self.finish = finish
        self.profit = profit


def _find_latest_compatible(jobs: list[Job], index: int) -> int:
    """Find the latest non-conflicting job before the given index.
    
    Uses binary search since jobs are sorted by finish time.
    
    Args:
        jobs: List of jobs sorted by finish time.
        index: Index of the current job.
    
    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    left, right = 0, index - 1
    
    while left <= right:
        mid = (left + right) // 2
        if jobs[mid].finish <= jobs[index].start:
            if mid + 1 <= index - 1 and jobs[mid + 1].finish <= jobs[index].start:
                left = mid + 1
            else:
                return mid
        else:
            right = mid - 1
    return -1


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
    
    # Sort once by finish time
    sorted_jobs = sorted(jobs, key=lambda j: j.finish)
    n = len(sorted_jobs)
    
    # DP table: max profit ending at each job
    dp = [0] * n
    dp[0] = sorted_jobs[0].profit
    
    for i in range(1, n):
        # Profit including current job
        incl_profit = sorted_jobs[i].profit
        prev_idx = _find_latest_compatible(sorted_jobs, i)
        
        if prev_idx != -1:
            incl_profit += dp[prev_idx]
        
        # Maximum of including or excluding current job
        dp[i] = max(incl_profit, dp[i - 1])
    
    return dp[n - 1]


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