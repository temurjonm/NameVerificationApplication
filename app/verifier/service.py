from dataclasses import dataclass
from app.store.memory import NameStore
from app.verifier.normalizer import Normalizer
from app.verifier.tokenizer import Tokenizer
from app.verifier.matcher import Matcher
from app.verifier.scorer import Scorer


@dataclass
class VerifyResponse:
    """Response from verification."""
    match: bool
    confidence: float
    reason: str


class NameVerifier:
    """Verifies candidate names against stored target."""
    
    def __init__(self, store: NameStore):
        self._store = store
        self._normalizer = Normalizer()
        self._tokenizer = Tokenizer()
        self._matcher = Matcher()
        self._scorer = Scorer()
    
    def verify(self, candidate: str) -> VerifyResponse:
        """Verify candidate against stored target name."""
        target = self._store.get_target()
        if target is None:
            raise ValueError("No target name in store")
        
        target_normalized = self._normalizer.normalize(target)
        candidate_normalized = self._normalizer.normalize(candidate)
        
        target_tokens = self._tokenizer.tokenize(target_normalized)
        candidate_tokens = self._tokenizer.tokenize(candidate_normalized)
        
        metrics = self._matcher.compute_similarity(target_tokens, candidate_tokens)
        confidence = self._scorer.compute_confidence(metrics)
        match = self._scorer.make_decision(confidence, metrics.order_preserved)
        reason = self._scorer.generate_reason(match, confidence, metrics)
        
        return VerifyResponse(
            match=match,
            confidence=confidence,
            reason=reason
        )
