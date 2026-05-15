"""
Fenwick Tree / Binary Indexed Tree

Consider we have an array arr[0 . . . n-1]. We would like to
1. Compute the sum of the first i elements.
2. Modify the value of a specified element of the array arr[i] = x where 0 <= i <= n-1.

A simple solution is to run a loop from 0 to i-1 and calculate the sum of the elements. To update a value, simply do arr[i] = x.
The first operation takes O(n) time and the second operation takes O(1) time.
Another simple solution is to create an extra array and store the sum of the first i-th elements at the i-th index in this new array.
The sum of a given range can now be calculated in O(1) time, but the update operation takes O(n) time now.
This works well if there are a large number of query operations but a very few number of update operations.


There are two solutions that can perform both the query and update operations in O(logn) time.
1. Fenwick Tree
2. Segment Tree

Compared with Segment Tree, Binary Indexed Tree requires less space and is easier to implement.
"""

class FenwickTree:
    def __init__(self, freq):
        self.n = len(freq)
        self.tree = [0] * (self.n + 1)
        self._build(freq)
    
    def _build(self, freq):
        """Build the Fenwick tree from initial frequencies."""
        for i, val in enumerate(freq):
            self._add(i, val)
    
    def _add(self, idx, delta):
        """Add delta to element at index idx."""
        idx += 1
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx
    
    def prefix_sum(self, idx):
        """Return sum of elements from index 0 to idx inclusive."""
        idx += 1
        result = 0
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & -idx
        return result
    
    def update(self, idx, new_val):
        """Update element at index idx to new_val."""
        current = self.range_sum(idx, idx)
        delta = new_val - current
        self._add(idx, delta)
    
    def range_sum(self, left, right):
        """Return sum of elements from index left to right inclusive."""
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    ft = FenwickTree(arr)
    total = 0

    for _ in range(20):
        for i in range(len(arr)):
            ft._add(i, i % 3 + 1)
        for i in range(len(arr)):
            total += ft.prefix_sum(i)

    print(total)