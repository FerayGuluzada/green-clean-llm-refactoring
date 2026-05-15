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

        # Use local variables for speed
        data = self.data
        blocks = self.blocks
        bs = self.block_size
        
        for i, val in enumerate(data):
            blocks[i // bs] += val

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
        n = len(self.data)
        if index < 0 or index >= n:
            msg = f"index {index} out of range for length {n}"
            raise IndexError(msg)

        block = index // self.block_size
        old_val = self.data[index]
        self.blocks[block] += value - old_val
        self.data[index] = value

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
        n = len(self.data)
        if left < 0 or right >= n or left > right:
            msg = f"invalid range [{left}, {right}] for length {n}"
            raise IndexError(msg)

        data = self.data
        blocks = self.blocks
        bs = self.block_size
        
        block_left = left // bs
        block_right = right // bs

        if block_left == block_right:
            return self._sum_range(data, left, right)
        
        total: int | float = 0
        total += self._sum_range(data, left, (block_left + 1) * bs - 1)
        total += self._sum_blocks(blocks, block_left + 1, block_right - 1)
        total += self._sum_range(data, block_right * bs, right)
        
        return total
    
    def _sum_range(self, data: list[int | float], start: int, end: int) -> int | float:
        """Sum elements from start to end inclusive."""
        total: int | float = 0
        for i in range(start, end + 1):
            total += data[i]
        return total
    
    def _sum_blocks(self, blocks: list[int | float], start: int, end: int) -> int | float:
        """Sum blocks from start to end inclusive."""
        total: int | float = 0
        for b in range(start, end + 1):
            total += blocks[b]
        return total
    
if __name__ == "__main__":
    sd = SqrtDecomposition([1, 2, 3, 4, 5, 6, 7, 8, 9])

    print(sd.query(0, 8))
    print(sd.query(2, 5))

    sd.update(4, 10)

    print(sd.query(0, 8))