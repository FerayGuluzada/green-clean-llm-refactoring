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


class TrieNode(object):
    def __init__(self, letter="", is_terminal=False):
        self.children = {}
        self.letter = letter
        self.is_terminal = is_terminal


class WordDictionary(object):
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        cur = self.root
        for letter in word:
            cur = cur.children.setdefault(letter, TrieNode(letter))
        cur.is_terminal = True

    def search(self, word, node=None):
        cur = self.root if node is None else node
        return self._search_from(word, 0, cur)

    def _search_from(self, word, index, node):
        for i in range(index, len(word)):
            letter = word[i]
            if letter == ".":
                next_index = i + 1
                return any(self._search_from(word, next_index, child) for child in node.children.values())
            node = node.children.get(letter)
            if node is None:
                return False
        return node.is_terminal


class WordDictionary2(object):
    def __init__(self):
        self.word_dict = collections.defaultdict(set)

    def add_word(self, word):
        if word:
            self.word_dict[len(word)].add(word)

    def search(self, word):
        if not word:
            return False

        words = self.word_dict[len(word)]
        if "." not in word:
            return word in words

        for candidate in words:
            if all(ch == "." or ch == candidate[i] for i, ch in enumerate(word)):
                return True
        return False


if __name__ == "__main__":
    wd = WordDictionary2()

    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")

    print(wd.search("pad"))
    print(wd.search("bad"))
    print(wd.search(".ad"))
    print(wd.search("b.."))