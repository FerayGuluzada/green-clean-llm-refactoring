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


def _binary_search_latest_compatible(
    finishes: list[int], start_time: int, right: int
) -> int:
    """Find the latest non-conflicting job before the current position.

    Args:
        finishes: Finish times of jobs sorted in ascending order.
        start_time: Start time of the current job.
        right: Rightmost index to search.

    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    left = 0
    compatible_index = -1

    while left <= right:
        mid = (left + right) // 2
        if finishes[mid] <= start_time:
            compatible_index = mid
            left = mid + 1
        else:
            right -= 1 if mid == right else right - (mid - 1)

    return compatible_index


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

    sorted_jobs = sorted(jobs, key=lambda current_job: current_job.finish)
    finishes = [current_job.finish for current_job in sorted_jobs]

    max_profits = [0] * len(sorted_jobs)
    max_profits[0] = sorted_jobs[0].profit

    for index in range(1, len(sorted_jobs)):
        current_job = sorted_jobs[index]
        compatible_index = _binary_search_latest_compatible(
            finishes, current_job.start, index - 1
        )

        profit_with_current = current_job.profit
        if compatible_index >= 0:
            profit_with_current += max_profits[compatible_index]

        profit_without_current = max_profits[index - 1]
        max_profits[index] = max(profit_with_current, profit_without_current)

    return max_profits[-1]


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