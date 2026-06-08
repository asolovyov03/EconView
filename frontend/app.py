import streamlit as st
from frontend.api_client import get_countries, get_dashboard
from frontend.layout import CATEGORY_LABELS, render_kpi, render_category_tab

st.set_page_config(
    page_title="EconView",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("EconView — социально-экономический дашборд")

try:
    countries = get_countries()
except Exception:
    st.error("Не удалось загрузить список стран. Убедитесь, что бэкенд запущен.")
    st.stop()

country_names = {c["iso3"]: c["name"] for c in countries}
default_idx = list(country_names.keys()).index("RUS") if "RUS" in country_names else 0
iso3_list = sorted(country_names.keys(), key=lambda k: (k != "RUS", country_names[k]))
selected_iso3 = st.selectbox(
    "Страна",
    options=iso3_list,
    format_func=lambda iso3: country_names.get(iso3, iso3),
    index=iso3_list.index("RUS") if "RUS" in iso3_list else 0,
)

col_left, col_right = st.columns(2)
with col_left:
    date_from = st.slider("Год начала", 1990, 2023, 2000, key="date_from")
with col_right:
    date_to = st.slider("Год окончания", 1991, 2024, 2024, key="date_to")

if date_from >= date_to:
    st.error("Год начала должен быть меньше года окончания")
    st.stop()

with st.spinner("Загружаем данные..."):
    try:
        data = get_dashboard(selected_iso3, int(date_from), int(date_to))
    except Exception:
        st.error("Не удалось загрузить данные с бэкенда. Проверьте соединение.")
        st.stop()

country_info = data.get("country", {})
if country_info:
    st.caption(
        f"{country_info.get('name', selected_iso3)} | "
        f"{country_info.get('region', '')} | "
        f"{country_info.get('income_level', '')}"
    )

series = data.get("series", {})

st.subheader("Ключевые показатели (последний доступный год)")
render_kpi(series)

st.subheader("Индикаторы по категориям")
tabs = st.tabs(list(CATEGORY_LABELS.values()))
for tab, (cat_key, _) in zip(tabs, CATEGORY_LABELS.items()):
    with tab:
        render_category_tab(series, cat_key)
