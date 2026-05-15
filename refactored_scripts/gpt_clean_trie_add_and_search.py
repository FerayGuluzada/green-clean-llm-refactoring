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
        node = self.root
        for letter in word:
            node = node.children.setdefault(letter, TrieNode(letter))
        node.is_terminal = True

    def search(self, word, node=None):
        return self._search_from(word, node or self.root)

    def _search_from(self, word, node):
        for index, letter in enumerate(word):
            if letter == ".":
                suffix = word[index + 1:]
                return any(self._search_from(suffix, child) for child in node.children.values())

            node = node.children.get(letter)
            if node is None:
                return False

        return node.is_terminal


class WordDictionary2(object):
    def __init__(self):
        self.word_dict = collections.defaultdict(list)

    def add_word(self, word):
        if word:
            self.word_dict[len(word)].append(word)

    def search(self, word):
        if not word:
            return False

        candidates = self.word_dict[len(word)]
        if "." not in word:
            return word in candidates

        return any(self._matches_pattern(word, candidate) for candidate in candidates)

    def _matches_pattern(self, pattern, word):
        return all(pattern_char == "." or pattern_char == word_char
                   for pattern_char, word_char in zip(pattern, word))


if __name__ == "__main__":
    wd = WordDictionary2()

    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")

    print(wd.search("pad"))
    print(wd.search("bad"))
    print(wd.search(".ad"))
    print(wd.search("b.."))