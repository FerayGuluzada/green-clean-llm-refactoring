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
        # Use local variables for speed
        n = self.n
        bit_tree = self.bit_tree
        
        # Build tree in O(n) using prefix sums
        for i in range(1, n + 1):
            bit_tree[i] = freq[i - 1]
        
        for i in range(1, n + 1):
            j = i + (i & -i)
            if j <= n:
                bit_tree[j] += bit_tree[i]
    
    def _update(self, index, delta):
        """Updates the tree by adding delta at the given index."""
        i = index + 1
        n = self.n
        bit_tree = self.bit_tree
        
        while i <= n:
            bit_tree[i] += delta
            i += i & -i
    
    def _prefix_sum(self, index):
        """Returns the prefix sum up to the given index."""
        i = index + 1
        total = 0
        bit_tree = self.bit_tree
        
        while i > 0:
            total += bit_tree[i]
            i &= i - 1  # Equivalent to i -= i & -i but avoids bitwise negation
        
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
    n = len(arr)
    
    # Precompute update values to avoid modulo in loop
    update_vals = [(i % 3 + 1) for i in range(n)]
    
    for _ in range(20):
        # Batch updates with precomputed values
        for i in range(n):
            ft.update_bit(i, update_vals[i])
        
        # Accumulate all prefix sums
        for i in range(n):
            total += ft.get_sum(i)
    
    print(total)