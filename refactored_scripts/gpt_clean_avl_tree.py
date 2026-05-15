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
        if not self.node:
            self._initialize_node(key)
        elif key < self.node.val:
            self.node.left.insert(key)
        elif key > self.node.val:
            self.node.right.insert(key)

        self.re_balance()

    def _initialize_node(self, key):
        node = TreeNode(key)
        node.left = AvlTree()
        node.right = AvlTree()
        self.node = node

    def re_balance(self):
        """
        Re balance tree. After inserting or deleting a node,
        """
        self._refresh_metrics(recursive=False)

        while abs(self.balance) > 1:
            if self.balance > 1:
                self._rebalance_left_heavy()
            else:
                self._rebalance_right_heavy()

    def _rebalance_left_heavy(self):
        if self.node.left.balance < 0:
            self.node.left.rotate_left()
            self._refresh_metrics()
        self.rotate_right()
        self._refresh_metrics()

    def _rebalance_right_heavy(self):
        if self.node.right.balance > 0:
            self.node.right.rotate_right()
            self._refresh_metrics()
        self.rotate_left()
        self._refresh_metrics()

    def _refresh_metrics(self, recursive=True):
        self.update_heights(recursive)
        self.update_balances(recursive)

    def update_heights(self, recursive=True):
        """
        Update tree height
        """
        if not self.node:
            self.height = -1
            return

        if recursive:
            self.node.left.update_heights()
            self.node.right.update_heights()

        self.height = 1 + max(self.node.left.height, self.node.right.height)

    def update_balances(self, recursive=True):
        """
        Calculate tree balance factor

        """
        if not self.node:
            self.balance = 0
            return

        if recursive:
            self.node.left.update_balances()
            self.node.right.update_balances()

        self.balance = self.node.left.height - self.node.right.height

    def rotate_right(self):
        """
        Right rotation
        """
        old_root = self.node
        new_root = old_root.left.node
        transferred_subtree = new_root.right.node

        self.node = new_root
        old_root.left.node = transferred_subtree
        new_root.right.node = old_root

    def rotate_left(self):
        """
        Left rotation
        """
        old_root = self.node
        new_root = old_root.right.node
        transferred_subtree = new_root.left.node

        self.node = new_root
        old_root.right.node = transferred_subtree
        new_root.left.node = old_root

    def in_order_traverse(self):
        """
        In-order traversal of the tree
        """
        if not self.node:
            return []

        return (
            self.node.left.in_order_traverse()
            + [self.node.key]
            + self.node.right.in_order_traverse()
        )


if __name__ == "__main__":
    tree = AvlTree()

    values = [10, 20, 5, 4, 15, 25, 3]
    for val in values:
        tree.insert(val)

    print("In-order traversal:", tree.in_order_traverse())