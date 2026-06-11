# EconView — socioeconomic dashboard of core country data based on World Bank Data

Dashboard is based on [World Bank Open Data API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures).

It is a study project.

## Technologies 

- Python 3.11+
- FastAPI + uvicorn (backend part)
- Streamlit + Plotly (frontend)
- pandas, httpx, Pydantic v2

## Quick Start

```bash
# 1. Create venv and install dependencies
make install

# 2. Start backend
make backend

# 3. Start frontend
make frontend
```

By default backend and frontend works locally on these adresses:

Backend: http://localhost:8000/docs (Swagger)  
Frontend: http://localhost:8501

## Indicators

| Category | Indicators |
|---|---|
| Economy | GDP, GDP per capita, GDP growth, CPI, Trade |
| Labor | Unemployment, Labor force participation rate |
| Demography | Population, Life expectancy, Birth rate, Urban population |
| Education | Education expenses, Literacy rate |
| Poverty and inequality | Gini coefficient, Poverty rate based on $2.15/day |

## API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Check |
| GET | `/countries` | Countries list |
| GET | `/indicators` | Indicators data |
| GET | `/series/{iso3}/{indicator}` | Series data by country and indicator |
| GET | `/dashboard/{iso3}` | All 15 indicators by country |
| POST | `/admin/cache/clear` | Clear in-memory cache |

## Screenshots
<img width="1368" height="434" alt="image" src="https://github.com/user-attachments/assets/df7ec72e-ddfb-494f-890a-04ca867d30ee" />

<img width="1359" height="669" alt="image" src="https://github.com/user-attachments/assets/2481925d-7d48-4d1b-8a73-5b2f68721ab2" />

