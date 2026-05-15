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


def _binary_search(finishes: list[int], target_start: int, right: int) -> int:
    """Find the latest non-conflicting job before the current position.

    Args:
        finishes: Finish times of jobs sorted in ascending order.
        target_start: Start time of the current job.
        right: Rightmost index to search.

    Returns:
        Index of the latest compatible job, or -1 if none exists.
    """
    left = 0
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if finishes[mid] <= target_start:
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
    length = len(job)
    if length == 0:
        return 0

    job = sorted(job, key=lambda j: j.finish)
    finishes = [j.finish for j in job]

    table = [0] * length
    table[0] = job[0].profit

    for i in range(1, length):
        current_job = job[i]
        incl_prof = current_job.profit
        pos = _binary_search(finishes, current_job.start, i - 1)
        if pos != -1:
            incl_prof += table[pos]

        prev_profit = table[i - 1]
        table[i] = incl_prof if incl_prof > prev_profit else prev_profit

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