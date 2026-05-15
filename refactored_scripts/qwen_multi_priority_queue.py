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

from typing import Any, Iterable, Optional


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
    
    __slots__ = ('priority_queue_list',)

    def __init__(
        self,
        items: Optional[Iterable[Any]] = None,
        priorities: Optional[Iterable[Any]] = None,
    ) -> None:
        self.priority_queue_list: list[PriorityQueueNode] = []
        
        if items is None:
            return
            
        # Use items as priorities if priorities not provided
        if priorities is None:
            for item in items:
                self.push(item, item)
        else:
            for item, priority in zip(items, priorities):
                self.push(item, priority)

    def __repr__(self) -> str:
        return f"PriorityQueue({self.priority_queue_list!r})"

    def size(self) -> int:
        return len(self.priority_queue_list)

    def push(self, item: Any, priority: Any = None) -> None:
        priority = item if priority is None else priority
        node = PriorityQueueNode(item, priority)
        
        # Find insertion point using binary search for better performance
        left, right = 0, len(self.priority_queue_list)
        while left < right:
            mid = (left + right) // 2
            if self.priority_queue_list[mid].priority < node.priority:
                right = mid
            else:
                left = mid + 1
                
        self.priority_queue_list.insert(left, node)

    def pop(self) -> Any:
        if not self.priority_queue_list:
            raise IndexError("pop from empty priority queue")
        return self.priority_queue_list.pop().data


if __name__ == "__main__":
    items = [5, 3, 9, 1, 7]
    print("Initial items:", items)
    pq = PriorityQueue(items)
    print("PriorityQueue after insertion:", pq)
    print("Pop items in order:")
    while pq.size() > 0:
        print(pq.pop())