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
        self.arr = freq
        self.n = len(freq)
        self.bit_tree = [0] * (self.n + 1)
        self._construct()
    
    def _to_bit_index(self, i):
        """Convert array index to BIT index (1-based)."""
        return i + 1
    
    def _next_index(self, i):
        """Get next index in BIT update traversal."""
        return i + (i & -i)
    
    def _parent_index(self, i):
        """Get parent index in BIT sum traversal."""
        return i & (i - 1)
    
    def get_sum(self, i):
        """
        Returns sum of arr[0..index]. This function assumes that the array is preprocessed and partial sums of array elements are stored in bit_tree[].
        """
        s = 0
        idx = self._to_bit_index(i)
        
        while idx > 0:
            s += self.bit_tree[idx]
            idx = self._parent_index(idx)
        return s
    
    def update(self, i, delta):
        """
        Updates a node in Binary Index Tree (bit_tree) at given index in bit_tree. The given value 'delta' is added to bit_tree[i] and all of its ancestors in tree.
        """
        idx = self._to_bit_index(i)
        
        while idx <= self.n:
            self.bit_tree[idx] += delta
            idx = self._next_index(idx)
    
    def _construct(self):
        """Constructs the Binary Indexed Tree for given array of size n."""
        for i in range(self.n):
            self.update(i, self.arr[i])

if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    ft = FenwickTree(arr)
    total = 0
    
    for _ in range(20):
        for i in range(len(arr)):
            ft.update(i, i % 3 + 1)
        for i in range(len(arr)):
            total += ft.get_sum(i)
    
    print(total)