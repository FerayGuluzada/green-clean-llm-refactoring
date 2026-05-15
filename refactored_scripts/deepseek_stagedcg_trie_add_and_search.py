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
    __slots__ = ('children', 'is_terminal')
    
    def __init__(self):
        self.children = {}
        self.is_terminal = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        node = self.root
        for letter in word:
            child = node.children.get(letter)
            if child is None:
                child = TrieNode()
                node.children[letter] = child
            node = child
        node.is_terminal = True

    def search(self, word):
        return self._search_from_node(word, 0, self.root)

    def _search_from_node(self, word, idx, node):
        """Iterative DFS with early termination."""
        stack = [(idx, node)]
        
        while stack:
            i, current = stack.pop()
            
            # Base case: reached end of word
            if i == len(word):
                if current.is_terminal:
                    return True
                continue
            
            letter = word[i]
            
            if letter == ".":
                # Wildcard: push all children with next index
                for child in current.children.values():
                    stack.append((i + 1, child))
            else:
                # Exact match: push matching child if exists
                child = current.children.get(letter)
                if child is not None:
                    stack.append((i + 1, child))
        
        return False


class WordDictionary2:
    __slots__ = ('words_by_length', '_pattern_cache')
    
    def __init__(self):
        self.words_by_length = collections.defaultdict(set)
        self._pattern_cache = {}

    def add_word(self, word):
        if word:
            self.words_by_length[len(word)].add(word)
            # Invalidate cache for this length
            self._pattern_cache.pop(len(word), None)

    def search(self, word):
        if not word:
            return False
        
        length = len(word)
        
        # Fast path: exact match
        if "." not in word:
            return word in self.words_by_length[length]
        
        # Check cache first
        cache_key = (length, word)
        if cache_key in self._pattern_cache:
            return self._pattern_cache[cache_key]
        
        result = self._match_pattern(word, length)
        self._pattern_cache[cache_key] = result
        return result

    def _match_pattern(self, pattern, length):
        """Optimized pattern matching with early exit."""
        candidates = self.words_by_length[length]
        
        # Convert pattern to list for faster indexing
        pattern_chars = list(pattern)
        pattern_len = len(pattern_chars)
        
        for candidate in candidates:
            # Early exit if first character doesn't match (common case)
            if pattern_chars[0] != "." and pattern_chars[0] != candidate[0]:
                continue
                
            # Manual loop for better performance
            i = 0
            while i < pattern_len:
                p = pattern_chars[i]
                if p != "." and p != candidate[i]:
                    break
                i += 1
            else:
                return True
        
        return False

    def _is_match(self, candidate, pattern):
        """Optimized character-by-character comparison."""
        # This method is kept for compatibility but _match_pattern uses inline loop
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