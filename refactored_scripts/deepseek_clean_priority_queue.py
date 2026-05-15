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
        
        priorities = priorities if priorities is not None else itertools.repeat(None)
        for item, priority in zip(items, priorities):
            self.push(item, priority=priority)

    def _insert_sorted(self, node: PriorityQueueNode) -> None:
        for index, current in enumerate(self._queue):
            if current.priority < node.priority:
                self._queue.insert(index, node)
                return
        self._queue.append(node)


if __name__ == "__main__":
    items = [5, 3, 9, 1, 7]
    print("Initial items:", items)
    pq = PriorityQueue(items)
    print("PriorityQueue after insertion:", pq)
    print("Pop items in order:")
    while pq.size() > 0:
        print(pq.pop())