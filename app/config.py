from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class VerifierConfig:
    """Configuration for name verification."""
    
    confidence_threshold: float = 0.80
    token_similarity_weight: float = 0.40
    nickname_weight: float = 0.35
    phonetic_weight: float = 0.15
    edit_distance_weight: float = 0.10
    
    compound_patterns: List[str] = field(default_factory=lambda: [
        'abdul', 'al', 'ibn', 'bin'
    ])
    
    nickname_map: Dict[str, List[str]] = field(default_factory=lambda: {
        'elizabeth': ['liz', 'beth', 'betty'],
        'william': ['will', 'bill'],
        'robert': ['rob', 'bob'],
        'richard': ['rick', 'dick'],
        'james': ['jim', 'jimmy'],
        'michael': ['mike', 'mick']
    })


config = VerifierConfig()
