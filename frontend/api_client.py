import os
import requests
import streamlit as st

BASE = os.getenv("BACKEND_URL", "http://localhost:8000")


@st.cache_data(ttl=600)
def get_countries():
    r = requests.get(f"{BASE}/countries", timeout=15)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=600)
def get_dashboard(iso3: str, date_from: int, date_to: int):
    r = requests.get(
        f"{BASE}/dashboard/{iso3}",
        params={"date_from": date_from, "date_to": date_to},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()
