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
    __slots__ = ('children', 'is_terminal')
    
    def __init__(self):
        self.children = {}
        self.is_terminal = False

class WordDictionary(object):
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_terminal = True

    def search(self, word):
        return self._search_from_node(word, 0, self.root)
    
    def _search_from_node(self, word, index, node):
        if index == len(word):
            return node.is_terminal
            
        char = word[index]
        if char == '.':
            return any(self._search_from_node(word, index + 1, child) 
                      for child in node.children.values())
        else:
            if char not in node.children:
                return False
            return self._search_from_node(word, index + 1, node.children[char])

class WordDictionary2(object):
    def __init__(self):
        self.word_dict = collections.defaultdict(list)

    def add_word(self, word):
        if word:
            self.word_dict[len(word)].append(word)

    def search(self, word):
        if not word or len(word) not in self.word_dict:
            return False
            
        if '.' not in word:
            return word in self.word_dict[len(word)]
            
        # Extract fixed character positions
        fixed_matches = [(i, ch) for i, ch in enumerate(word) if ch != '.']
        
        # If no fixed characters, any word of same length matches
        if not fixed_matches:
            return bool(self.word_dict[len(word)])
            
        # Unzip indices and characters for efficient matching
        indices, chars = zip(*fixed_matches)
        
        # Check candidates
        for candidate in self.word_dict[len(word)]:
            if all(candidate[i] == ch for i, ch in zip(indices, chars)):
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