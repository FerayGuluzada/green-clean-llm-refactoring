"""
Union-Find (Disjoint Set) Data Structure

A Union-Find data structure supporting add, find (root), and unite operations.
Uses union by size and path compression for near-constant amortized time.

Reference: https://en.wikipedia.org/wiki/Disjoint-set_data_structure

Complexity:
    Time:  O(alpha(n)) amortized per operation (inverse Ackermann)
    Space: O(n)
"""

from __future__ import annotations


class Union:
    """A Union-Find (Disjoint Set) data structure.

    Supports adding elements, finding set representatives, and merging sets.
    Uses union by size and path compression for near-constant amortized time.

    Examples:
        >>> uf = Union()
        >>> uf.add(1); uf.add(2); uf.add(3)
        >>> uf.unite(1, 2)
        >>> uf.root(1) == uf.root(2)
        True
        >>> uf.root(1) == uf.root(3)
        False
    """

    def __init__(self) -> None:
        self._data: dict[object, dict[str, object | int]] = {}

    def add(self, element: object) -> None:
        """Add a new singleton set containing the given element.

        Args:
            element: The element to add.
        """
        self._data[element] = {"parent": element, "size": 1}

    def _find_root(self, element: object) -> object:
        """Find the root representative of the set containing element.

        Args:
            element: The element whose root to find.

        Returns:
            The root representative of the element's set.
        """
        if self._data[element]["parent"]!= element:
            self._data[element]["parent"] = self._find_root(self._data[element]["parent"])
        return self._data[element]["parent"]

    def unite(self, element1: object, element2: object) -> None:
        """Merge the sets containing the two elements.

        Args:
            element1: An element in the first set.
            element2: An element in the second set.
        """
        root1, root2 = self._find_root(element1), self._find_root(element2)
        if root1 == root2:
            return
        if self._data[root1]["size"] > self._data[root2]["size"]:
            root1, root2 = root2, root1
        self._data[root1]["parent"] = root2
        self._data[root2]["size"] += self._data[root1]["size"]

    def root(self, element: object) -> object:
        """Find the root representative of the set containing element.

        Args:
            element: The element whose root to find.

        Returns:
            The root representative of the element's set.
        """
        return self._find_root(element)


if __name__ == "__main__":
    uf = Union()
    
    uf.add(1)
    uf.add(2)
    uf.add(3)

    uf.unite(1, 2)

    print("Root of 1:", uf.root(1))
    print("Root of 2:", uf.root(2))
    print("Root of 3:", uf.root(3))

    uf.unite(2, 3)
    print("After uniting 2 and 3:")
    print("Root of 1:", uf.root(1))
    print("Root of 2:", uf.root(2))
    print("Root of 3:", uf.root(3))