import re


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Limit length
    text = text[:500]
    
    # Remove potentially dangerous patterns
    text = re.sub(r'[<>{}\\]', '', text)
    
    return text
