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

    __slots__ = ("start", "finish", "profit")

    def __init__(self, start: int, finish: int, profit: int) -> None:
        self.start = start
        self.finish = finish
        self.profit = profit


def _binary_search(finishes: list[int], current_start: int, right: int) -> int:
    """Find the latest non-conflicting job ending on or before current_start.

    Args:
        finishes: Finish times of jobs sorted in ascending order.
        current_start: Start time of the current job.
        right: Rightmost index to search.

    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    left = 0
    latest_compatible = -1

    while left <= right:
        mid = (left + right) >> 1
        if finishes[mid] <= current_start:
            latest_compatible = mid
            left = mid + 1
        else:
            right = mid - 1

    return latest_compatible


def schedule(job: list[Job]) -> int:
    """Find the maximum profit from non-overlapping jobs.

    Args:
        job: List of Job objects.

    Returns:
        Maximum achievable profit.

    Examples:
        >>> schedule([Job(1, 3, 2), Job(2, 3, 4)])
        4
    """
    if not job:
        return 0

    jobs = sorted(job, key=lambda current_job: current_job.finish)
    job_count = len(jobs)

    finishes = [current_job.finish for current_job in jobs]
    profits = [0] * job_count
    profits[0] = jobs[0].profit

    for index in range(1, job_count):
        current_job = jobs[index]
        compatible_index = _binary_search(finishes, current_job.start, index - 1)

        profit_including_current = current_job.profit
        if compatible_index >= 0:
            profit_including_current += profits[compatible_index]

        previous_profit = profits[index - 1]
        profits[index] = (
            profit_including_current
            if profit_including_current > previous_profit
            else previous_profit
        )

    return profits[-1]


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