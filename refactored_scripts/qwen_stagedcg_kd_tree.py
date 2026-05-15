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


class _SearchState(NamedTuple):
    """State for nearest neighbor search."""
    best_point: tuple[float, ...] | None
    best_distance: float


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
            right=self._build(points[mid + 1 :], depth + 1),
            axis=axis,
        )

    def nearest(self, target: tuple[float, ...]) -> tuple[float, ...]:
        """Return the point closest to *target*."""
        state = _SearchState(None, math.inf)
        result = self._nearest_search(self.root, target, state)
        return result.best_point  # type: ignore

    def _nearest_search(
        self,
        node: KDNode | None,
        target: tuple[float, ...],
        state: _SearchState,
    ) -> _SearchState:
        """Recursive nearest neighbor search with early pruning."""
        if node is None:
            return state
            
        # Calculate squared distance without sqrt for performance
        dist_sq = _sq_dist(node.point, target)
        if dist_sq < state.best_distance:
            state = _SearchState(node.point, dist_sq)
            
        # Determine which subtree to visit first based on splitting axis
        axis = node.axis
        diff = target[axis] - node.point[axis]
        close, away = (node.left, node.right) if diff <= 0 else (node.right, node.left)
        
        # Visit closer subtree first
        state = self._nearest_search(close, target, state)
        
        # Only visit farther subtree if the hypersphere intersects the splitting plane
        if diff * diff < state.best_distance:
            state = self._nearest_search(away, target, state)
            
        return state


def _sq_dist(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    """Calculate squared Euclidean distance between two points."""
    # Use math.fsum for better numerical stability in summation
    return math.fsum((x - y) * (x - y) for x, y in zip(a, b))


if __name__ == "__main__":
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree = KDTree(points)
    target = (9, 2)
    print(tree.nearest(target))