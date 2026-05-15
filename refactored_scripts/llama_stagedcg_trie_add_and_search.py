"""
We are asked to design an efficient data structure
that allows us to add and search for words.
The search can be a literal word or regular expression
containing “.”, where “.” can be any letter.

Example:
addWord(“bad”)
addWord(“dad”)
addWord(“mad”)
search(“pad”) -> false
search(“bad”) -> true
search(“.ad”) -> true
search(“b..”) -> true
"""
import collections

class TrieNode:
    """A node in the Trie data structure."""
    def __init__(self):
        # Use a defaultdict to avoid KeyError when accessing children
        self.children = collections.defaultdict(TrieNode)
        self.is_terminal = False

class WordDictionary:
    """A dictionary that allows adding and searching for words."""
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        """Add a word to the dictionary."""
        node = self.root
        for letter in word:
            # Use the defaultdict to create children nodes on the fly
            node = node.children[letter]
        node.is_terminal = True

    def _search(self, word, node):
        """Recursively search for a word in the Trie."""
        for i, letter in enumerate(word):
            if letter == ".":
                # Use a generator expression to avoid creating a list
                return any(self._search(word[i+1:], child) for child in node.children.values())
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_terminal

    def search(self, word):
        """Search for a word in the dictionary."""
        return self._search(word, self.root)

if __name__ == "__main__":
    wd = WordDictionary()

    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")

    print(wd.search("pad"))
    print(wd.search("bad"))
    print(wd.search(".ad"))
    print(wd.search("b.."))