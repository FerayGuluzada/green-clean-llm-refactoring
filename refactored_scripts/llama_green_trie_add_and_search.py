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
    def __init__(self, letter, is_terminal=False):
        self.children = dict()
        self.letter = letter
        self.is_terminal = is_terminal

class WordDictionary(object):
    def __init__(self):
        self.root = TrieNode("")

    def add_word(self, word):
        cur = self.root
        for letter in word:
            if letter not in cur.children:
                cur.children[letter] = TrieNode(letter)
            cur = cur.children[letter]
        cur.is_terminal = True

    def search(self, word, node=None):
        if not node:
            node = self.root
        if not word:
            return node.is_terminal
        if word[0] == ".":
            for child in node.children.values():
                if self.search(word[1:], child):
                    return True
            return False
        if word[0] not in node.children:
            return False
        return self.search(word[1:], node.children[word[0]])

class WordDictionary2(object):
    def __init__(self):
        self.word_dict = collections.defaultdict(list)

    def add_word(self, word):
        if word:
            self.word_dict[len(word)].append(word)

    def search(self, word):
        if not word:
            return False
        if '.' not in word:
            return word in self.word_dict[len(word)]
        for v in self.word_dict[len(word)]:
            match = True
            for i, ch in enumerate(word):
                if ch!= v[i] and ch!= '.':
                    match = False
                    break
            if match:
                return True
        return False


if __name__ == "__main__":
    wd = WordDictionary()

    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")

    print(wd.search("pad"))
    print(wd.search("bad"))
    print(wd.search(".ad"))
    print(wd.search("b.."))