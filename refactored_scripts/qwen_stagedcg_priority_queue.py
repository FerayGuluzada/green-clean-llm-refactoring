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
        return "{}: {}".format(self.data, self.priority)


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
        self.priority_queue_list: list[PriorityQueueNode] = []
        if items is None:
            return
        if priorities is None:
            priorities = itertools.repeat(None)
        # Pre-allocate list size when possible to reduce dynamic resizing
        items_list = list(items)
        self.priority_queue_list = [None] * len(items_list)
        
        # Build all nodes first
        nodes = []
        for item, priority in zip(items_list, priorities):
            if priority is None:
                priority = item
            nodes.append(PriorityQueueNode(item, priority))
        
        # Sort nodes by priority
        nodes.sort(key=lambda x: x.priority)
        
        # Place sorted nodes in the list
        self.priority_queue_list[:] = nodes

    def __repr__(self) -> str:
        """Return a string representation of the priority queue.

        Returns:
            Formatted string.
        """
        return "PriorityQueue({!r})".format(self.priority_queue_list)

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
        if priority is None:
            priority = item
        node = PriorityQueueNode(item, priority)
        
        # Use binary search for faster insertion point finding
        left, right = 0, len(self.priority_queue_list)
        while left < right:
            mid = (left + right) // 2
            if self.priority_queue_list[mid].priority > node.priority:
                right = mid
            else:
                left = mid + 1
        
        self.priority_queue_list.insert(left, node)

    def pop(self) -> Any:
        """Remove and return the item with the lowest priority.

        Returns:
            The data of the lowest-priority node.
        """
        if not self.priority_queue_list:
            raise IndexError("pop from empty priority queue")
        return self.priority_queue_list.pop(0).data


if __name__ == "__main__":
    items = [5, 3, 9, 1, 7]
    print("Initial items:", items)
    pq = PriorityQueue(items)
    print("PriorityQueue after insertion:", pq)
    print("Pop items in order:")
    while pq.size() > 0:
        print(pq.pop())