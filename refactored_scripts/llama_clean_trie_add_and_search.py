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
    def __init__(self):
        self.children = {}
        self.is_terminal = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        node = self.root
        for letter in word:
            node = node.children.setdefault(letter, TrieNode())
        node.is_terminal = True

    def _search(self, word, node):
        for i, letter in enumerate(word):
            if letter == ".":
                return any(self._search(word[i+1:], child) for child in node.children.values())
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_terminal

    def search(self, word):
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