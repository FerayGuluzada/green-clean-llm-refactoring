"""
Fenwick Tree / Binary Indexed Tree

Consider we have an array arr[0... n-1]. We would like to
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
        self.arr = freq
        self.n = len(freq)

    def _get_parent(self, i):
        """Returns the parent index in the Fenwick Tree."""
        return i - (i & -i)

    def _get_sum(self, bit_tree, i):
        """Returns sum of arr[0..index]."""
        s = 0
        i += 1
        while i > 0:
            s += bit_tree[i]
            i = self._get_parent(i)
        return s

    def _update_bit(self, bit_tree, i, v):
        """Updates a node in Binary Index Tree (bit_tree) at given index in bit_tree."""
        i += 1
        while i <= self.n:
            bit_tree[i] += v
            i += i & -i

    def construct(self):
        """Constructs and returns a Binary Indexed Tree for given array of size n."""
        bit_tree = [0] * (self.n + 1)
        for i, val in enumerate(self.arr):
            self._update_bit(bit_tree, i, val)
        return bit_tree

    def query(self, bit_tree, i):
        """Returns the sum of the first i elements."""
        return self._get_sum(bit_tree, i)

    def update(self, bit_tree, i, v):
        """Updates the value of a specified element of the array."""
        self._update_bit(bit_tree, i, v)

if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    ft = FenwickTree(arr)
    bit_tree = ft.construct()

    total = 0

    for _ in range(20):
        for i in range(len(arr)):
            ft.update(bit_tree, i, i % 3 + 1)
        for i in range(len(arr)):
            total += ft.query(bit_tree, i)

    print(total)