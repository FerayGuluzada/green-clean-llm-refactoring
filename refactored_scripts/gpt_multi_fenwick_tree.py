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

    def get_sum(self, bit_tree, i):
        """
             Returns sum of arr[0..index]. This function assumes that the array is preprocessed and partial sums of array elements are stored in bit_tree[].
        """
        total = 0
        i += 1

        # Traverse ancestors of bit_tree[index]
        while i:
            # Add current element of bit_tree to sum
            total += bit_tree[i]

            # Move index to parent node in getSum View
            i -= i & -i
        return total

    def update_bit(self, bit_tree, i, v):
        """
             Updates a node in Binary Index Tree (bit_tree) at given index in bit_tree. The given value 'val' is added to bit_tree[i] and all of its ancestors in tree.
        """
        i += 1
        n = self.n

        # Traverse all ancestors and add 'val'
        while i <= n:
            # Add 'val' to current node of bit_tree
            bit_tree[i] += v

            # Update index to that of parent in update View
            i += i & -i

    def construct(self):
        """
             Constructs and returns a Binary Indexed Tree for given array of size n.
        """
        n = self.n
        arr = self.arr
        bit_tree = [0] * (n + 1)

        # Build BIT in linear time
        for i, value in enumerate(arr, 1):
            bit_tree[i] += value
            parent = i + (i & -i)
            if parent <= n:
                bit_tree[parent] += bit_tree[i]

        return bit_tree


if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    ft = Fenwick_Tree(arr)
    bit_tree = ft.construct()

    total = 0
    arr_len = len(arr)
    update_bit = ft.update_bit
    get_sum = ft.get_sum

    for _ in range(20):
        for i in range(arr_len):
            update_bit(bit_tree, i, i % 3 + 1)
        for i in range(arr_len):
            total += get_sum(bit_tree, i)

    print(total)