"""
We are asked to design an efficient data structure
that allows us to add and search for words.
The search can be a literal word or regular expression
containing ".", where "." can be any letter.

Example:
addWord("bad")
add_word("dad")
add_word("mad")
search("pad") -> false
search("bad") -> true
search(".ad") -> true
search("b..") -> true
"""
import collections

class TrieNode(object):
    __slots__ = ('children', 'letter', 'is_terminal')
    
    def __init__(self, letter="", is_terminal=False):
        self.children = dict()
        self.letter = letter
        self.is_terminal = is_terminal

class WordDictionary(object):
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        cur = self.root
        children = cur.children
        for letter in word:
            if letter not in children:
                children[letter] = TrieNode(letter)
            cur = children[letter]
            children = cur.children
        cur.is_terminal = True

    def search(self, word, node=None):
        cur = node or self.root
        
        for i, letter in enumerate(word):
            if letter == ".":
                # For wildcard, check all children recursively
                remaining = word[i+1:]
                # Use iterative approach to avoid deep recursion
                return any(self.search(remaining, child) for child in cur.children.values())
            elif letter in cur.children:
                cur = cur.children[letter]
            else:
                return False
                
        return cur.is_terminal

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
        
        if '.' not in word:
            return word in candidates
            
        # Check each candidate against pattern
        pattern_chars = tuple(word)  # Convert to tuple for faster access
        for candidate in candidates:
            if self._matches(candidate, pattern_chars):
                return True
        return False
        
    def _matches(self, candidate, pattern_chars):
        """Check if candidate word matches pattern with wildcards."""
        # Use direct iteration instead of zip for better performance
        for i, pattern_char in enumerate(pattern_chars):
            if pattern_char != '.' and pattern_char != candidate[i]:
                return False
        return True

if __name__ == "__main__":
    wd = WordDictionary2()

    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")

    print(wd.search("pad"))  # False
    print(wd.search("bad"))  # True
    print(wd.search(".ad"))  # True
    print(wd.search("b.."))  # True