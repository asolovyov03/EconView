import logging
import httpx
from backend.config import settings
from backend.cache import TTLCache

logger = logging.getLogger(__name__)


class WBClientError(Exception):
    pass


class WorldBankClient:
    def __init__(self, client: httpx.AsyncClient, cache: TTLCache):
        self._client = client
        self._cache = cache

    async def fetch_countries(self) -> list[dict]:
        cache_key = "countries"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{settings.wb_base_url}/country"
        params = {"format": "json", "per_page": 400}
        try:
            resp = await self._client.get(url, params=params)
            resp.raise_for_status()
            result = resp.json()
        except httpx.HTTPError as e:
            raise WBClientError(f"WB API error: {e}") from e

        meta, data = result
        countries = []
        for item in data:
            region = item.get("region", {})
            if isinstance(region, dict) and region.get("id") == "NA":
                continue
            if item.get("capitalCity") == "":
                continue
            countries.append(item)

        self._cache.set(cache_key, countries)
        return countries

    async def fetch_series(
        self, country_iso3: str, indicator: str, date_from: int, date_to: int
    ) -> list[dict]:
        cache_key = f"series:{country_iso3}:{indicator}:{date_from}:{date_to}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{settings.wb_base_url}/country/{country_iso3}/indicator/{indicator}"
        params = {
            "format": "json",
            "per_page": 20000,
            "date": f"{date_from}:{date_to}",
        }
        try:
            resp = await self._client.get(url, params=params)
            resp.raise_for_status()
            result = resp.json()
        except httpx.HTTPError as e:
            raise WBClientError(f"WB API error: {e}") from e

        _, data = result
        self._cache.set(cache_key, data)
        return data

    async def fetch_multiple_series(
        self, country_iso3: str, indicators: list[str], date_from: int, date_to: int
    ) -> dict[str, list[dict]]:
        import asyncio

        tasks = [
            self.fetch_series(country_iso3, ind, date_from, date_to)
            for ind in indicators
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        output: dict[str, list[dict]] = {}
        for ind, result in zip(indicators, results):
            if isinstance(result, Exception):
                logger.warning("Failed to fetch %s: %s", ind, result)
                output[ind] = []
            else:
                output[ind] = result
        return output
