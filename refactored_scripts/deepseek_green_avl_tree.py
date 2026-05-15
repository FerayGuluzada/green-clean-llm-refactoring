""" Imports TreeNodes"""

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.val = key
        self.left = None
        self.right = None


class AvlTree(object):
    """
    An avl tree.
    """

    def __init__(self):
        # Root node of the tree.
        self.node = None
        self.height = -1
        self.balance = 0

    def insert(self, key):
        """
        Insert new key into node
        """
        # Create new node
        node = TreeNode(key)
        if not self.node:
            self.node = node
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
        Rebalance tree after insertion
        """
        self._update_height()
        self._update_balance()

        if self.balance > 1:
            if self.node.left.balance < 0:
                self.node.left._rotate_left()
                self._update_height()
                self._update_balance()
            self._rotate_right()
            self._update_height()
            self._update_balance()
        elif self.balance < -1:
            if self.node.right.balance > 0:
                self.node.right._rotate_right()
                self._update_height()
                self._update_balance()
            self._rotate_left()
            self._update_height()
            self._update_balance()

    def _update_height(self):
        """
        Update tree height (non-recursive)
        """
        if self.node:
            left_height = self.node.left.height if self.node.left else -1
            right_height = self.node.right.height if self.node.right else -1
            self.height = 1 + max(left_height, right_height)
        else:
            self.height = -1

    def _update_balance(self):
        """
        Calculate tree balance factor (non-recursive)
        """
        if self.node:
            left_height = self.node.left.height if self.node.left else -1
            right_height = self.node.right.height if self.node.right else -1
            self.balance = left_height - right_height
        else:
            self.balance = 0

    def _rotate_right(self):
        """
        Right rotation
        """
        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

        # Update heights locally
        if old_root.left:
            old_root.left._update_height()
        if new_root.right:
            new_root.right._update_height()
        self._update_height()

    def _rotate_left(self):
        """
        Left rotation
        """
        new_root = self.node.right.node
        new_left_sub = new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

        # Update heights locally
        if old_root.right:
            old_root.right._update_height()
        if new_root.left:
            new_root.left._update_height()
        self._update_height()

    def in_order_traverse(self):
        """
        In-order traversal of the tree
        """
        result = []

        if not self.node:
            return result

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