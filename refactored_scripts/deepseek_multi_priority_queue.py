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


class PriorityQueueNode:
    """A node holding data and its priority."""

    __slots__ = ('data', 'priority')

    def __init__(self, data: Any, priority: Any) -> None:
        self.data = data
        self.priority = priority

    def __repr__(self) -> str:
        return f"{self.data}: {self.priority}"


class PriorityQueue:
    """Priority queue backed by a sorted linear array."""

    def __init__(
        self,
        items: Iterable[Any] | None = None,
        priorities: Iterable[Any] | None = None,
    ) -> None:
        self._queue: list[PriorityQueueNode] = []
        if items is not None:
            self._initialize_queue(items, priorities)

    def __repr__(self) -> str:
        return f"PriorityQueue({self._queue!r})"

    def _initialize_queue(
        self,
        items: Iterable[Any],
        priorities: Iterable[Any] | None
    ) -> None:
        """Initialize queue with items and optional priorities."""
        if priorities is None:
            priorities = itertools.repeat(None)
        for item, priority in zip(items, priorities):
            self.push(item, priority)

    def size(self) -> int:
        """Return the number of elements in the queue."""
        return len(self._queue)

    def push(self, item: Any, priority: Any = None) -> None:
        """Insert an item with the given priority."""
        priority = item if priority is None else priority
        node = PriorityQueueNode(item, priority)
        self._insert_sorted(node)

    def _insert_sorted(self, node: PriorityQueueNode) -> None:
        """Insert node while maintaining sorted order by priority."""
        for idx, current in enumerate(self._queue):
            if current.priority < node.priority:
                self._queue.insert(idx, node)
                return
        self._queue.append(node)

    def pop(self) -> Any:
        """Remove and return the item with the lowest priority."""
        return self._queue.pop().data


if __name__ == "__main__":
    items = [5, 3, 9, 1, 7]
    print("Initial items:", items)
    pq = PriorityQueue(items)
    print("PriorityQueue after insertion:", pq)
    print("Pop items in order:")
    while pq.size() > 0:
        print(pq.pop())