import time
from typing import Any

CACHE_VERSION = "v1"


class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self._store: dict[str, tuple[float, Any]] = {}

    def _versioned(self, key: str) -> str:
        return f"{CACHE_VERSION}:{key}"

    def get(self, key: str) -> Any | None:
        item = self._store.get(self._versioned(key))
        if item is None:
            return None
        expires_at, value = item
        if time.time() > expires_at:
            del self._store[self._versioned(key)]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._store[self._versioned(key)] = (time.time() + self.ttl, value)

    def clear(self) -> int:
        n = len(self._store)
        self._store.clear()
        return n
