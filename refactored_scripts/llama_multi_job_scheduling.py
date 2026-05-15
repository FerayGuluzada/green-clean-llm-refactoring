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
    left, right = 0, start_index - 1
    while left <= right:
        mid = (left + right) // 2
        if jobs[mid].finish <= jobs[start_index].start:
            if mid + 1 < start_index and jobs[mid + 1].finish <= jobs[start_index].start:
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
    """
    # Sort jobs by finish time
    jobs = sorted(jobs, key=lambda j: j.finish)

    # Initialize table to store maximum profit at each index
    max_profit = [0] * len(jobs)
    max_profit[0] = jobs[0].profit

    # Fill table using dynamic programming
    for i in range(1, len(jobs)):
        incl_prof = jobs[i].profit
        prev_job_index = _binary_search(jobs, i)
        if prev_job_index!= -1:
            incl_prof += max_profit[prev_job_index]
        max_profit[i] = max(incl_prof, max_profit[i - 1])

    # Return maximum profit
    return max_profit[-1]


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