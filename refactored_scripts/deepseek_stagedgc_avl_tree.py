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
        """
        Insert new key into tree.
        """
        if not self.node:
            self.node = TreeNode(key)
            self.node.left = AvlTree()
            self.node.right = AvlTree()
            self.height = 0
            self.balance = 0
        elif key < self.node.val:
            self.node.left.insert(key)
        elif key > self.node.val:
            self.node.right.insert(key)
        
        self._rebalance()

    def _rebalance(self):
        """
        Rebalance tree after insertion.
        """
        self._update_heights_and_balance()
        
        if self.balance > 1:
            self._handle_left_heavy()
        elif self.balance < -1:
            self._handle_right_heavy()

    def _update_heights_and_balance(self):
        """
        Update height and balance factor together.
        """
        if not self.node:
            self.height = -1
            self.balance = 0
            return
        
        left_height = self.node.left.height
        right_height = self.node.right.height
        
        self.height = 1 + max(left_height, right_height)
        self.balance = left_height - right_height

    def _handle_left_heavy(self):
        """
        Handle left-heavy tree (balance > 1).
        """
        if self.node.left.balance < 0:
            self.node.left._rotate_left()
            self._update_heights_and_balance()
        self._rotate_right()
        self._update_heights_and_balance()

    def _handle_right_heavy(self):
        """
        Handle right-heavy tree (balance < -1).
        """
        if self.node.right.balance > 0:
            self.node.right._rotate_right()
            self._update_heights_and_balance()
        self._rotate_left()
        self._update_heights_and_balance()

    def _rotate_right(self):
        """
        Right rotation.
        """
        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

        self._update_subtree_heights(old_root.left, new_root.right, self)

    def _rotate_left(self):
        """
        Left rotation.
        """
        new_root = self.node.right.node
        new_left_sub = new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

        self._update_subtree_heights(old_root.right, new_root.left, self)

    def _update_subtree_heights(self, subtree1, subtree2, current_tree):
        """
        Update heights for affected subtrees after rotation.
        """
        if subtree1:
            subtree1._update_heights_and_balance()
        if subtree2:
            subtree2._update_heights_and_balance()
        current_tree._update_heights_and_balance()

    def in_order_traverse(self):
        """
        In-order traversal of the tree.
        """
        if not self.node:
            return []
        
        return (self.node.left.in_order_traverse() + 
                [self.node.key] + 
                self.node.right.in_order_traverse())


if __name__ == "__main__":
    tree = AvlTree()

    values = [10, 20, 5, 4, 15, 25, 3]
    for val in values:
        tree.insert(val)

    print("In-order traversal:", tree.in_order_traverse())