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
        self.block_size = max(1, math.isqrt(len(self.data)))
        self.blocks = self._calculate_block_sums()

    def _calculate_block_sums(self) -> list[int | float]:
        """Calculate the sum of each block."""
        num_blocks = (len(self.data) + self.block_size - 1) // self.block_size
        return [self._block_sum(i) for i in range(num_blocks)]

    def _block_sum(self, block_index: int) -> int | float:
        """Calculate the sum of a block."""
        start = block_index * self.block_size
        end = min((block_index + 1) * self.block_size, len(self.data))
        return sum(self.data[start:end])

    def _update_block_sum(self, block_index: int) -> None:
        """Update the sum of a block."""
        self.blocks[block_index] = self._block_sum(block_index)

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
        if not (0 <= index < len(self.data)):
            msg = f"index {index} out of range for length {len(self.data)}"
            raise IndexError(msg)

        block_index = index // self.block_size
        self.data[index] = value
        self._update_block_sum(block_index)

    def _query_block(self, block_index: int, left: int, right: int) -> int | float:
        """Query a block."""
        start = max(left, block_index * self.block_size)
        end = min(right + 1, (block_index + 1) * self.block_size)
        return sum(self.data[start:end])

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
        if not (0 <= left <= right < len(self.data)):
            msg = f"invalid range [{left}, {right}] for length {len(self.data)}"
            raise IndexError(msg)

        block_left = left // self.block_size
        block_right = right // self.block_size

        if block_left == block_right:
            # Same block — iterate directly
            return self._query_block(block_left, left, right)
        else:
            # Partial left block
            total = self._query_block(block_left, left, right)
            # Full middle blocks
            total += sum(self.blocks[block_left + 1:block_right])
            # Partial right block
            total += self._query_block(block_right, left, right)
            return total

if __name__ == "__main__":
    sd = SqrtDecomposition([1, 2, 3, 4, 5, 6, 7, 8, 9])

    print(sd.query(0, 8))
    print(sd.query(2, 5))

    sd.update(4, 10)

    print(sd.query(0, 8))