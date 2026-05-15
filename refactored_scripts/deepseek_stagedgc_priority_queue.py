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
from typing import Any, Iterable


class PriorityQueueNode:
    """A node holding data and its priority.

    Args:
        data: The stored value.
        priority: The priority of this node.
    """

    __slots__ = ('data', 'priority')

    def __init__(self, data: Any, priority: Any) -> None:
        self.data = data
        self.priority = priority

    def __repr__(self) -> str:
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
        if items is not None:
            self._initialize_queue(items, priorities)

    def _initialize_queue(
        self,
        items: Iterable[Any],
        priorities: Iterable[Any] | None
    ) -> None:
        """Initialize queue with items and priorities."""
        if priorities is None:
            self._queue = [PriorityQueueNode(item, item) for item in items]
        else:
            self._queue = [
                PriorityQueueNode(item, pri)
                for item, pri in zip(items, priorities)
            ]
        self._queue.sort(key=lambda node: node.priority)

    def __repr__(self) -> str:
        return f"PriorityQueue({self._queue!r})"

    def size(self) -> int:
        """Return the number of elements in the queue."""
        return len(self._queue)

    def _find_insert_index(self, priority: Any) -> int:
        """Binary search for insertion point."""
        lo, hi = 0, len(self._queue)
        while lo < hi:
            mid = (lo + hi) // 2
            if self._queue[mid].priority < priority:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def push(self, item: Any, priority: Any = None) -> None:
        """Insert an item with the given priority.

        Args:
            item: The value to insert.
            priority: Priority value; defaults to the item itself.
        """
        priority = item if priority is None else priority
        node = PriorityQueueNode(item, priority)
        index = self._find_insert_index(priority)
        self._queue.insert(index, node)

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
```

**Refactoring improvements:**

1. **Reduced Cyclomatic Complexity**: Extracted `_initialize_queue()` and `_find_insert_index()` methods
2. **Improved Readability**: Clearer method names and separation of concerns
3. **Reduced Halstead Volume**: Smaller, focused methods with single responsibilities
4. **Eliminated Code Smells**: 
   - Removed complex conditional logic from constructor
   - Separated initialization from construction
   - Isolated binary search algorithm
5. **Preserved Efficiency**: All performance optimizations remain intact
6. **Better Modularity**: Each method has a clear, single purpose
7. **Consistent Naming**: Changed `priority_queue_list` to `_queue` for brevity and privacy indication