from fastapi import APIRouter, Depends
from backend.wb_client import WorldBankClient, WBClientError
from backend.schemas import Country
from backend.dependencies import get_wb_client

router = APIRouter()


@router.get("/countries", response_model=list[Country])
async def list_countries(client: WorldBankClient = Depends(get_wb_client)):
    try:
        raw = await client.fetch_countries()
    except WBClientError:
        from fastapi import HTTPException
        raise HTTPException(status_code=502, detail="World Bank API unavailable")
    result = []
    for c in raw:
        name = c.get("name", "")
        iso3 = c.get("id", "")
        iso2 = c.get("iso2Code", "")
        region = c.get("region", {})
        region_name = region.get("value", "") if isinstance(region, dict) else ""
        income = c.get("incomeLevel", {})
        income_name = income.get("value", "") if isinstance(income, dict) else ""
        result.append(Country(
            iso3=iso3,
            iso2=iso2,
            name=name,
            region=region_name,
            income_level=income_name,
        ))
    return result
