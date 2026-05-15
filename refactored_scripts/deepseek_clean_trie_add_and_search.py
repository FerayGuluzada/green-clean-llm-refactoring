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
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.is_terminal = True

    def search(self, word):
        return self._search_from_node(word, self.root)

    def _search_from_node(self, word, node):
        for i, letter in enumerate(word):
            if letter == ".":
                return self._handle_wildcard(word[i:], node)
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_terminal

    def _handle_wildcard(self, suffix, node):
        if not suffix:
            return any(child.is_terminal for child in node.children.values())
        
        next_char = suffix[0]
        remaining = suffix[1:]
        
        for child in node.children.values():
            if next_char == "." or next_char == child.letter:
                if self._search_from_node(remaining, child):
                    return True
        return False


class WordDictionary2:
    def __init__(self):
        self.words_by_length = collections.defaultdict(list)

    def add_word(self, word):
        if word:
            self.words_by_length[len(word)].append(word)

    def search(self, word):
        if not word:
            return False
        
        if "." not in word:
            return word in self.words_by_length[len(word)]
        
        return self._match_pattern(word)

    def _match_pattern(self, pattern):
        length = len(pattern)
        for candidate in self.words_by_length[length]:
            if self._is_match(candidate, pattern):
                return True
        return False

    def _is_match(self, candidate, pattern):
        for c, p in zip(candidate, pattern):
            if p != "." and p != c:
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