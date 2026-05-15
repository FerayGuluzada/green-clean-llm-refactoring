"""KD-tree — a space-partitioning tree for k-dimensional points.

Supports efficient nearest-neighbour and range queries.

Inspired by PR #915 (gjones1077).
"""

from __future__ import annotations

import math
from typing import Any, Optional


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
        self._optimize_pivot(points, axis)
        
        mid = len(points) // 2
        self._partial_sort(points, axis, mid)
        
        return KDNode(
            point=points[mid],
            left=self._build(points[:mid], depth + 1),
            right=self._build(points[mid + 1:], depth + 1),
            axis=axis,
        )

    def _optimize_pivot(self, points: list[tuple[float, ...]], axis: int) -> None:
        """Use median-of-three pivot selection for better balance."""
        if len(points) <= 2:
            return

        indices = [0, len(points) // 2, -1]
        sample = [points[i][axis] for i in indices]
        
        # Sort indices by sample values
        sorted_indices = sorted(indices, key=lambda i: sample[indices.index(i)])
        pivot_idx = sorted_indices[1]
        
        # Move pivot to middle position
        if pivot_idx != len(points) // 2:
            points[pivot_idx], points[len(points) // 2] = \
                points[len(points) // 2], points[pivot_idx]

    def _partial_sort(self, points: list[tuple[float, ...]], axis: int, mid: int) -> None:
        """Sort halves separately for efficiency."""
        points[mid:] = sorted(points[mid:], key=lambda p: p[axis])
        points[:mid] = sorted(points[:mid], key=lambda p: p[axis])

    def nearest(self, target: tuple[float, ...]) -> tuple[float, ...]:
        """Return the point closest to *target*."""
        best = _SearchResult()
        self._nearest(self.root, target, best)
        return best.point

    def _nearest(self, node: Optional[KDNode], target: tuple[float, ...], 
                 best: _SearchResult) -> None:
        if node is None:
            return
        
        dist = self._squared_distance_with_early_exit(node.point, target, best.distance)
        
        if dist < best.distance:
            best.update(node.point, dist)
        
        self._search_subtrees(node, target, best)

    def _squared_distance_with_early_exit(self, point: tuple[float, ...], 
                                          target: tuple[float, ...], 
                                          cutoff: float) -> float:
        """Calculate squared distance with early exit if exceeding cutoff."""
        dist = 0.0
        for i in range(len(point)):
            diff = point[i] - target[i]
            dist += diff * diff
            if dist >= cutoff:
                break
        return dist

    def _search_subtrees(self, node: KDNode, target: tuple[float, ...], 
                        best: _SearchResult) -> None:
        """Search closer subtree first, then farther if needed."""
        axis = node.axis
        diff = target[axis] - node.point[axis]
        
        close, away = (node.left, node.right) if diff <= 0 else (node.right, node.left)
        
        self._nearest(close, target, best)
        
        # Only search farther subtree if it could contain a better point
        if diff * diff < best.distance:
            self._nearest(away, target, best)


class _SearchResult:
    """Helper class to track nearest neighbor search state."""
    __slots__ = ("point", "distance")
    
    def __init__(self) -> None:
        self.point: Optional[tuple[float, ...]] = None
        self.distance = math.inf
    
    def update(self, point: tuple[float, ...], distance: float) -> None:
        self.point = point
        self.distance = distance


if __name__ == "__main__":
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree = KDTree(points)
    target = (9, 2)
    print(tree.nearest(target))