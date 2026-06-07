import httpx
from backend.cache import TTLCache
from backend.wb_client import WorldBankClient

_cache: TTLCache | None = None
_http: httpx.AsyncClient | None = None
_wb: WorldBankClient | None = None


def set_clients(cache: TTLCache, http: httpx.AsyncClient, wb: WorldBankClient) -> None:
    global _cache, _http, _wb
    _cache = cache
    _http = http
    _wb = wb


def get_cache() -> TTLCache:
    assert _cache is not None
    return _cache


def get_http_client() -> httpx.AsyncClient:
    assert _http is not None
    return _http


def get_wb_client() -> WorldBankClient:
    assert _wb is not None
    return _wb
