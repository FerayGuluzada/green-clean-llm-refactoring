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
        cur = self.root
        for letter in word:
            child = cur.children.get(letter)
            if child is None:
                child = TrieNode()
                cur.children[letter] = child
            cur = child
        cur.is_terminal = True

    def search(self, word, node=None):
        cur = self.root if node is None else node
        n = len(word)

        def dfs(start, trie_node):
            cur_node = trie_node
            for i in range(start, n):
                letter = word[i]
                if letter == ".":
                    if i == n - 1:  # if last character
                        for child in cur_node.children.values():
                            if child.is_terminal:
                                return True
                        return False
                    next_index = i + 1
                    for child in cur_node.children.values():
                        if dfs(next_index, child):
                            return True
                    return False

                cur_node = cur_node.children.get(letter)
                if cur_node is None:
                    return False
            return cur_node.is_terminal

        return dfs(0, cur)


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
        if not candidates:
            return False

        for candidate in candidates:
            for i in range(word_len):
                ch = word[i]
                if ch != "." and ch != candidate[i]:
                    break
            else:
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