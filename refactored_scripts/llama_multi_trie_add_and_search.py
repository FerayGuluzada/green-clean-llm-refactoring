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
        self.children = {}
        self.is_terminal = False

class WordDictionary:
    """A dictionary that allows adding and searching for words."""
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        """Add a word to the dictionary."""
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.is_terminal = True

    def search(self, word: str) -> bool:
        """Search for a word in the dictionary."""
        return self._search_recursive(self.root, word)

    def _search_recursive(self, node: TrieNode, word: str) -> bool:
        """Recursively search for a word in the dictionary."""
        for i, letter in enumerate(word):
            if letter == ".":
                return any(self._search_recursive(child, word[i+1:]) for child in node.children.values())
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_terminal

if __name__ == "__main__":
    wd = WordDictionary()

    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")

    print(wd.search("pad"))
    print(wd.search("bad"))
    print(wd.search(".ad"))
    print(wd.search("b.."))