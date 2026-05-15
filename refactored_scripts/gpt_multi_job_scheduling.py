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


def _latest_compatible_index(finish_times: list[int], jobs: list[Job], index: int) -> int:
    """Find the latest non-conflicting job before index.

    Args:
        finish_times: Finish times of jobs sorted in ascending order.
        jobs: List of jobs sorted by finish time.
        index: Index of the current job.

    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    left = 0
    right = index - 1
    target_start = jobs[index].start
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if finish_times[mid] <= target_start:
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    return result


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
    length = len(jobs)
    finish_times = [current_job.finish for current_job in jobs]
    table = [0] * length
    table[0] = jobs[0].profit

    for i in range(1, length):
        include_profit = jobs[i].profit
        compatible_index = _latest_compatible_index(finish_times, jobs, i)
        if compatible_index >= 0:
            include_profit += table[compatible_index]
        table[i] = max(include_profit, table[i - 1])

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