import streamlit as st
from frontend.charts import chart_level, chart_yoy, chart_indexed, format_big_number


INDICATOR_CATEGORIES = {
    "economy": ["NY.GDP.MKTP.CD", "NY.GDP.PCAP.CD", "NY.GDP.MKTP.KD.ZG", "FP.CPI.TOTL.ZG", "NE.TRD.GNFS.ZS"],
    "labor": ["SL.UEM.TOTL.ZS", "SL.TLF.CACT.ZS"],
    "demography": ["SP.POP.TOTL", "SP.DYN.LE00.IN", "SP.DYN.TFRT.IN", "SP.URB.TOTL.IN.ZS"],
    "education": ["SE.XPD.TOTL.GD.ZS", "SE.ADT.LITR.ZS"],
    "poverty": ["SI.POV.GINI", "SI.POV.DDAY"],
}

CATEGORY_LABELS = {
    "economy": "Экономика",
    "labor": "Рынок труда",
    "demography": "Демография",
    "education": "Образование",
    "poverty": "Бедность и неравенство",
}


def _safe_last_value(series: dict) -> float | None:
    points = series.get("data", [])
    for p in reversed(points):
        if p["value"] is not None:
            return p["value"]
    return None


def _safe_last_yoy(series: dict) -> float | None:
    yoy = series.get("yoy", [])
    for p in reversed(yoy):
        if p["value"] is not None:
            return p["value"]
    return None


def render_kpi(series: dict[str, dict]):
    indicators = {
        "NY.GDP.MKTP.CD": "ВВП, текущие USD",
        "NY.GDP.PCAP.CD": "ВВП на душу, USD",
        "FP.CPI.TOTL.ZG": "Инфляция (CPI), %",
        "SL.UEM.TOTL.ZS": "Безработица, %",
    }
    series_subset = {k: series[k] for k in indicators if k in series}
    cols = st.columns(len(series_subset))
    for col, (code, label) in zip(cols, indicators.items()):
        s = series.get(code)
        with col:
            if s and s.get("data"):
                val = _safe_last_value(s)
                delta_val = _safe_last_yoy(s)
                unit = s.get("unit", "")
                st.metric(
                    label=label,
                    value=format_big_number(val, unit),
                    delta=f"{delta_val:+.1f}% YoY" if delta_val is not None else None,
                )
            else:
                st.metric(label=label, value="—")


def render_category_tab(series: dict[str, dict], category: str):
    codes = INDICATOR_CATEGORIES.get(category, [])
    for code in codes:
        s = series.get(code)
        if not s or not s.get("data"):
            st.info(f"Нет данных по индикатору {code}")
            continue

        mode = st.radio(
            f"Режим: {s['indicator_name']}",
            ["Уровень", "YoY %", "Индекс к базе"],
            horizontal=True,
            key=f"mode_{code}",
        )

        log_scale = False
        if s["unit"] == "USD" and mode == "Уровень":
            log_scale = st.checkbox("Log scale", key=f"log_{code}")

        if mode == "Уровень":
            fig = chart_level(s, code, log_scale=log_scale)
        elif mode == "YoY %":
            fig = chart_yoy(s)
        else:
            fig = chart_indexed(s)

        st.plotly_chart(fig, width="stretch")
