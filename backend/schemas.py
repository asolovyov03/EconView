from pydantic import BaseModel


class Country(BaseModel):
    iso3: str
    iso2: str
    name: str
    region: str
    income_level: str


class DataPoint(BaseModel):
    year: int
    value: float | None


class SeriesResponse(BaseModel):
    country_iso3: str
    indicator_code: str
    indicator_name: str
    unit: str
    data: list[DataPoint]


class SeriesWithDerived(SeriesResponse):
    yoy: list[DataPoint] | None = None
    indexed: list[DataPoint] | None = None
    cagr: float | None = None
