"""
Square Root (Sqrt) Decomposition

Divides an array into blocks of size √n to allow O(√n) range queries and
point updates — a simple alternative to segment trees for range-aggregate
problems.

Supports:
- **Range sum queries** in O(√n).
- **Point updates** in O(1).

Reference: https://cp-algorithms.com/data_structures/sqrt_decomposition.html

Complexity:
    Build: O(n)
    Query: O(√n)
    Update: O(1)
    Space: O(n)
"""

from __future__ import annotations

import math


class SqrtDecomposition:
    """Square root decomposition for range sum queries.

    Attributes:
        data: The underlying array.
        block_size: Size of each block (⌈√n⌉).
        blocks: Precomputed block sums.

    Examples:
        >>> sd = SqrtDecomposition([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> sd.query(0, 8)
        45
        >>> sd.query(2, 5)
        18
        >>> sd.update(4, 10)
        >>> sd.query(0, 8)
        50
    """

    def __init__(self, arr: list[int | float]) -> None:
        """Build the sqrt decomposition from *arr*.

        Args:
            arr: Input array of numbers.
        """
        self.data = list(arr)
        n = len(self.data)
        self.block_size = max(1, math.isqrt(n))
        num_blocks = (n + self.block_size - 1) // self.block_size
        self.blocks: list[int | float] = [0] * num_blocks

        for i, val in enumerate(self.data):
            self.blocks[i // self.block_size] += val

    def _validate_index(self, index: int) -> None:
        """Validate array index."""
        if index < 0 or index >= len(self.data):
            msg = f"index {index} out of range for length {len(self.data)}"
            raise IndexError(msg)

    def _validate_range(self, left: int, right: int) -> None:
        """Validate query range."""
        if left < 0 or right >= len(self.data) or left > right:
            msg = f"invalid range [{left}, {right}] for length {len(self.data)}"
            raise IndexError(msg)

    def update(self, index: int, value: int | float) -> None:
        """Set ```data[index]``` to *value* and update the block sum.

        Args:
            index: Array index to update.
            value: New value.

        Raises:
            IndexError: If *index* is out of range.

        Examples:
            >>> sd = SqrtDecomposition([1, 2, 3])
            >>> sd.update(1, 10)
            >>> sd.query(0, 2)
            14
        """
        self._validate_index(index)
        
        block = index // self.block_size
        self.blocks[block] += value - self.data[index]
        self.data[index] = value

    def _sum_range(self, start: int, end: int) -> int | float:
        """Sum elements from start to end inclusive."""
        return sum(self.data[i] for i in range(start, end + 1))

    def query(self, left: int, right: int) -> int | float:
        """Return the sum of elements from *left* to *right* inclusive.

        Args:
            left: Start index (inclusive).
            right: End index (inclusive).

        Returns:
            Sum of ```data[left..right]```.

        Raises:
            IndexError: If indices are out of range.

        Examples:
            >>> sd = SqrtDecomposition([1, 2, 3, 4, 5])
            >>> sd.query(1, 3)
            9
        """
        self._validate_range(left, right)

        block_left = left // self.block_size
        block_right = right // self.block_size

        if block_left == block_right:
            return self._sum_range(left, right)

        total: int | float = 0
        # Partial left block
        total += self._sum_range(left, (block_left + 1) * self.block_size - 1)
        # Full middle blocks
        total += sum(self.blocks[block_left + 1:block_right])
        # Partial right block
        total += self._sum_range(block_right * self.block_size, right)

        return total


if __name__ == "__main__":
    sd = SqrtDecomposition([1, 2, 3, 4, 5, 6, 7, 8, 9])

    print(sd.query(0, 8))
    print(sd.query(2, 5))

    sd.update(4, 10)

    print(sd.query(0, 8))