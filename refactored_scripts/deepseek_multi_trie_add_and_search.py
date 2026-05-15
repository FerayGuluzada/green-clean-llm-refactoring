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
        cur = self.root
        for letter in word:
            if letter not in cur.children:
                cur.children[letter] = TrieNode()
            cur = cur.children[letter]
        cur.is_terminal = True

    def search(self, word):
        return self._search_recursive(word, 0, self.root)

    def _search_recursive(self, word, index, node):
        if index == len(word):
            return node.is_terminal

        letter = word[index]

        if letter == '.':
            for child in node.children.values():
                if self._search_recursive(word, index + 1, child):
                    return True
            return False

        if letter not in node.children:
            return False

        return self._search_recursive(word, index + 1, node.children[letter])


class WordDictionary2:
    def __init__(self):
        self.word_dict = collections.defaultdict(list)

    def add_word(self, word):
        if word:
            self.word_dict[len(word)].append(word)

    def search(self, word):
        if not word:
            return False

        length = len(word)
        if '.' not in word:
            return word in self.word_dict[length]

        for candidate in self.word_dict[length]:
            if all(c1 == c2 or c2 == '.' for c1, c2 in zip(candidate, word)):
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