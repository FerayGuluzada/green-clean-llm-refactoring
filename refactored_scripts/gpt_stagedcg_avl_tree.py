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
        node = self.node
        if not node:
            self._create_node(key)
            return

        if key < node.val:
            node.left.insert(key)
        elif key > node.val:
            node.right.insert(key)
        else:
            return

        self.re_balance()

    def _create_node(self, key):
        node = TreeNode(key)
        node.left = AvlTree()
        node.right = AvlTree()
        self.node = node
        self.height = 0
        self.balance = 0

    def re_balance(self):
        """
        Re balance tree. After inserting or deleting a node,
        """
        node = self.node
        if not node:
            self.height = -1
            self.balance = 0
            return

        left = node.left
        right = node.right

        left_height = left.height
        right_height = right.height
        self.height = 1 + (left_height if left_height > right_height else right_height)
        self.balance = left_height - right_height

        if self.balance > 1:
            if left.balance < 0:
                left.rotate_left()
                left._update_local()
            self.rotate_right()
            self._update_local()
        elif self.balance < -1:
            if right.balance > 0:
                right.rotate_right()
                right._update_local()
            self.rotate_left()
            self._update_local()

    def _update_local(self):
        node = self.node
        if not node:
            self.height = -1
            self.balance = 0
            return

        left_height = node.left.height
        right_height = node.right.height
        self.height = 1 + (left_height if left_height > right_height else right_height)
        self.balance = left_height - right_height

    def _refresh(self, recursive=False):
        self.update_heights(recursive=recursive)
        self.update_balances(recursive=recursive)

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

        old_root.left._update_local()
        new_root.right._update_local()

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

        old_root.right._update_local()
        new_root.left._update_local()

    def in_order_traverse(self):
        """
        In-order traversal of the tree
        """
        if not self.node:
            return []

        result = []
        stack = []
        current = self

        while stack or current.node:
            while current.node:
                stack.append(current)
                current = current.node.left

            current = stack.pop()
            result.append(current.node.key)
            current = current.node.right

        return result


if __name__ == "__main__":
    tree = AvlTree()

    values = [10, 20, 5, 4, 15, 25, 3]
    for val in values:
        tree.insert(val)

    print("In-order traversal:", tree.in_order_traverse())