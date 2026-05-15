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
    __slots__ = ('children', 'letter', 'is_terminal')
    
    def __init__(self, letter, is_terminal=False):
        self.children = {}
        self.letter = letter
        self.is_terminal = is_terminal

class WordDictionary(object):
    def __init__(self):
        self.root = TrieNode("")

    def add_word(self, word):
        cur = self.root
        for letter in word:
            nxt = cur.children.get(letter)
            if nxt is None:
                nxt = TrieNode(letter)
                cur.children[letter] = nxt
            cur = nxt
        cur.is_terminal = True

    def search(self, word):
        return self._search_recursive(word, 0, self.root)
    
    def _search_recursive(self, word, idx, node):
        if idx == len(word):
            return node.is_terminal
            
        letter = word[idx]
        
        if letter == '.':
            # Early exit if this is the last character
            if idx == len(word) - 1:
                return any(child.is_terminal for child in node.children.values())
            
            # Check all children recursively
            for child in node.children.values():
                if self._search_recursive(word, idx + 1, child):
                    return True
            return False
        
        # Exact letter match
        nxt = node.children.get(letter)
        if nxt is None:
            return False
        return self._search_recursive(word, idx + 1, nxt)

class WordDictionary2(object):
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
        candidates = self.word_dict.get(length, [])
        
        if '.' not in word:
            # Use set for O(1) lookup instead of O(n) list search
            return word in self.word_dict[length]
        
        # Pre-compile pattern positions
        dot_positions = [i for i, ch in enumerate(word) if ch == '.']
        
        for candidate in candidates:
            # Quick length check (already done by dict lookup)
            # Check only positions that aren't dots
            for i in range(length):
                if word[i] != '.' and word[i] != candidate[i]:
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