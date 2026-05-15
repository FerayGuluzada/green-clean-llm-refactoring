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

class Fenwick_Tree:
    def __init__(self, freq):
        self.n = len(freq)
        self.bit_tree = [0] * (self.n + 1)
        self._build_tree(freq)
    
    def _build_tree(self, freq):
        """Builds the Fenwick tree from the initial frequency array."""
        for i, value in enumerate(freq):
            self._update(i, value)
    
    def _update(self, index, delta):
        """Updates the tree by adding delta at the given index."""
        i = index + 1
        while i <= self.n:
            self.bit_tree[i] += delta
            i += i & -i
    
    def _prefix_sum(self, index):
        """Returns the prefix sum up to the given index."""
        i = index + 1
        total = 0
        while i > 0:
            total += self.bit_tree[i]
            i -= i & -i
        return total
    
    def get_sum(self, i):
        """Returns sum of arr[0..index]."""
        return self._prefix_sum(i)
    
    def update_bit(self, i, v):
        """Updates the value at index i by adding v."""
        self._update(i, v)

if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    ft = Fenwick_Tree(arr)
    total = 0

    for _ in range(20):
        for i in range(len(arr)):
            ft.update_bit(i, i % 3 + 1)
        for i in range(len(arr)):
            total += ft.get_sum(i)

    print(total)