from typing import List


class Tokenizer:
    """Splits normalized names into tokens and merges compound patterns."""
    
    def __init__(self):
        self._compound_prefixes = {'abdul', 'al', 'ibn', 'bin'}
    
    def tokenize(self, normalized_name: str) -> List[str]:
        """Split name into tokens and merge known compound patterns."""
        tokens = normalized_name.split()
        return self._merge_compounds(tokens)
    
    def _merge_compounds(self, tokens: List[str]) -> List[str]:
        """Merge known compound patterns into single tokens."""
        if len(tokens) < 2:
            return tokens
        
        result = []
        i = 0
        
        while i < len(tokens):
            if tokens[i] in self._compound_prefixes and i + 1 < len(tokens):
                result.append(tokens[i] + tokens[i + 1])
                i += 2
            else:
                result.append(tokens[i])
                i += 1
        
        return result
