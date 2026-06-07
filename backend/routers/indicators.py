from fastapi import APIRouter, Depends, HTTPException, Query
from backend.wb_client import WorldBankClient, WBClientError
from backend.indicators import INDICATORS, CATEGORIES_RU
from backend.schemas import DataPoint, SeriesResponse, SeriesWithDerived
from backend.computations import year_over_year, cagr, normalize_to_base
from backend.dependencies import get_wb_client

router = APIRouter()


def _build_series(
    raw_data: list[dict],
    country_iso3: str,
    indicator_code: str,
    derive: bool = False,
) -> SeriesResponse | SeriesWithDerived:
    meta = INDICATORS[indicator_code]
    points: list[DataPoint] = []
    for entry in raw_data:
        try:
            year = int(entry["date"])
        except (ValueError, TypeError):
            continue
        value = entry.get("value")
        points.append(DataPoint(year=year, value=value))
    points.sort(key=lambda p: p.year)

    if not derive:
        return SeriesResponse(
            country_iso3=country_iso3,
            indicator_code=indicator_code,
            indicator_name=meta.name_ru,
            unit=meta.unit,
            data=points,
        )

    series_tuples = [(p.year, p.value) for p in points]
    yoy_data = year_over_year(series_tuples)
    base_year = points[0].year if points else 2000
    indexed_data = normalize_to_base(series_tuples, base_year)
    computed_cagr = cagr(series_tuples)

    return SeriesWithDerived(
        country_iso3=country_iso3,
        indicator_code=indicator_code,
        indicator_name=meta.name_ru,
        unit=meta.unit,
        data=points,
        yoy=[DataPoint(year=y, value=v) for y, v in yoy_data],
        indexed=[DataPoint(year=y, value=v) for y, v in indexed_data],
        cagr=computed_cagr,
    )


@router.get("/indicators")
async def list_indicators():
    return {
        "indicators": {
            code: {
                "code": m.code,
                "name_ru": m.name_ru,
                "category": m.category,
                "category_ru": CATEGORIES_RU[m.category],
                "unit": m.unit,
                "higher_is_better": m.higher_is_better,
            }
            for code, m in INDICATORS.items()
        },
        "categories": CATEGORIES_RU,
    }


@router.get("/series/{iso3}/{indicator}", response_model=SeriesResponse | SeriesWithDerived)
async def get_series(
    iso3: str,
    indicator: str,
    date_from: int = Query(2000),
    date_to: int = Query(2024),
    derive: bool = Query(False),
    client: WorldBankClient = Depends(get_wb_client),
):
    if indicator not in INDICATORS:
        raise HTTPException(status_code=404, detail=f"Indicator {indicator} not found")
    try:
        raw = await client.fetch_series(iso3.upper(), indicator, date_from, date_to)
    except WBClientError:
        raise HTTPException(status_code=502, detail="World Bank API unavailable")
    return _build_series(raw, iso3.upper(), indicator, derive=derive)


@router.get("/dashboard/{iso3}")
async def get_dashboard(
    iso3: str,
    date_from: int = Query(2000),
    date_to: int = Query(2024),
    client: WorldBankClient = Depends(get_wb_client),
):
    indicator_codes = list(INDICATORS.keys())
    try:
        raw_series = await client.fetch_multiple_series(
            iso3.upper(), indicator_codes, date_from, date_to
        )
    except WBClientError:
        raise HTTPException(status_code=502, detail="World Bank API unavailable")

    series_result: dict[str, dict] = {}
    for code in indicator_codes:
        raw = raw_series.get(code, [])
        built = _build_series(raw, iso3.upper(), code, derive=True)
        series_result[code] = built.model_dump()

    country_info = None
    try:
        countries = await client.fetch_countries()
    except WBClientError:
        country_info = None
    else:
        for c in countries:
            if c.get("id") == iso3.upper():
                region = c.get("region", {})
                income = c.get("incomeLevel", {})
                country_info = {
                    "iso3": c.get("id", ""),
                    "iso2": c.get("iso2Code", ""),
                    "name": c.get("name", ""),
                    "region": region.get("value", "") if isinstance(region, dict) else "",
                    "income_level": income.get("value", "") if isinstance(income, dict) else "",
                }
                break

    return {
        "country": country_info,
        "period": {"from": date_from, "to": date_to},
        "series": series_result,
    }
