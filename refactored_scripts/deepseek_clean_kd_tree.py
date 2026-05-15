"""KD-tree — a space-partitioning tree for k-dimensional points.

Supports efficient nearest-neighbour and range queries.

Inspired by PR #915 (gjones1077).
"""

from __future__ import annotations

import math
from typing import Any, NamedTuple


class KDNode:
    """A single node in a KD-tree."""

    __slots__ = ("point", "left", "right", "axis")

    def __init__(
        self,
        point: tuple[float, ...],
        left: KDNode | None = None,
        right: KDNode | None = None,
        axis: int = 0,
    ) -> None:
        self.point = point
        self.left = left
        self.right = right
        self.axis = axis


class _BestCandidate(NamedTuple):
    """Container for nearest neighbor search result."""
    point: tuple[float, ...] | None
    distance: float = math.inf


class KDTree:
    """A k-dimensional tree built from a list of points.

    >>> tree = KDTree([(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)])
    >>> tree.nearest((9, 2))
    (8, 1)
    """

    def __init__(self, points: list[tuple[float, ...]]) -> None:
        self.k = len(points[0]) if points else 0
        self.root = self._build(list(points), depth=0)

    def _build(self, points: list[tuple[float, ...]], depth: int) -> KDNode | None:
        if not points:
            return None
        
        axis = depth % self.k
        points.sort(key=lambda p: p[axis])
        mid = len(points) // 2
        
        return KDNode(
            point=points[mid],
            left=self._build(points[:mid], depth + 1),
            right=self._build(points[mid + 1:], depth + 1),
            axis=axis,
        )

    def nearest(self, target: tuple[float, ...]) -> tuple[float, ...]:
        """Return the point closest to *target*."""
        best = _BestCandidate()
        self._nearest(self.root, target, best)
        return best.point

    def _nearest(
        self,
        node: KDNode | None,
        target: tuple[float, ...],
        best: _BestCandidate,
    ) -> _BestCandidate:
        if node is None:
            return best
        
        dist = _sq_dist(node.point, target)
        if dist < best.distance:
            best = _BestCandidate(node.point, dist)
        
        axis = node.axis
        diff = target[axis] - node.point[axis]
        
        # Determine which child is closer to target
        close = node.left if diff <= 0 else node.right
        away = node.right if diff <= 0 else node.left
        
        best = self._nearest(close, target, best)
        
        # Check if we need to search the farther child
        if diff * diff < best.distance:
            best = self._nearest(away, target, best)
        
        return best


def _sq_dist(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    """Calculate squared Euclidean distance between two points."""
    return sum((x - y) ** 2 for x, y in zip(a, b))


if __name__ == "__main__":
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree = KDTree(points)
    target = (9, 2)
    print(tree.nearest(target))