""" Imports TreeNodes"""


class TreeNode:
    def __init__(self, key):
        self.key = key
        self.val = key
        self.left = None
        self.right = None


class AvlTree:
    """
    An AVL tree implementation.
    """

    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

    def insert(self, key):
        """Insert new key into tree."""
        if not self.node:
            self.node = TreeNode(key)
            self.node.left = AvlTree()
            self.node.right = AvlTree()
            self.height = 0
            self.balance = 0
            return
        
        if key < self.node.val:
            self.node.left.insert(key)
        elif key > self.node.val:
            self.node.right.insert(key)
        else:
            return  # Duplicate key, no insertion needed
        
        self._rebalance()

    def _rebalance(self):
        """Rebalance tree after insertion."""
        # Update height and balance for current node only
        self._update_local_properties()
        
        if self.balance > 1:
            self._handle_left_heavy()
        elif self.balance < -1:
            self._handle_right_heavy()

    def _handle_left_heavy(self):
        """Handle left-heavy tree cases."""
        if self.node.left.balance < 0:
            self.node.left._rotate_left()
            # Only update affected nodes after rotation
            self.node.left._update_local_properties()
        self._rotate_right()
        self._update_local_properties()

    def _handle_right_heavy(self):
        """Handle right-heavy tree cases."""
        if self.node.right.balance > 0:
            self.node.right._rotate_right()
            # Only update affected nodes after rotation
            self.node.right._update_local_properties()
        self._rotate_left()
        self._update_local_properties()

    def _update_local_properties(self):
        """Update height and balance factor for current node only."""
        if not self.node:
            self.height = -1
            self.balance = 0
            return
        
        left_height = self.node.left.height if self.node.left else -1
        right_height = self.node.right.height if self.node.right else -1
        
        self.height = 1 + max(left_height, right_height)
        self.balance = left_height - right_height

    def _rotate_right(self):
        """Perform right rotation."""
        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root
        
        # Update heights for affected subtrees
        if old_root.left:
            old_root.left._update_local_properties()
        if new_root.right:
            new_root.right._update_local_properties()

    def _rotate_left(self):
        """Perform left rotation."""
        new_root = self.node.right.node
        new_left_sub = new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root
        
        # Update heights for affected subtrees
        if old_root.right:
            old_root.right._update_local_properties()
        if new_root.left:
            new_root.left._update_local_properties()

    def in_order_traverse(self):
        """Return in-order traversal of the tree."""
        if not self.node:
            return []

        # Pre-allocate list and use extend for better performance
        result = []
        result.extend(self.node.left.in_order_traverse())
        result.append(self.node.key)
        result.extend(self.node.right.in_order_traverse())
        return result


if __name__ == "__main__":
    tree = AvlTree()
    values = [10, 20, 5, 4, 15, 25, 3]
    
    for val in values:
        tree.insert(val)

    print("In-order traversal:", tree.in_order_traverse())