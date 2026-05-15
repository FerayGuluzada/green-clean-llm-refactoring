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
    __slots__ = ("children", "is_terminal")

    def __init__(self, is_terminal=False):
        self.children = {}
        self.is_terminal = is_terminal


class WordDictionary(object):
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        node = self.root
        for letter in word:
            child = node.children.get(letter)
            if child is None:
                child = TrieNode()
                node.children[letter] = child
            node = child
        node.is_terminal = True

    def search(self, word, node=None):
        root = self.root if node is None else node
        word_len = len(word)

        def dfs(index, trie_node):
            if index == word_len:
                return trie_node.is_terminal

            letter = word[index]
            if letter == ".":
                next_index = index + 1
                for child in trie_node.children.values():
                    if dfs(next_index, child):
                        return True
                return False

            child = trie_node.children.get(letter)
            return False if child is None else dfs(index + 1, child)

        return dfs(0, root)


class WordDictionary2(object):
    def __init__(self):
        self.word_dict = collections.defaultdict(list)
        self.word_sets = collections.defaultdict(set)

    def add_word(self, word):
        if not word:
            return

        word_len = len(word)
        self.word_dict[word_len].append(word)
        self.word_sets[word_len].add(word)

    def search(self, word):
        if not word:
            return False

        word_len = len(word)
        if "." not in word:
            return word in self.word_sets[word_len]

        for candidate in self.word_dict[word_len]:
            if self._matches(word, candidate):
                return True
        return False

    @staticmethod
    def _matches(pattern, candidate):
        for pattern_ch, candidate_ch in zip(pattern, candidate):
            if pattern_ch != "." and pattern_ch != candidate_ch:
                return False
        return True


if __name__ == "__main__":
    wd = WordDictionary2()

    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")

    print(wd.search("pad"))
    print(wd.search("bad"))
    print(wd.search(".ad"))
    print(wd.search("b.."))