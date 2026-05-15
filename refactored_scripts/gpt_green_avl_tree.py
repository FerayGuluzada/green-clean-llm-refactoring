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
            node = TreeNode(key)
            self.node = node
            self.node.left = AvlTree()
            self.node.right = AvlTree()
            self.height = 0
            self.balance = 0
            return

        node = self.node
        if key < node.val:
            node.left.insert(key)
        elif key > node.val:
            node.right.insert(key)
        else:
            return

        self.re_balance()

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
                left.update_metrics()
            self.rotate_right()
            self.update_metrics()
        elif self.balance < -1:
            if right.balance > 0:
                right.rotate_right()
                right.update_metrics()
            self.rotate_left()
            self.update_metrics()

    def update_metrics(self):
        """
        Update tree height and balance factor
        """
        node = self.node
        if node:
            left_height = node.left.height
            right_height = node.right.height
            self.height = 1 + (left_height if left_height > right_height else right_height)
            self.balance = left_height - right_height
        else:
            self.height = -1
            self.balance = 0

    def update_heights(self, recursive=True):
        """
        Update tree height
        """
        if self.node:
            if recursive:
                self.node.left.update_heights()
                self.node.right.update_heights()

            left_height = self.node.left.height
            right_height = self.node.right.height
            self.height = 1 + (left_height if left_height > right_height else right_height)
        else:
            self.height = -1

    def update_balances(self, recursive=True):
        """
        Calculate tree balance factor

        """
        if self.node:
            if recursive:
                self.node.left.update_balances()
                self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def rotate_right(self):
        """
        Right rotation
        """
        old_root = self.node
        new_root = old_root.left.node
        moved_subtree = new_root.right.node

        self.node = new_root
        old_root.left.node = moved_subtree
        new_root.right.node = old_root

        old_root.left.update_metrics()
        old_root.right.update_metrics()
        new_root.right.update_metrics()

    def rotate_left(self):
        """
        Left rotation
        """
        old_root = self.node
        new_root = old_root.right.node
        moved_subtree = new_root.left.node

        self.node = new_root
        old_root.right.node = moved_subtree
        new_root.left.node = old_root

        old_root.left.update_metrics()
        old_root.right.update_metrics()
        new_root.left.update_metrics()

    def in_order_traverse(self):
        """
        In-order traversal of the tree
        """
        result = []
        self._in_order_traverse(result)
        return result

    def _in_order_traverse(self, result):
        node = self.node
        if not node:
            return

        node.left._in_order_traverse(result)
        result.append(node.key)
        node.right._in_order_traverse(result)


if __name__ == "__main__":
    tree = AvlTree()

    values = [10, 20, 5, 4, 15, 25, 3]
    for val in values:
        tree.insert(val)

    print("In-order traversal:", tree.in_order_traverse())