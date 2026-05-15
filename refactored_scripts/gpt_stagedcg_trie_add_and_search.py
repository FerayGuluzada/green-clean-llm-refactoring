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
    __slots__ = ("children", "letter", "is_terminal")

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
            children = node.children
            next_node = children.get(letter)
            if next_node is None:
                next_node = TrieNode(letter)
                children[letter] = next_node
            node = next_node
        node.is_terminal = True

    def search(self, word, node=None):
        return self._search_from(word, 0, node or self.root)

    def _search_from(self, word, index, node):
        word_len = len(word)

        while index < word_len:
            letter = word[index]
            if letter == ".":
                next_index = index + 1
                for child in node.children.values():
                    if self._search_from(word, next_index, child):
                        return True
                return False

            node = node.children.get(letter)
            if node is None:
                return False
            index += 1

        return node.is_terminal


class WordDictionary2(object):
    def __init__(self):
        self.word_dict = collections.defaultdict(list)
        self.word_sets = collections.defaultdict(set)

    def add_word(self, word):
        if word:
            word_len = len(word)
            self.word_dict[word_len].append(word)
            self.word_sets[word_len].add(word)

    def search(self, word):
        if not word:
            return False

        word_len = len(word)
        if "." not in word:
            return word in self.word_sets[word_len]

        candidates = self.word_dict[word_len]
        for candidate in candidates:
            if self._matches_pattern(word, candidate):
                return True
        return False

    def _matches_pattern(self, pattern, word):
        for pattern_char, word_char in zip(pattern, word):
            if pattern_char != "." and pattern_char != word_char:
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