""" Imports TreeNodes"""

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.val = key
        self.left = None
        self.right = None
        self.height = 1


class AvlTree(object):
    """
    An avl tree.
    """

    def __init__(self):
        # Root node of the tree.
        self.node = None

    def insert(self, key):
        """
        Insert new key into node
        """
        self.node = self._insert(self.node, key)

    def _insert(self, node, key):
        if not node:
            return TreeNode(key)
        elif key < node.val:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1 and key < node.left.val:
            return self._rotate_right(node)
        if balance < -1 and key > node.right.val:
            return self._rotate_left(node)
        if balance > 1 and key > node.left.val:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.val:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))

        return new_root

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))

        return new_root

    def in_order_traverse(self):
        """
        In-order traversal of the tree
        """
        result = []
        self._in_order_traverse(self.node, result)
        return result

    def _in_order_traverse(self, node, result):
        if node:
            self._in_order_traverse(node.left, result)
            result.append(node.key)
            self._in_order_traverse(node.right, result)


if __name__ == "__main__":
    tree = AvlTree()

    values = [10, 20, 5, 4, 15, 25, 3]
    for val in values:
        tree.insert(val)

    print("In-order traversal:", tree.in_order_traverse())