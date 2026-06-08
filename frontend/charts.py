import plotly.graph_objects as go


def format_big_number(value: float | None, unit: str) -> str:
    if value is None:
        return "—"
    if unit == "%":
        return f"{value:.1f} %"
    if unit == "index":
        return f"{value:.2f}"
    if unit == "USD":
        if abs(value) >= 1e12:
            return f"{value / 1e12:.2f} трлн USD"
        elif abs(value) >= 1e9:
            return f"{value / 1e9:.2f} млрд USD"
        return f"{value:,.0f} USD"
    if unit == "people":
        if abs(value) >= 1e9:
            return f"{value / 1e9:.2f} млрд чел."
        elif abs(value) >= 1e6:
            return f"{value / 1e6:.2f} млн чел."
        return f"{value:,.0f} чел."
    if unit == "years":
        return f"{value:.1f} лет"
    if unit == "births/woman":
        return f"{value:.2f} рожд./жен."
    return f"{value:,.2f}"


def _build_line_chart(
    years: list[int],
    values: list[float | None],
    title: str,
    yaxis_title: str,
    log_scale: bool = False,
) -> go.Figure:
    fig = go.Figure()
    x = []
    y = []
    for yr, val in zip(years, values):
        if val is not None:
            x.append(yr)
            y.append(val)
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        line=dict(width=2),
        marker=dict(size=5),
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Год",
        yaxis_title=yaxis_title,
        template="plotly_white",
        margin=dict(l=50, r=20, t=40, b=40),
        height=400,
    )
    if log_scale:
        fig.update_yaxes(type="log")
    return fig


def chart_level(series: dict, indicator_code: str, log_scale: bool = False) -> go.Figure:
    data = series["data"]
    years = [p["year"] for p in data]
    values = [p["value"] for p in data]
    unit = series["unit"]
    unit_labels = {
        "USD": "USD",
        "%": "%",
        "people": "чел.",
        "years": "лет",
        "index": "индекс",
        "births/woman": "рожд./жен.",
    }
    return _build_line_chart(
        years, values,
        title=f"{series['indicator_name']} (уровень)",
        yaxis_title=unit_labels.get(unit, unit),
        log_scale=log_scale and unit == "USD",
    )


def chart_yoy(series: dict) -> go.Figure:
    yoy_data = series.get("yoy", [])
    years = [p["year"] for p in yoy_data]
    values = [p["value"] for p in yoy_data]
    return _build_line_chart(
        years, values,
        title=f"{series['indicator_name']} (YoY, %)",
        yaxis_title="%",
    )


def chart_indexed(series: dict) -> go.Figure:
    idx_data = series.get("indexed", [])
    years = [p["year"] for p in idx_data]
    values = [p["value"] for p in idx_data]
    return _build_line_chart(
        years, values,
        title=f"{series['indicator_name']} (индекс)",
        yaxis_title="Индекс",
    )
