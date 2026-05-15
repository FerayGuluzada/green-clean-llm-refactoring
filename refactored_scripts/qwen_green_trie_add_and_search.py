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
        return self._search_helper(word, 0, self.root)
    
    def _search_helper(self, word, index, node):
        # Base case: reached end of word
        if index == len(word):
            return node.is_terminal
            
        char = word[index]
        
        # Handle wildcard character
        if char == '.':
            # Check all children nodes
            for child_node in node.children.values():
                if self._search_helper(word, index + 1, child_node):
                    return True
            return False
        else:
            # Handle regular character
            if char not in node.children:
                return False
            return self._search_helper(word, index + 1, node.children[char])

class WordDictionary2(object):
    def __init__(self):
        self.word_dict = collections.defaultdict(list)

    def add_word(self, word):
        if word:
            self.word_dict[len(word)].append(word)

    def search(self, word):
        if not word:
            return False
            
        word_len = len(word)
        if word_len not in self.word_dict:
            return False
            
        if '.' not in word:
            return word in self.word_dict[word_len]
            
        # Pre-compile pattern analysis
        pattern_chars = [(i, ch) for i, ch in enumerate(word) if ch != '.']
        
        # Early exit if no specific characters to match
        if not pattern_chars:
            return bool(self.word_dict[word_len])
            
        # Extract indices and characters that need matching
        fixed_indices, fixed_chars = zip(*pattern_chars) if pattern_chars else ([], [])
        
        # Check each candidate word
        for candidate in self.word_dict[word_len]:
            # Match all fixed positions
            for idx, ch in zip(fixed_indices, fixed_chars):
                if candidate[idx] != ch:
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