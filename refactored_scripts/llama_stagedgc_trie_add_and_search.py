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
    """Node in the Trie data structure."""
    def __init__(self, letter, is_terminal=False):
        self.children = {}
        self.letter = letter
        self.is_terminal = is_terminal

class WordDictionary:
    """Data structure for efficient word addition and search."""
    def __init__(self):
        self.root = TrieNode("")

    def add_word(self, word: str) -> None:
        """Add a word to the dictionary."""
        node = self.root
        for letter in word:
            node = node.children.setdefault(letter, TrieNode(letter))
        node.is_terminal = True

    def _search(self, word: str, node: TrieNode) -> bool:
        """Recursive search helper function."""
        if not word:
            return node.is_terminal
        if word[0] == ".":
            return any(self._search(word[1:], child) for child in node.children.values())
        return word[0] in node.children and self._search(word[1:], node.children[word[0]])

    def search(self, word: str) -> bool:
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