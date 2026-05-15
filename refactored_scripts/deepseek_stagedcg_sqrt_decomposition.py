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
        self.blocks: list[int | float] = [0] * ((n + self.block_size - 1) // self.block_size)
        self._build_blocks()

    def _build_blocks(self) -> None:
        """Initialize block sums."""
        # Use local variables for speed
        data = self.data
        blocks = self.blocks
        block_size = self.block_size
        
        for i, val in enumerate(data):
            blocks[i // block_size] += val

    def _validate_index(self, index: int) -> None:
        """Raise IndexError if index is invalid."""
        if index < 0 or index >= len(self.data):
            msg = f"index {index} out of range for length {len(self.data)}"
            raise IndexError(msg)

    def _validate_range(self, left: int, right: int) -> None:
        """Raise IndexError if range is invalid."""
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
        old_value = self.data[index]
        self.blocks[block] += value - old_value
        self.data[index] = value

    def _sum_range_direct(self, left: int, right: int) -> int | float:
        """Sum elements within a single block."""
        # Use built-in sum with slice for better performance
        return sum(self.data[left:right + 1])

    def _sum_partial_block(self, start: int, end: int) -> int | float:
        """Sum elements from start to end-1."""
        # Use built-in sum with slice for better performance
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
        self._validate_range(left, right)
        
        block_left = left // self.block_size
        block_right = right // self.block_size

        if block_left == block_right:
            return self._sum_range_direct(left, right)

        total: int | float = 0
        block_size = self.block_size
        data = self.data
        blocks = self.blocks
        
        # Partial left block
        left_end = (block_left + 1) * block_size
        total += sum(data[left:left_end])
        
        # Full middle blocks
        total += sum(blocks[b] for b in range(block_left + 1, block_right))
        
        # Partial right block
        right_start = block_right * block_size
        total += sum(data[right_start:right + 1])

        return total
    
if __name__ == "__main__":
    sd = SqrtDecomposition([1, 2, 3, 4, 5, 6, 7, 8, 9])

    print(sd.query(0, 8))
    print(sd.query(2, 5))

    sd.update(4, 10)

    print(sd.query(0, 8))