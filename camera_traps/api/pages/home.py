import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash import Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate

from camera_traps.api.components import create_card
from camera_traps.api.config import CONTINUOUS_SCALE, GRAPH_CONFIG
from camera_traps.db.config import db
from camera_traps.settings import SITES

dash.register_page(__name__, path="/", title="Home", order=0)


layout = dmc.Container(
    fluid=True,
    p="md",
    children=[
        dmc.Stack(
            gap="md",
            children=[
                dmc.Grid(
                    gutter="md",
                    children=[
                        dmc.GridCol(
                            span=5,
                            children=dmc.Stack(
                                gap="md",
                                children=[
                                    dmc.SimpleGrid(
                                        cols=3,
                                        spacing="md",
                                        children=[
                                            create_card(id="kpi-total-videos", title="Total videos"),
                                            create_card(id="kpi-total-tracks", title="Total tracks"),
                                            create_card(id="kpi-total-species", title="Total species"),
                                        ],
                                    ),
                                    dmc.Paper(
                                        withBorder=True,
                                        radius="md",
                                        p="xs",
                                        style={"height": "40vh"},
                                        children=dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=[
                                                dmc.Text(
                                                    children=[
                                                        html.Span(
                                                            id="camera-map-value",
                                                            children="0",
                                                            style={"fontWeight": 500},
                                                        ),
                                                        " · sites",
                                                    ],
                                                    size="xs",
                                                    c="dimmed",
                                                    fw=300,
                                                    tt="uppercase",
                                                    mb="xs",
                                                ),
                                                dcc.Graph(
                                                    id="camera-map",
                                                    config=GRAPH_CONFIG | {"scrollZoom": True},
                                                    style={"height": "35vh", "width": "100%"},
                                                ),
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        dmc.GridCol(
                            span=3,
                            children=dmc.Paper(
                                withBorder=True,
                                radius="md",
                                p="md",
                                style={"height": "100%"},
                                children=dmc.Stack(
                                    gap="xs",
                                    justify="space-between",
                                    style={"height": "100%"},
                                    children=[
                                        dmc.Text(children="Processing status", size="lg", fw=400, ta="center"),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="status-chart",
                                                config=GRAPH_CONFIG,
                                                style={"height": "18.5vh", "width": "100%"},
                                            ),
                                        ),
                                        dmc.Divider(variant="solid"),
                                        dmc.Text(children="Computational timing", size="lg", fw=400, ta="center"),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="computational-timing",
                                                config=GRAPH_CONFIG,
                                                style={"height": "18.5vh", "width": "100%"},
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ),
                        dmc.GridCol(
                            span=4,
                            children=dmc.Paper(
                                withBorder=True,
                                radius="md",
                                p="md",
                                style={"height": "100%"},
                                children=dmc.Stack(
                                    gap="xs",
                                    children=[
                                        dmc.Text(
                                            children="Predicted species distribution", size="lg", fw=400, ta="center"
                                        ),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="species-histogram",
                                                config=GRAPH_CONFIG,
                                                style={"height": "44vh", "width": "100%"},
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ),
                    ],
                ),
                dmc.Grid(
                    gutter="md",
                    children=[
                        dmc.GridCol(
                            span=6,
                            children=dmc.Paper(
                                withBorder=True,
                                radius="md",
                                p="md",
                                style={"height": "36vh"},
                                children=dmc.Stack(
                                    gap="xs",
                                    children=[
                                        dmc.Text(children="Daily tracks flow", size="lg", fw=400, ta="center"),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="daily-sightings-chart",
                                                config=GRAPH_CONFIG,
                                                style={"height": "30vh", "width": "100%"},
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ),
                        dmc.GridCol(
                            span=6,
                            children=dmc.Paper(
                                withBorder=True,
                                radius="md",
                                p="md",
                                style={"height": "36vh"},
                                children=dmc.Stack(
                                    gap="xs",
                                    children=[
                                        dmc.Text(children="Hourly tracks distribution", size="lg", fw=400, ta="center"),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="hourly-heatmap-chart",
                                                config=GRAPH_CONFIG,
                                                style={"height": "30vh", "width": "100%"},
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        )
    ],
)


@callback(
    Output("kpi-total-videos", "children"),
    Output("kpi-total-tracks", "children"),
    Output("kpi-total-species", "children"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_kpi(date_range: list[str | None], sites: list[str]):
    """Display the KPI cards"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_kpi = db.run_sql_file("home/get_kpi.sql", parameters=params)
    df_species = db.run_sql_file("home/get_species.sql", parameters=params)

    return (
        f"{df_kpi['total_videos'].sum():,.0f}",
        f"{df_kpi['total_tracks'].sum():,.0f}",
        f"{df_species['species'].nunique():,.0f}",
    )


@callback(
    Output("camera-map", "figure"),
    Output("camera-map-value", "children"),
    Input("date-range-picker", "value"),
    Input("theme-radio", "value"),
    Input("site-filter", "value"),
)
def update_map(date_range: list[str | None], theme: str, sites: list[str]):
    """Display camera trap locations on the map"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_kpi = db.run_sql_file("home/get_kpi.sql", parameters=params)
    df_location = pd.DataFrame.from_dict(SITES, orient="index").reset_index(names="site")
    df_trap = pd.merge(df_location, df_kpi, on="site", how="right")

    # Create figure.
    fig = px.scatter_mapbox(
        df_trap,
        lat="lat",
        lon="lon",
        custom_data=["name", "total_videos", "total_tracks", "total_species"],
    )
    fig.update_traces(
        marker=dict(size=13, color="#E07A5F", opacity=1.0),
        hovertemplate=(
            "<b>Site</b>: %{customdata[0]}<br><br>"
            "<b>Total videos</b>: %{customdata[1]}<br>"
            "<b>Tracked individuals</b>: %{customdata[2]}<br>"
            "<b>Detected species</b>: %{customdata[3]}"
            "<extra></extra>"
        ),
    )
    fig.add_trace(
        go.Scattermapbox(
            lat=df_trap["lat"],
            lon=df_trap["lon"],
            mode="markers",
            marker=dict(size=26, color="#E07A5F", opacity=0.35),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
        mapbox=dict(
            center=go.layout.mapbox.Center(lat=44.6337, lon=9.7314),
            style="open-street-map",
            zoom=12,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
    )

    return fig, len(df_trap)


@callback(
    Output("status-chart", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_status_chart(date_range: list[str | None], sites: list[str]):
    """Display donut chart of video processing status"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_status = db.run_sql_file("home/get_status.sql", parameters=params)

    # Create figure.
    fig = px.pie(
        df_status,
        names="status",
        values="total",
        hole=0.5,
        color_discrete_sequence=pio.templates[pio.templates.default].layout.colorway[1:],
    )
    fig.update_traces(
        textinfo="percent+value",
        hovertemplate="<b>Status</b>: %{label}<br>"
        "<b>N° of videos</b>: %{value}<br>"
        "<b>Percentage</b>: %{percent}<br>"
        "<extra></extra>",
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=15, b=15),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=0,
            title_text="",
        ),
        autosize=True,
    )

    return fig


@callback(
    Output("computational-timing", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_computational_timing(date_range: list[str | None], sites: list[str]):
    """Display horizontal box plot of queue and processing times"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_timing = db.run_sql_file("home/get_computational_timing.sql", parameters=params)
    df_melted = df_timing.melt(
        value_vars=["queue_time", "processing_time"],
        var_name="phase",
        value_name="seconds",
    ).replace({"queue_time": "Queue", "processing_time": "Execution"})

    # Create figure.
    fig = px.box(
        df_melted,
        x="seconds",
        y="phase",
        color="phase",
        orientation="h",
        points="outliers",
        color_discrete_sequence=pio.templates[pio.templates.default].layout.colorway[1:],
    )
    fig.update_traces(
        opacity=0.75,
        name="",
    )
    fig.update_layout(
        showlegend=False,
        hovermode="y unified",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.9)"),
        xaxis=dict(title="Time (s)", hoverformat=".1f"),
        yaxis=dict(title=""),
        margin=dict(l=20, r=20, t=10, b=20),
        autosize=True,
    )

    return fig


@callback(
    Output("species-histogram", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_species_histogram(date_range: list[str | None], sites: list[str]):
    """Display horizontal bar chart of detected species"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_species = db.run_sql_file("home/get_species.sql", parameters=params)
    df_species = df_species.groupby("species", as_index=False).agg(total=("total", "sum"))

    # Create figure.
    fig = px.bar(
        df_species,
        x="total",
        y="species",
        orientation="h",
    )
    fig.update_traces(hovertemplate="<b>N° of tracks</b>: %{x}<br>" "<b>Species</b>: %{y}<br>" "<extra></extra>")
    fig.update_layout(
        legend=dict(title_text=""),
        xaxis=dict(title="Number of tracks"),
        yaxis=dict(title="Species"),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
    )

    return fig


@callback(
    Output("daily-sightings-chart", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_daily_sightings(date_range: list[str | None], sites: list[str]):
    """Display area chart of daily detected animals"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_daily = db.run_sql_file("home/get_tracked_individuals.sql", parameters=params)
    df_filtered = (
        df_daily.set_index("created_at")
        .reindex(pd.date_range(start=date_range[0], end=date_range[1], freq="D"))
        .rename_axis("created_at")
        .reset_index()
        .fillna(0)
    )

    # Create figure.
    fig = go.Figure(
        [
            go.Scatter(
                x=df_filtered["created_at"],
                y=df_filtered["total"],
                fill="tozeroy",
                mode="markers+lines",
                fillgradient=dict(
                    type="vertical",
                    colorscale=CONTINUOUS_SCALE,
                ),
            )
        ]
    )
    fig.update_traces(
        hovertemplate="<b>N° of tracks</b>: %{y}<br>" "<b>Datetime</b>: %{x}, %{x|%a}" "<extra></extra>",
    )
    fig.update_layout(
        showlegend=False,
        xaxis=dict(title="Datetime"),
        yaxis=dict(title="Number of tracks"),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
    )

    return fig


@callback(
    Output("hourly-heatmap-chart", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_hourly_flow(date_range: list[str | None], sites: list[str]):
    """Display hourly heatmap of detected animals"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_hourly = db.run_sql_file("home/get_tracked_individuals_hourly.sql", parameters=params)
    df_filtered = (
        df_hourly.set_index("created_at")
        .reindex(pd.date_range(start=f"{date_range[0]} 00:00:00", end=f"{date_range[1]} 23:00:00", freq="h"))
        .rename_axis("created_at")
        .reset_index()
        .fillna(0)
    )

    df_filtered["date"] = df_filtered["created_at"].dt.date
    df_filtered["hour"] = df_filtered["created_at"].dt.hour
    df_pivot = df_filtered.pivot_table(index="hour", columns="date", values="total", aggfunc="sum", fill_value=0)
    df_pivot.index = [f"{int(h):02d}:00" for h in df_pivot.index]

    # Create figure.
    fig = px.imshow(df_pivot, aspect="auto", color_continuous_scale=CONTINUOUS_SCALE)
    fig.update_traces(
        hovertemplate="<b>N° of tracks</b>: %{z}<br><br>"
        "<b>Datetime</b>: %{x}<br>"
        "<b>Hour</b>: %{y}<br>"
        "<extra></extra>"
    )
    fig.update_layout(
        xaxis=dict(title="Datetime", showgrid=False, zeroline=False),
        yaxis=dict(title="Hour", showgrid=False, zeroline=False),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
        coloraxis_colorbar=dict(title="Trackers"),
        coloraxis_colorbar_title_side="right",
        hoverlabel=dict(
            bgcolor="#2E6F40",
            bordercolor="#2E6F40",
        ),
    )

    return fig
