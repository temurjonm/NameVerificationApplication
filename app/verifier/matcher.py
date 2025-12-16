from dataclasses import dataclass
from typing import List, Dict, Set
from rapidfuzz import fuzz
from metaphone import doublemetaphone


@dataclass
class MatchMetrics:
    """Metrics from matching algorithms."""
    token_similarity: float
    edit_distance: float
    phonetic_match: float
    nickname_match: float
    order_preserved: bool


class Matcher:
    """Computes similarity metrics between token lists."""
    
    def __init__(self):
        self._nickname_map = self._build_nickname_map()
    
    def _build_nickname_map(self) -> Dict[str, Set[str]]:
        """Build bidirectional nickname mapping."""
        mappings = {
            'elizabeth': ['liz', 'beth', 'betty'],
            'william': ['will', 'bill'],
            'robert': ['rob', 'bob'],
            'richard': ['rick', 'dick'],
            'james': ['jim', 'jimmy'],
            'michael': ['mike', 'mick']
        }
        
        result = {}
        for full_name, nicknames in mappings.items():
            result[full_name] = set(nicknames)
            for nick in nicknames:
                if nick not in result:
                    result[nick] = set()
                result[nick].add(full_name)
                result[nick].update(n for n in nicknames if n != nick)
        
        return result
    
    def compute_similarity(
        self,
        target_tokens: List[str],
        candidate_tokens: List[str]
    ) -> MatchMetrics:
        """Compute all matching metrics between token lists."""
        token_sim = self._compute_token_similarity(target_tokens, candidate_tokens)
        edit_dist = self._compute_edit_distance(target_tokens, candidate_tokens)
        phonetic = self._compute_phonetic_match(target_tokens, candidate_tokens)
        nickname = self._compute_nickname_match(target_tokens, candidate_tokens)
        order = self._check_order_preserved(target_tokens, candidate_tokens)
        
        return MatchMetrics(
            token_similarity=token_sim,
            edit_distance=edit_dist,
            phonetic_match=phonetic,
            nickname_match=nickname,
            order_preserved=order
        )
    
    def _compute_token_similarity(
        self,
        target_tokens: List[str],
        candidate_tokens: List[str]
    ) -> float:
        """Compute token-level similarity."""
        if not target_tokens or not candidate_tokens:
            return 0.0
        
        matches = 0
        for t_token in target_tokens:
            for c_token in candidate_tokens:
                if t_token == c_token:
                    matches += 1
                    break
        
        return matches / max(len(target_tokens), len(candidate_tokens))
    
    def _compute_edit_distance(
        self,
        target_tokens: List[str],
        candidate_tokens: List[str]
    ) -> float:
        """Compute normalized edit distance similarity."""
        if not target_tokens or not candidate_tokens:
            return 0.0
        
        total_similarity = 0.0
        comparisons = 0
        
        for t_token in target_tokens:
            for c_token in candidate_tokens:
                similarity = fuzz.ratio(t_token, c_token) / 100.0
                total_similarity += similarity
                comparisons += 1
        
        return total_similarity / comparisons if comparisons > 0 else 0.0
    
    def _compute_phonetic_match(
        self,
        target_tokens: List[str],
        candidate_tokens: List[str]
    ) -> float:
        """Compute phonetic similarity using Double Metaphone."""
        if not target_tokens or not candidate_tokens:
            return 0.0
        
        matches = 0
        total = 0
        
        for t_token in target_tokens:
            t_primary, t_secondary = doublemetaphone(t_token)
            for c_token in candidate_tokens:
                c_primary, c_secondary = doublemetaphone(c_token)
                
                if t_primary and c_primary and (
                    t_primary == c_primary or
                    t_primary == c_secondary or
                    t_secondary == c_primary or
                    (t_secondary and t_secondary == c_secondary)
                ):
                    matches += 1
                    break
            total += 1
        
        return matches / total if total > 0 else 0.0
    
    def _compute_nickname_match(
        self,
        target_tokens: List[str],
        candidate_tokens: List[str]
    ) -> float:
        """Compute nickname matching score."""
        if not target_tokens or not candidate_tokens:
            return 0.0
        
        matches = 0
        
        for t_token in target_tokens:
            for c_token in candidate_tokens:
                if self._are_nicknames(t_token, c_token):
                    matches += 1
                    break
        
        return matches / max(len(target_tokens), len(candidate_tokens))
    
    def _are_nicknames(self, token1: str, token2: str) -> bool:
        """Check if two tokens are nicknames of each other."""
        if token1 == token2:
            return True
        
        if token1 in self._nickname_map:
            if token2 in self._nickname_map[token1]:
                return True
        
        return False
    
    def _check_order_preserved(
        self,
        target_tokens: List[str],
        candidate_tokens: List[str]
    ) -> bool:
        """Check if token order is preserved between lists."""
        if not target_tokens or not candidate_tokens:
            return False
        
        if len(target_tokens) != len(candidate_tokens):
            return False
        
        return target_tokens == candidate_tokens
