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

import itertools
from typing import Any, Iterable
from bisect import bisect_left


class PriorityQueueNode:
    """A node holding data and its priority.

    Args:
        data: The stored value.
        priority: The priority of this node.
    """

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
        self._queue: list[PriorityQueueNode] = []
        self._init_queue(items, priorities)

    def __repr__(self) -> str:
        """Return a string representation of the priority queue.

        Returns:
            Formatted string.
        """
        return f"PriorityQueue({self._queue})"

    def size(self) -> int:
        """Return the number of elements in the queue.

        Returns:
            The queue size.
        """
        return len(self._queue)

    def _init_queue(self, items: Iterable[Any] | None, priorities: Iterable[Any] | None) -> None:
        """Initialize the priority queue with items and priorities.

        Args:
            items: Initial items to insert.
            priorities: Corresponding priorities; defaults to item values.
        """
        if items is None:
            return
        if priorities is None:
            priorities = itertools.repeat(None)
        for item, priority in zip(items, priorities):
            self.push(item, priority=priority)

    def push(self, item: Any, priority: Any = None) -> None:
        """Insert an item with the given priority.

        Args:
            item: The value to insert.
            priority: Priority value; defaults to the item itself.
        """
        priority = item if priority is None else priority
        node = PriorityQueueNode(item, priority)
        index = bisect_left([n.priority for n in self._queue], node.priority)
        self._queue.insert(index, node)

    def pop(self) -> Any:
        """Remove and return the item with the lowest priority.

        Returns:
            The data of the lowest-priority node.
        """
        return self._queue.pop(0).data


if __name__ == "__main__":
    items = [5, 3, 9, 1, 7]
    print("Initial items:", items)
    pq = PriorityQueue(items)
    print("PriorityQueue after insertion:", pq)
    print("Pop items in order:")
    while pq.size() > 0:
        print(pq.pop())