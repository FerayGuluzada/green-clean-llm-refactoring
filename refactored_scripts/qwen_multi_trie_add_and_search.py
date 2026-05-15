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
    def __init__(self, letter):
        self.children = {}
        self.letter = letter
        self.is_terminal = False

class WordDictionary(object):
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
        return self._search_helper(word, 0, self.root)
    
    def _search_helper(self, word, index, node):
        # Base case: reached end of word
        if index == len(word):
            return node.is_terminal
            
        char = word[index]
        
        # Handle wildcard character
        if char == ".":
            return any(
                self._search_helper(word, index + 1, child)
                for child in node.children.values()
            )
        
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
            
        # Direct lookup for exact matches
        if '.' not in word:
            return word in self.word_dict[len(word)]
        
        # Pattern matching for words with wildcards
        word_len = len(word)
        for candidate in self.word_dict[word_len]:
            if self._matches(word, candidate):
                return True
        return False
    
    def _matches(self, pattern, word):
        """Check if pattern matches word, where '.' matches any character."""
        return all(
            p_char == '.' or p_char == w_char
            for p_char, w_char in zip(pattern, word)
        )


if __name__ == "__main__":
    wd = WordDictionary2()

    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")

    print(wd.search("pad"))  # False
    print(wd.search("bad"))  # True
    print(wd.search(".ad"))  # True
    print(wd.search("b.."))  # True