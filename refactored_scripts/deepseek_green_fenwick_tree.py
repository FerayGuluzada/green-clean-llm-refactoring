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

class Fenwick_Tree(object):
    def __init__(self, freq):
        self.arr = freq
        self.n = len(freq)
        self.bit_tree = [0] * (self.n + 1)
        self._construct()
        
    def get_sum(self, i):
        """
        Returns sum of arr[0..index]. This function assumes that the array is preprocessed and partial sums of array elements are stored in bit_tree[]. 
        """
        s = 0
        i += 1  # index in bit_tree[] is 1 more than the index in arr[]
        
        # Traverse ancestors of bit_tree[index]
        while i > 0:
            s += self.bit_tree[i]
            i &= i - 1  # equivalent to i -= i & (-i) but uses bitwise AND
        return s
      
    def update_bit(self, i, v):
        """
        Updates a node in Binary Index Tree (bit_tree) at given index in bit_tree. The given value 'val' is added to bit_tree[i] and all of its ancestors in tree. 
        """
        i += 1  # index in bit_tree[] is 1 more than the index in arr[]
        
        # Traverse all ancestors and add 'v'
        while i <= self.n:
            self.bit_tree[i] += v
            i += i & -i  # keep original for clarity, but ensure it's stored locally
      
    def _construct(self):
        """
        Constructs the Binary Indexed Tree for given array of size n.
        """
        # Store the actual values in bit_tree[] using update()
        for i in range(self.n):
            self.update_bit(i, self.arr[i])

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