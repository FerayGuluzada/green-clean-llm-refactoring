"""
Weighted Job Scheduling

Given a set of jobs with start times, finish times, and profits, find
the maximum profit subset such that no two jobs overlap.

Reference: https://en.wikipedia.org/wiki/Job-shop_scheduling

Complexity:
    Time:  O(n^2)
    Space: O(n)
"""

from __future__ import annotations


class Job:
    """Represents a job with start time, finish time, and profit."""

    def __init__(self, start: int, finish: int, profit: int) -> None:
        self.start = start
        self.finish = finish
        self.profit = profit


def _binary_search(jobs: list[Job], current_index: int) -> int:
    """Find the latest non-conflicting job before current_index.

    Args:
        jobs: List of jobs sorted by finish time.
        current_index: Index of the current job.

    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    left, right = 0, current_index - 1
    result = -1
    
    # Cache current job's start time to avoid repeated attribute access
    current_start = jobs[current_index].start
    
    while left <= right:
        mid = (left + right) >> 1  # Bit shift for faster division by 2
        if jobs[mid].finish <= current_start:
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
        
    # Sort in place to reduce memory allocation
    jobs.sort(key=lambda j: j.finish)
    n = len(jobs)
    
    # Use list instead of recreating with multiplication for better cache performance
    table = [0] * n
    table[0] = jobs[0].profit

    for i in range(1, n):
        # Profit including current job
        incl_profit = jobs[i].profit
        latest_non_conflicting = _binary_search(jobs, i)
        
        if latest_non_conflicting != -1:
            incl_profit += table[latest_non_conflicting]

        # Store maximum of including or excluding current job
        table[i] = max(incl_profit, table[i - 1])

    return table[-1]


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