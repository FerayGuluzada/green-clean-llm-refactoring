"""
Weighted Job Scheduling

Given a set of jobs with start times, finish times, and profits, find
the maximum profit subset such that no two jobs overlap.

Reference: https://en.wikipedia.org/wiki/Job-shop_scheduling

Complexity:
    Time:  O(n log n)
    Space: O(n)
"""

from __future__ import annotations


class Job:
    """Represents a job with start time, finish time, and profit."""

    def __init__(self, start: int, finish: int, profit: int) -> None:
        self.start = start
        self.finish = finish
        self.profit = profit


def _binary_search(jobs: list[Job], index: int) -> int:
    """Find the latest non-conflicting job before the given index.

    Args:
        jobs: List of jobs sorted by finish time.
        index: Index of the current job.

    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    target_start_time = jobs[index].start
    left, right = 0, index - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if jobs[mid].finish <= target_start_time:
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    return result


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

    # Sort jobs by finish time
    sorted_jobs = sorted(jobs, key=lambda j: j.finish)
    
    # Initialize DP table
    dp = [0] * len(sorted_jobs)
    dp[0] = sorted_jobs[0].profit

    # Fill DP table
    for i in range(1, len(sorted_jobs)):
        # Profit including current job
        incl_profit = sorted_jobs[i].profit
        latest_non_conflicting = _binary_search(sorted_jobs, i)
        
        if latest_non_conflicting != -1:
            incl_profit += dp[latest_non_conflicting]

        # Store maximum of including or excluding current job
        dp[i] = max(incl_profit, dp[i - 1])

    return dp[-1]


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