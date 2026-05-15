class TreeNode:
    def __init__(self, key):
        self.key = key
        self.val = key
        self.left = None
        self.right = None


class AvlTree:
    """
    An AVL tree implementation with automatic balancing.
    """

    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

    def insert(self, key):
        """
        Insert a new key into the tree and rebalance if necessary.
        """
        if not self.node:
            self._initialize_node(key)
        elif key < self.node.val:
            self.node.left.insert(key)
        elif key > self.node.val:
            self.node.right.insert(key)
        
        self._rebalance_tree()

    def _initialize_node(self, key):
        """Initialize root node with children."""
        self.node = TreeNode(key)
        self.node.left = AvlTree()
        self.node.right = AvlTree()

    def _rebalance_tree(self):
        """Rebalance the tree after insertion or deletion."""
        self._update_height_and_balance()

        while abs(self.balance) > 1:
            self._perform_rotation()
            self._update_height_and_balance()

    def _update_height_and_balance(self):
        """Update height and balance factor."""
        if not self.node:
            self.height, self.balance = -1, 0
            return

        # Update heights recursively
        self.node.left._update_height_and_balance()
        self.node.right._update_height_and_balance()
        
        # Calculate current node values
        self.height = 1 + max(self.node.left.height, self.node.right.height)
        self.balance = self.node.left.height - self.node.right.height

    def _perform_rotation(self):
        """Perform necessary rotations to balance the tree."""
        if self.balance > 1:  # Left-heavy
            if self.node.left.balance < 0:  # Left-right case
                self.node.left._rotate_left()
            self._rotate_right()
        elif self.balance < -1:  # Right-heavy
            if self.node.right.balance > 0:  # Right-left case
                self.node.right._rotate_right()
            self._rotate_left()

    def _rotate_right(self):
        """Perform right rotation."""
        old_root = self.node
        new_root = old_root.left.node
        new_left_sub = new_root.right.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

    def _rotate_left(self):
        """Perform left rotation."""
        old_root = self.node
        new_root = old_root.right.node
        new_left_sub = new_root.left.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

    def in_order_traverse(self):
        """
        Return in-order traversal of the tree.
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