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
            self.node = TreeNode(key)
            self.node.left = AvlTree()
            self.node.right = AvlTree()
        elif key < self.node.val:
            self.node.left.insert(key)
        elif key > self.node.val:
            self.node.right.insert(key)
        else:
            return

        self.re_balance()

    def re_balance(self):
        """
        Re balance tree. After inserting or deleting a node,
        """
        self._refresh()

        while abs(self.balance) > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotate_left()
                    self.node.left._refresh()
                self.rotate_right()
            else:
                if self.node.right.balance > 0:
                    self.node.right.rotate_right()
                    self.node.right._refresh()
                self.rotate_left()
            self._refresh()

    def _refresh(self):
        if not self.node:
            self.height = -1
            self.balance = 0
            return

        left = self.node.left
        right = self.node.right
        self.height = 1 + max(left.height, right.height)
        self.balance = left.height - right.height

    def update_heights(self, recursive=True):
        """
        Update tree height
        """
        if self.node and recursive:
            self.node.left.update_heights()
            self.node.right.update_heights()

        self.height = (
            1 + max(self.node.left.height, self.node.right.height)
            if self.node
            else -1
        )

    def update_balances(self, recursive=True):
        """
        Calculate tree balance factor

        """
        if self.node and recursive:
            self.node.left.update_balances()
            self.node.right.update_balances()

        self.balance = (
            self.node.left.height - self.node.right.height
            if self.node
            else 0
        )

    def rotate_right(self):
        """
        Right rotation
        """
        old_root = self.node
        new_root = old_root.left.node
        old_root.left.node = new_root.right.node
        new_root.right.node = old_root
        self.node = new_root
        old_root.left._refresh()
        new_root.right._refresh()
        self._refresh()

    def rotate_left(self):
        """
        Left rotation
        """
        old_root = self.node
        new_root = old_root.right.node
        old_root.right.node = new_root.left.node
        new_root.left.node = old_root
        self.node = new_root
        old_root.right._refresh()
        new_root.left._refresh()
        self._refresh()

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