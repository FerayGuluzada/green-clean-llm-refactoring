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
        self.node = self._insert(self.node, key)
        self.height = self._get_height(self.node)
        self.balance = self._get_balance(self.node)

    def _insert(self, node, key):
        if not node:
            return TreeNode(key)
        elif key < node.val:
            node.left = self._insert(node.left, key)
        elif key > node.val:
            node.right = self._insert(node.right, key)
        return self._re_balance(node)

    def _re_balance(self, node):
        node.height = self._get_height(node)
        node.balance = self._get_balance(node)
        if node.balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        elif node.balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _get_height(self, node):
        if not node:
            return -1
        return 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        node.height = self._get_height(node)
        node.balance = self._get_balance(node)
        new_root.height = self._get_height(new_root)
        new_root.balance = self._get_balance(new_root)
        return new_root

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        node.height = self._get_height(node)
        node.balance = self._get_balance(node)
        new_root.height = self._get_height(new_root)
        new_root.balance = self._get_balance(new_root)
        return new_root

    def in_order_traverse(self):
        """
        In-order traversal of the tree
        """
        return self._in_order_traverse(self.node)

    def _in_order_traverse(self, node):
        result = []
        if node:
            result.extend(self._in_order_traverse(node.left))
            result.append(node.key)
            result.extend(self._in_order_traverse(node.right))
        return result


if __name__ == "__main__":
    tree = AvlTree()

    values = [10, 20, 5, 4, 15, 25, 3]
    for val in values:
        tree.insert(val)

    print("In-order traversal:", tree.in_order_traverse())