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
        elif key < self.node.val:
            self.node.left.insert(key)
        elif key > self.node.val:
            self.node.right.insert(key)
        
        self._rebalance()

    def _rebalance(self):
        """Rebalance tree after insertion."""
        self._update_properties(recursive=False)
        
        if self.balance > 1:
            self._handle_left_heavy()
        elif self.balance < -1:
            self._handle_right_heavy()

    def _handle_left_heavy(self):
        """Handle left-heavy tree cases."""
        if self.node.left.balance < 0:
            self.node.left._rotate_left()
            self._update_properties()
        self._rotate_right()
        self._update_properties()

    def _handle_right_heavy(self):
        """Handle right-heavy tree cases."""
        if self.node.right.balance > 0:
            self.node.right._rotate_right()
            self._update_properties()
        self._rotate_left()
        self._update_properties()

    def _update_properties(self, recursive=True):
        """Update height and balance factor."""
        self._update_height(recursive)
        self._update_balance(recursive)

    def _update_height(self, recursive=True):
        """Update tree height."""
        if not self.node:
            self.height = -1
            return

        if recursive:
            if self.node.left:
                self.node.left._update_height()
            if self.node.right:
                self.node.right._update_height()

        self.height = 1 + max(self.node.left.height, self.node.right.height)

    def _update_balance(self, recursive=True):
        """Calculate tree balance factor."""
        if not self.node:
            self.balance = 0
            return

        if recursive:
            if self.node.left:
                self.node.left._update_balance()
            if self.node.right:
                self.node.right._update_balance()

        self.balance = self.node.left.height - self.node.right.height

    def _rotate_right(self):
        """Perform right rotation."""
        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

    def _rotate_left(self):
        """Perform left rotation."""
        new_root = self.node.right.node
        new_left_sub = new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

    def in_order_traverse(self):
        """Return in-order traversal of the tree."""
        if not self.node:
            return []

        return (
            self.node.left.in_order_traverse() +
            [self.node.key] +
            self.node.right.in_order_traverse()
        )


if __name__ == "__main__":
    tree = AvlTree()
    values = [10, 20, 5, 4, 15, 25, 3]
    
    for val in values:
        tree.insert(val)

    print("In-order traversal:", tree.in_order_traverse())