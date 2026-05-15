"""KD-tree — a space-partitioning tree for k-dimensional points.

Supports efficient nearest-neighbour and range queries.

Inspired by PR #915 (gjones1077).
"""

from __future__ import annotations


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
        points.sort(key=lambda point: point[axis])
        mid = len(points) // 2

        return KDNode(
            point=points[mid],
            left=self._build(points[:mid], depth + 1),
            right=self._build(points[mid + 1 :], depth + 1),
            axis=axis,
        )

    def nearest(self, target: tuple[float, ...]) -> tuple[float, ...]:
        """Return the point closest to *target*."""
        root = self.root
        if root is None:
            return ()

        best_point = root.point
        best_dist = _sq_dist(best_point, target)
        stack: list[tuple[KDNode | None, bool]] = [(root, False)]

        while stack:
            node, revisit = stack.pop()
            if node is None:
                continue

            if revisit:
                diff = target[node.axis] - node.point[node.axis]
                if diff * diff < best_dist:
                    far_branch = node.right if diff <= 0 else node.left
                    if far_branch is not None:
                        stack.append((far_branch, False))
                continue

            node_point = node.point
            node_dist = _sq_dist(node_point, target)
            if node_dist < best_dist:
                best_point = node_point
                best_dist = node_dist

            diff = target[node.axis] - node_point[node.axis]
            near_branch = node.left if diff <= 0 else node.right

            stack.append((node, True))
            if near_branch is not None:
                stack.append((near_branch, False))

        return best_point


def _sq_dist(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    total = 0.0
    for x, y in zip(a, b):
        diff = x - y
        total += diff * diff
    return total


if __name__ == "__main__":
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree = KDTree(points)
    target = (9, 2)
    print(tree.nearest(target))