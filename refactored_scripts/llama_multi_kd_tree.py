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
        point: tuple[float,...],
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

    def __init__(self, points: list[tuple[float,...]]) -> None:
        self.k = len(points[0]) if points else 0
        self.root = self._build(points, 0)

    def _build(self, points: list[tuple[float,...]], depth: int) -> KDNode | None:
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

    def nearest(self, target: tuple[float,...]) -> tuple[float,...]:
        """Return the point closest to *target*."""
        return self._nearest(self.root, target, [None, math.inf])[0]

    def _nearest(
        self,
        node: KDNode | None,
        target: tuple[float,...],
        best: list[Any],
    ) -> list[Any]:
        if node is None:
            return best
        dist = self._sq_dist(node.point, target)
        if dist < best[1]:
            best[0], best[1] = node.point, dist
        axis = node.axis
        diff = target[axis] - node.point[axis]
        close, away = (node.left, node.right) if diff <= 0 else (node.right, node.left)
        best = self._nearest(close, target, best)
        if diff * diff < best[1]:
            best = self._nearest(away, target, best)
        return best

    @staticmethod
    def _sq_dist(a: tuple[float,...], b: tuple[float,...]) -> float:
        return sum((x - y) ** 2 for x, y in zip(a, b))


if __name__ == "__main__":
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree = KDTree(points)
    target = (9, 2)
    print(tree.nearest(target))