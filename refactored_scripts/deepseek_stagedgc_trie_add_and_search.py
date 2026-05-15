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
    __slots__ = ('children', 'letter', 'is_terminal')
    
    def __init__(self, letter, is_terminal=False):
        self.children = {}
        self.letter = letter
        self.is_terminal = is_terminal


class WordDictionary:
    def __init__(self):
        self.root = TrieNode("")

    def add_word(self, word):
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode(letter)
            node = node.children[letter]
        node.is_terminal = True

    def search(self, word):
        return self._search_from_node(word, 0, self.root)
    
    def _search_from_node(self, word, idx, node):
        if idx == len(word):
            return node.is_terminal
            
        letter = word[idx]
        
        if letter == '.':
            for child in node.children.values():
                if self._search_from_node(word, idx + 1, child):
                    return True
            return False
        
        if letter not in node.children:
            return False
        return self._search_from_node(word, idx + 1, node.children[letter])


class WordDictionary2:
    __slots__ = ('word_dict',)
    
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
        
        return self._search_with_dots(word, length)
    
    def _search_with_dots(self, word, length):
        for candidate in self.word_dict.get(length, []):
            if self._matches_pattern(word, candidate):
                return True
        return False
    
    def _matches_pattern(self, pattern, candidate):
        for p_char, c_char in zip(pattern, candidate):
            if p_char != '.' and p_char != c_char:
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