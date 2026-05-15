"""KD-tree — a space-partitioning tree for k-dimensional points.

Supports efficient nearest-neighbour and range queries.

Inspired by PR #915 (gjones1077).
"""

from __future__ import annotations

import math
from typing import Any


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
        self.root = self._build(points, 0)

    def _build(self, points: list[tuple[float, ...]], depth: int) -> KDNode | None:
        if not points:
            return None
        axis = depth % self.k
        points.sort(key=lambda p: p[axis])
        mid = len(points) >> 1  # Bit shift for faster division by 2
        return KDNode(
            point=points[mid],
            left=self._build(points[:mid], depth + 1),
            right=self._build(points[mid + 1:], depth + 1),
            axis=axis,
        )

    def nearest(self, target: tuple[float, ...]) -> tuple[float, ...]:
        """Return the point closest to *target*."""
        best_point: tuple[float, ...] | None = None
        best_dist = math.inf
        best_point, best_dist = self._nearest(self.root, target, best_point, best_dist)
        return best_point

    def _nearest(
        self,
        node: KDNode | None,
        target: tuple[float, ...],
        best_point: tuple[float, ...] | None,
        best_dist: float,
    ) -> tuple[tuple[float, ...] | None, float]:
        if node is None:
            return best_point, best_dist
            
        # Calculate squared distance without square root
        dist = _sq_dist(node.point, target)
        if dist < best_dist:
            best_point, best_dist = node.point, dist
            
        axis = node.axis
        diff = target[axis] - node.point[axis]
        close, away = (node.left, node.right) if diff <= 0 else (node.right, node.left)
        
        best_point, best_dist = self._nearest(close, target, best_point, best_dist)
        
        # Only search the away side if necessary
        if diff * diff < best_dist:
            best_point, best_dist = self._nearest(away, target, best_point, best_dist)
            
        return best_point, best_dist


def _sq_dist(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    # Use math.fsum for better numerical accuracy and performance
    return math.fsum((x - y) * (x - y) for x, y in zip(a, b))


if __name__ == "__main__":
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree = KDTree(points)
    target = (9, 2)
    print(tree.nearest(target))