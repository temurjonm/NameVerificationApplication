import re
import unicodedata


class Normalizer:
    """Normalizes name strings for comparison."""
    
    def __init__(self):
        self._prefix_patterns = {
            'al': 'al',
            'ibn': 'ibn',
            'bin': 'bin'
        }
    
    def normalize(self, name: str) -> str:
        """Apply all normalization rules to a name string."""
        result = name.lower()
        result = unicodedata.normalize('NFC', result)
        result = re.sub(r"[-'.]", '', result)
        result = re.sub(r'\s+', ' ', result)
        result = result.strip()
        result = self._standardize_prefixes(result)
        return result
    
    def _standardize_prefixes(self, name: str) -> str:
        """Standardize known prefixes to consistent form."""
        tokens = name.split()
        standardized = []
        
        for token in tokens:
            if token in self._prefix_patterns:
                standardized.append(self._prefix_patterns[token])
            else:
                standardized.append(token)
        
        return ' '.join(standardized)
