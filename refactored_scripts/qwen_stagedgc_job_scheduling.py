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


def _binary_search(jobs: list[Job], start_index: int) -> int:
    """Find the latest non-conflicting job before start_index.

    Args:
        jobs: List of jobs sorted by finish time.
        start_index: Index of the current job.

    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    target_start = jobs[start_index].start
    left, right = 0, start_index - 1
    result = -1
    
    while left <= right:
        mid = (left + right) >> 1  # Faster than // 2
        if jobs[mid].finish <= target_start:
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
    jobs.sort(key=lambda j: j.finish)
    
    length = len(jobs)
    # Use list instead of array for better cache performance
    table = [0] * length
    table[0] = jobs[0].profit

    for i in range(1, length):
        # Calculate profit including current job
        incl_prof = jobs[i].profit
        pos = _binary_search(jobs, i)
        if pos != -1:
            incl_prof += table[pos]

        # Store maximum of including and excluding current job
        table[i] = max(incl_prof, table[i - 1])

    return table[length - 1]


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