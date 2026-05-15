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
        data = list(arr)
        n = len(data)
        block_size = max(1, math.isqrt(n))
        num_blocks = (n + block_size - 1) // block_size
        blocks: list[int | float] = [0] * num_blocks

        for index, value in enumerate(data):
            blocks[index // block_size] += value

        self.data = data
        self.block_size = block_size
        self.blocks = blocks

    def _validate_index(self, index: int) -> None:
        if 0 <= index < len(self.data):
            return
        msg = f"index {index} out of range for length {len(self.data)}"
        raise IndexError(msg)

    def _validate_range(self, left: int, right: int) -> None:
        if 0 <= left <= right < len(self.data):
            return
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

        data = self.data
        old_value = data[index]
        data[index] = value
        self.blocks[index // self.block_size] += value - old_value

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

        data = self.data
        blocks = self.blocks
        block_size = self.block_size

        block_left = left // block_size
        block_right = right // block_size

        if block_left == block_right:
            # Same block — iterate directly
            total = 0
            for i in range(left, right + 1):
                total += data[i]
            return total

        total = 0

        left_block_end = (block_left + 1) * block_size
        for i in range(left, left_block_end):
            total += data[i]

        for block in range(block_left + 1, block_right):
            total += blocks[block]

        right_block_start = block_right * block_size
        for i in range(right_block_start, right + 1):
            total += data[i]

        return total


if __name__ == "__main__":
    sd = SqrtDecomposition([1, 2, 3, 4, 5, 6, 7, 8, 9])

    print(sd.query(0, 8))
    print(sd.query(2, 5))

    sd.update(4, 10)

    print(sd.query(0, 8))