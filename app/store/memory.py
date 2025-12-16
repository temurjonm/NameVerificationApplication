from typing import Optional
from threading import Lock


class NameStore:
    """Thread-safe in-memory storage for the current target name."""
    
    def __init__(self):
        self._target_name: Optional[str] = None
        self._lock = Lock()
    
    def set_target(self, name: str) -> None:
        """Store the current target name, overwriting any previous value."""
        with self._lock:
            self._target_name = name
    
    def get_target(self) -> Optional[str]:
        """Retrieve the current target name."""
        with self._lock:
            return self._target_name
