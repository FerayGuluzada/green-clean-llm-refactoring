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

    __slots__ = ('data', 'priority')  # Reduces memory overhead and improves cache locality

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
        self._initialize_queue(items, priorities)

    def __repr__(self) -> str:
        return f"PriorityQueue({self._queue!r})"

    def size(self) -> int:
        return len(self._queue)

    def push(self, item: Any, priority: Any = None) -> None:
        priority = item if priority is None else priority
        node = PriorityQueueNode(item, priority)
        self._insert_sorted(node)

    def pop(self) -> Any:
        return self._queue.pop().data

    def _initialize_queue(
        self,
        items: Iterable[Any] | None,
        priorities: Iterable[Any] | None
    ) -> None:
        if items is None:
            return
        
        # Pre-allocate memory if possible
        if hasattr(items, '__len__'):
            self._queue = [None] * len(items)  # type: ignore
            self._queue.clear()  # Clear but keep allocated capacity
        
        priorities = priorities if priorities is not None else itertools.repeat(None)
        
        # Batch processing: collect all nodes first, then sort once
        nodes = []
        for item, priority in zip(items, priorities):
            nodes.append(PriorityQueueNode(item, item if priority is None else priority))
        
        if nodes:
            # Sort in descending order for O(1) pop from end
            nodes.sort(key=lambda x: x.priority, reverse=True)
            self._queue.extend(nodes)

    def _insert_sorted(self, node: PriorityQueueNode) -> None:
        """Insert node while maintaining descending order for O(1) pop."""
        # Use binary search for O(log n) insertion instead of linear scan
        low, high = 0, len(self._queue)
        while low < high:
            mid = (low + high) // 2
            if self._queue[mid].priority > node.priority:  # Compare with > for descending order
                low = mid + 1
            else:
                high = mid
        self._queue.insert(low, node)


if __name__ == "__main__":
    items = [5, 3, 9, 1, 7]
    print("Initial items:", items)
    pq = PriorityQueue(items)
    print("PriorityQueue after insertion:", pq)
    print("Pop items in order:")
    while pq.size() > 0:
        print(pq.pop())