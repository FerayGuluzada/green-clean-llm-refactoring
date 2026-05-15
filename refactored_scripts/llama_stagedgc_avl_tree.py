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
        self.node = self._insert_recursive(self.node, key)
        self.re_balance()

    def _insert_recursive(self, node, key):
        if not node:
            return TreeNode(key)
        elif key < node.val:
            node.left = self._insert_recursive(node.left, key) if node.left else AvlTree()
            node.left.node = node.left._insert_recursive(node.left.node, key) if node.left else TreeNode(key)
        elif key > node.val:
            node.right = self._insert_recursive(node.right, key) if node.right else AvlTree()
            node.right.node = node.right._insert_recursive(node.right.node, key) if node.right else TreeNode(key)
        return node

    def re_balance(self):
        """
        Re balance tree. After inserting or deleting a node,
        """
        self.update_heights()
        self.update_balances()

        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotate_left()
                self.rotate_right()
            elif self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rotate_right()
                self.rotate_left()
            self.update_heights()
            self.update_balances()

    def update_heights(self):
        """
        Update tree height
        """
        self._update_heights_recursive(self.node)

    def _update_heights_recursive(self, node):
        if node:
            if node.left:
                self._update_heights_recursive(node.left.node)
            if node.right:
                self._update_heights_recursive(node.right.node)
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        self.height = self.get_height(self.node)

    def update_balances(self):
        """
        Calculate tree balance factor

        """
        self._update_balances_recursive(self.node)

    def _update_balances_recursive(self, node):
        if node:
            if node.left:
                self._update_balances_recursive(node.left.node)
            if node.right:
                self._update_balances_recursive(node.right.node)
            node.balance = self.get_height(node.left) - self.get_height(node.right)
        self.balance = self.get_height(self.node.left) - self.get_height(self.node.right) if self.node else 0

    def rotate_right(self):
        """
        Right rotation
        """
        new_root = self.node.left.node
        new_left_sub = new_root.right
        old_root = self.node

        self.node = new_root
        old_root.left = new_left_sub
        new_root.right = old_root
        self.update_heights()
        self.update_balances()

    def rotate_left(self):
        """
        Left rotation
        """
        new_root = self.node.right.node
        new_left_sub = new_root.left
        old_root = self.node

        self.node = new_root
        old_root.right = new_left_sub
        new_root.left = old_root
        self.update_heights()
        self.update_balances()

    def in_order_traverse(self):
        """
        In-order traversal of the tree
        """
        return self._in_order_traverse_recursive(self.node)

    def _in_order_traverse_recursive(self, node):
        result = []
        if node:
            result.extend(self._in_order_traverse_recursive(node.left.node) if node.left else [])
            result.append(node.key)
            result.extend(self._in_order_traverse_recursive(node.right.node) if node.right else [])
        return result

    @staticmethod
    def get_height(node):
        return node.height if node else -1


if __name__ == "__main__":
    tree = AvlTree()

    values = [10, 20, 5, 4, 15, 25, 3]
    for val in values:
        tree.insert(val)

    print("In-order traversal:", tree.in_order_traverse())