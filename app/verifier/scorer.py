from app.verifier.matcher import MatchMetrics


class Scorer:
    """Computes confidence scores and makes match decisions."""
    
    def __init__(self):
        self._threshold = 0.80
        self._token_weight = 0.40
        self._nickname_weight = 0.35
        self._phonetic_weight = 0.15
        self._edit_weight = 0.10
    
    def compute_confidence(self, metrics: MatchMetrics) -> float:
        """Combine metrics into a single confidence score."""
        confidence = (
            metrics.token_similarity * self._token_weight +
            metrics.nickname_match * self._nickname_weight +
            metrics.phonetic_match * self._phonetic_weight +
            metrics.edit_distance * self._edit_weight
        )
        return max(0.0, min(1.0, confidence))
    
    def make_decision(self, confidence: float, order_preserved: bool) -> bool:
        """Apply threshold and order rules to make match decision."""
        return confidence >= self._threshold and order_preserved
    
    def generate_reason(
        self,
        match: bool,
        confidence: float,
        metrics: MatchMetrics
    ) -> str:
        """Create human-readable explanation for the match decision."""
        if match:
            reasons = []
            if metrics.token_similarity > 0.8:
                reasons.append("high token similarity")
            if metrics.nickname_match > 0.5:
                reasons.append("nickname match")
            if metrics.phonetic_match > 0.5:
                reasons.append("phonetic similarity")
            
            reason_text = ", ".join(reasons) if reasons else "sufficient similarity"
            return f"Match (confidence: {confidence:.2f}): {reason_text}"
        else:
            if not metrics.order_preserved:
                return f"No match (confidence: {confidence:.2f}): token order not preserved"
            elif confidence < self._threshold:
                return f"No match (confidence: {confidence:.2f}): below threshold of {self._threshold}"
            else:
                return f"No match (confidence: {confidence:.2f}): insufficient similarity"
