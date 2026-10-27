import plotly.io as pio

pio.templates[pio.templates.default].layout.update(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(gridcolor="rgba(0,0,0,0)"),
    yaxis=dict(gridcolor="rgba(200, 200, 200, 0.2)"),
    colorway=["#2E6F40", "#E07A5F", "#3D5A80", "#F2CC8F", "#81559B"],
)

GRAPH_CONFIG = {
    "displayModeBar": False,
    "displaylogo": False,
}

CONTINUOUS_SCALE = [
    (0.0, "rgba(133, 193, 150, 0.0)"),
    (0.5, "rgba(133, 193, 150, 0.3)"),
    (1.0, "rgba(133, 193, 150, 0.8)"),
]

STATUS_COLOR_MAP = {
    "COMPLETED": "#2d6a3e",
    "PROCESSING": "#3b82a6",
    "PENDING": "#e09f3e",
    "FAILED": "#c94a4a",
}

EDIT_COLOR_MAP = {
    "Confirmed": "#E07A5F",
    "Relabeled": "#3D5A80",
    "Added": "#F2CC8F",
}
