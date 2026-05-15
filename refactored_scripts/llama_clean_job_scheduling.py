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


def _find_latest_non_conflicting_job(jobs: list[Job], current_index: int) -> int:
    """Find the latest non-conflicting job before current_index.

    Args:
        jobs: List of jobs sorted by finish time.
        current_index: Index of the current job.

    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    for i in range(current_index - 1, -1, -1):
        if jobs[i].finish <= jobs[current_index].start:
            return i
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

    # Base case: maximum profit for the first job is its own profit
    max_profit[0] = jobs[0].profit

    # Fill table using dynamic programming
    for i in range(1, len(jobs)):
        # Find the latest non-conflicting job
        latest_non_conflicting_index = _find_latest_non_conflicting_job(jobs, i)

        # Calculate maximum profit including the current job
        including_current_job = jobs[i].profit
        if latest_non_conflicting_index!= -1:
            including_current_job += max_profit[latest_non_conflicting_index]

        # Update maximum profit at the current index
        max_profit[i] = max(including_current_job, max_profit[i - 1])

    # Return the maximum profit for the last job
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