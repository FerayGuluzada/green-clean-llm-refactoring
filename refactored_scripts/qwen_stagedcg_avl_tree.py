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
        # Root node of the tree.
        self.node = None
        self.height = -1
        self.balance = 0

    def insert(self, key):
        """
        Insert new key into node
        """
        # Create new node
        if not self.node:
            node = TreeNode(key)
            self.node = node
            self.node.left = AvlTree()
            self.node.right = AvlTree()
        else:
            if key < self.node.val:
                self.node.left.insert(key)
            elif key > self.node.val:
                self.node.right.insert(key)
            else:
                return  # Duplicate key, do nothing
        
        self.re_balance()

    def re_balance(self):
        """
        Rebalance tree after insertion or deletion
        """
        self.update_heights(False)
        self.update_balances(False)

        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotate_left()
                self.rotate_right()

            elif self.balance < -1:  # Changed to elif for efficiency
                if self.node.right.balance > 0:
                    self.node.right.rotate_right()
                self.rotate_left()
            
            # Update heights and balances after rotations
            self.update_heights()
            self.update_balances()

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

        # Use max with default to handle None cases more efficiently
        left_height = self.node.left.height if self.node.left else -1
        right_height = self.node.right.height if self.node.right else -1
        self.height = 1 + max(left_height, right_height)

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

        # Direct access to heights for better performance
        left_height = self.node.left.height if self.node.left else -1
        right_height = self.node.right.height if self.node.right else -1
        self.balance = left_height - right_height

    def rotate_right(self):
        """
        Right rotation
        """
        old_root = self.node
        new_root = old_root.left.node
        new_left_sub = new_root.right.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

    def rotate_left(self):
        """
        Left rotation
        """
        old_root = self.node
        new_root = old_root.right.node
        new_left_sub = new_root.left.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

    def in_order_traverse(self):
        """
        In-order traversal of the tree
        """
        if not self.node:
            return []

        result = []
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