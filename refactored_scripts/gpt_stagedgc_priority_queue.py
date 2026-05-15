"""
Priority Queue (Linear Array)

A priority queue implementation using a sorted linear array. Elements
are inserted in order so that extraction of the minimum is O(1).

Reference: https://en.wikipedia.org/wiki/Priority_queue

Complexity:
    Time:  O(n) for push, O(1) for pop
    Space: O(n)
"""

from __future__ import annotations

from bisect import bisect_left
from typing import Any, Iterable


class PriorityQueueNode:
    """A node holding data and its priority.

    Args:
        data: The stored value.
        priority: The priority of this node.
    """

    __slots__ = ("data", "priority")

    def __init__(self, data: Any, priority: Any) -> None:
        self.data = data
        self.priority = priority

    def __repr__(self) -> str:
        """Return a string representation of the node.

        Returns:
            Formatted string with data and priority.
        """
        return f"{self.data}: {self.priority}"


class PriorityQueue:
    """Priority queue backed by a sorted linear array.

    Examples:
        >>> pq = PriorityQueue([3, 1, 2])
        >>> pq.pop()
        1
        >>> pq.size()
        2
    """

    __slots__ = ("priority_queue_list", "_priorities")

    def __init__(
        self,
        items: Iterable[Any] | None = None,
        priorities: Iterable[Any] | None = None,
    ) -> None:
        """Create a priority queue, optionally from items and priorities.

        Args:
            items: Initial items to insert.
            priorities: Corresponding priorities; defaults to item values.
        """
        self.priority_queue_list: list[PriorityQueueNode] = []
        self._priorities: list[Any] = []

        if items is None:
            return

        pairs = self._build_pairs(items, priorities)
        if not pairs:
            return

        pairs.sort(key=lambda pair: pair[1], reverse=True)
        self.priority_queue_list = [
            PriorityQueueNode(item, priority) for item, priority in pairs
        ]
        self._priorities = [-priority for _, priority in pairs]

    @staticmethod
    def _resolve_priority(item: Any, priority: Any) -> Any:
        return item if priority is None else priority

    @classmethod
    def _build_pairs(
        cls,
        items: Iterable[Any],
        priorities: Iterable[Any] | None,
    ) -> list[tuple[Any, Any]]:
        if priorities is None:
            return [(item, item) for item in items]
        return [
            (item, cls._resolve_priority(item, priority))
            for item, priority in zip(items, priorities)
        ]

    def __repr__(self) -> str:
        """Return a string representation of the priority queue.

        Returns:
            Formatted string.
        """
        return f"PriorityQueue({self.priority_queue_list!r})"

    def size(self) -> int:
        """Return the number of elements in the queue.

        Returns:
            The queue size.
        """
        return len(self.priority_queue_list)

    def push(self, item: Any, priority: Any = None) -> None:
        """Insert an item with the given priority.

        Args:
            item: The value to insert.
            priority: Priority value; defaults to the item itself.
        """
        resolved_priority = self._resolve_priority(item, priority)
        negated_priority = -resolved_priority
        index = bisect_left(self._priorities, negated_priority)
        self._priorities.insert(index, negated_priority)
        self.priority_queue_list.insert(index, PriorityQueueNode(item, resolved_priority))

    def pop(self) -> Any:
        """Remove and return the item with the lowest priority.

        Returns:
            The data of the lowest-priority node.
        """
        self._priorities.pop()
        return self.priority_queue_list.pop().data


if __name__ == "__main__":
    items = [5, 3, 9, 1, 7]
    print("Initial items:", items)
    pq = PriorityQueue(items)
    print("PriorityQueue after insertion:", pq)
    print("Pop items in order:")
    while pq.size() > 0:
        print(pq.pop())