from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.cache import TTLCache
from backend.wb_client import WorldBankClient
from backend.dependencies import set_clients, get_cache
from backend.routers.countries import router as countries_router
from backend.routers.indicators import router as indicators_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    cache = TTLCache(ttl_seconds=settings.cache_ttl_seconds)
    http = httpx.AsyncClient(timeout=settings.wb_timeout_seconds)
    wb = WorldBankClient(client=http, cache=cache)
    set_clients(cache, http, wb)
    yield
    await http.aclose()


app = FastAPI(
    title="EconView API",
    description="Прокси к World Bank API с расчётами",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/admin/cache/clear")
async def clear_cache(cache: TTLCache = Depends(get_cache)):
    n = cache.clear()
    return {"cleared": n}


app.include_router(countries_router)
app.include_router(indicators_router)
