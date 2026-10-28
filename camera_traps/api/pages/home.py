import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash import Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate

from camera_traps.api.components import create_card, create_title
from camera_traps.api.config import CONTINUOUS_SCALE, GRAPH_CONFIG, STATUS_COLOR_MAP
from camera_traps.data import Classes
from camera_traps.db.config import db
from camera_traps.settings import SITES, S

dash.register_page(__name__, path="/home", title="Home", order=0)


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
                                            create_card(
                                                id="kpi-total-sites",
                                                title="Total sites",
                                                info="Number of total active sites.",
                                            ),
                                            create_card(
                                                id="kpi-total-videos",
                                                title="Total videos",
                                                info="Number of total videos registered.",
                                            ),
                                            create_card(
                                                id="kpi-total-classes",
                                                title="Total classes",
                                                info=f"Number of total classes that the model could recognize: {', '.join(c.value for c in Classes)}.",
                                            ),
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
                                                    style={"height": "34vh", "width": "100%"},
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
                                        create_title(
                                            title="Processing status",
                                            info="Proportion of videos categorized by their current processing state: PENDING, PROCESSING, COMPLETED, FAILED.",
                                        ),
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
                                        create_title(
                                            title="Computational timing",
                                            info="Time required by the algorithm to queue and process the videos.",
                                        ),
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
                                        create_title(
                                            title="Video duration distribution",
                                            info="Distribution of the video duration.",
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
                                        create_title(
                                            title="Daily videos flow",
                                            info="Daily trend of registered videos over the selected period.",
                                        ),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="daily-video-chart",
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
                                        create_title(
                                            title="Hourly videos distribution",
                                            info="Concentration of registered videos across different hours of the day.",
                                        ),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="hourly-video-chart",
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
    Output("kpi-total-sites", "children"),
    Output("kpi-total-videos", "children"),
    Output("kpi-total-classes", "children"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_kpi(date_range: list[str | None], sites: list[str], hour_range: list[int]):
    """Display the KPI cards"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
    }
    df_kpi = db.run_sql_file("home/get_kpi.sql", parameters=params)

    return (
        f"{len(df_kpi):,.0f}",
        f"{df_kpi['total_videos'].sum():,.0f}",
        f"{len(Classes):,.0f}",
    )


@callback(
    Output("camera-map", "figure"),
    Output("camera-map-value", "children"),
    Input("theme-radio", "value"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_map(theme: str, date_range: list[str | None], sites: list[str], hour_range: list[int]):
    """Display camera trap locations on the map"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
    }
    df_kpi = db.run_sql_file("home/get_kpi.sql", parameters=params)
    df_location = pd.DataFrame.from_dict(SITES, orient="index").reset_index(names="site")
    df_trap = pd.merge(df_location, df_kpi, on="site", how="right")

    # Create figure.
    fig = px.scatter_mapbox(
        df_trap,
        lat="lat",
        lon="lon",
        custom_data=["name", "total_videos"],
    )
    fig.update_traces(
        marker=dict(size=13, color="#E07A5F", opacity=1.0),
        hovertemplate=(
            "<b>Site</b>: %{customdata[0]}<br><br>" "<b>N° of videos</b>: %{customdata[1]}" "<extra></extra>"
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
        template="mantine_dark" if theme == "dark" else "mantine_light",
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
        mapbox=dict(
            accesstoken=S.MAPBOX_TOKEN,
            center=go.layout.mapbox.Center(lat=44.6337, lon=9.7314),
            style="dark" if theme == "dark" else "light",
            zoom=12,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        autosize=True,
    )

    return fig, len(df_trap)


@callback(
    Output("status-chart", "figure"),
    Input("theme-radio", "value"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_status_chart(theme: str, date_range: list[str | None], sites: list[str], hour_range: list[int]):
    """Display donut chart of video processing status"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
    }
    df_status = db.run_sql_file("home/get_status.sql", parameters=params)

    # Create figure.
    fig = px.pie(
        df_status,
        names="status",
        values="total",
        hole=0.5,
        color="status",
        color_discrete_map=STATUS_COLOR_MAP,
        category_orders={"status": ["COMPLETED", "PROCESSING", "PENDING", "FAILED"]},
    )
    fig.update_traces(
        textinfo="percent+value",
        hovertemplate="<b>Status</b>: %{label}<br>"
        "<b>N° of videos</b>: %{value}<br>"
        "<b>Percentage</b>: %{percent}<br>"
        "<extra></extra>",
    )
    fig.update_layout(
        template="mantine_dark" if theme == "dark" else "mantine_light",
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
    Input("theme-radio", "value"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_computational_timing(theme: str, date_range: list[str | None], sites: list[str], hour_range: list[int]):
    """Display horizontal box plot of queue and processing times"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
    }
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
        template="mantine_dark" if theme == "dark" else "mantine_light",
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
    Input("theme-radio", "value"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_duration_histogram(theme: str, date_range: list[str | None], sites: list[str], hour_range: list[int]):
    """Display histogram of video duration"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
    }
    df_duration = db.run_sql_file("home/get_info.sql", parameters=params)

    # Create figure.
    fig = px.histogram(
        df_duration,
        x="duration",
        opacity=0.8,
    )
    fig.update_traces(
        hovertemplate="<b>N° of videos</b>: %{y}<br><b>Duration</b>: %{x}<br><extra></extra>",
        xbins=dict(size=1),
    )
    fig.update_layout(
        template="mantine_dark" if theme == "dark" else "mantine_light",
        xaxis=dict(title="Duration (s)", dtick=1),
        yaxis=dict(title="Number of videos", dtick=1),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
    )

    return fig


@callback(
    Output("daily-video-chart", "figure"),
    Input("theme-radio", "value"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_daily_video(theme: str, date_range: list[str | None], sites: list[str], hour_range: list[int]):
    """Display area chart of daily detected animals"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
    }
    df_daily = db.run_sql_file("home/get_info.sql", parameters=params)
    df_daily["created_at"] = pd.to_datetime(df_daily["created_at"]).dt.tz_localize(None).dt.date
    df_filtered = (
        df_daily.groupby("created_at")["id"]
        .count()
        .reindex(pd.date_range(start=date_range[0], end=date_range[1], freq="D"), fill_value=0)
        .rename_axis("created_at")
        .reset_index()
    )

    # Create figure.
    fig = go.Figure(
        [
            go.Scatter(
                x=df_filtered["created_at"],
                y=df_filtered["id"],
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
        hovertemplate="<b>N° of videos</b>: %{y}<br>" "<b>Datetime</b>: %{x}, %{x|%a}" "<extra></extra>",
    )
    fig.update_layout(
        template="mantine_dark" if theme == "dark" else "mantine_light",
        showlegend=False,
        xaxis=dict(title="Datetime"),
        yaxis=dict(title="Number of videos"),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
    )

    return fig


@callback(
    Output("hourly-video-chart", "figure"),
    Input("theme-radio", "value"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_hourly_video(theme: str, date_range: list[str | None], sites: list[str], hour_range: list[int]):
    """Display hourly heatmap of detected animals"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
    }
    df_hourly = db.run_sql_file("home/get_info.sql", parameters=params)
    df_hourly["created_at"] = pd.to_datetime(df_hourly["created_at"]).dt.tz_localize(None)
    df_filtered = (
        df_hourly.set_index("created_at")
        .resample("h")["id"]
        .count()
        .reindex(
            pd.date_range(start=f"{date_range[0]} 00:00:00", end=f"{date_range[1]} 23:00:00", freq="h"), fill_value=0
        )
        .rename_axis("created_at")
        .reset_index()
    )

    df_filtered["date"] = df_filtered["created_at"].dt.date
    df_filtered["hour"] = df_filtered["created_at"].dt.hour
    df_pivot = df_filtered.pivot_table(index="hour", columns="date", values="id", aggfunc="sum", fill_value=0)
    df_pivot = df_pivot.loc[hour_range[0] : hour_range[1] - 1]
    df_pivot.index = [f"{int(h):02d}:00" for h in df_pivot.index]

    # Create figure.
    fig = px.imshow(
        df_pivot, aspect="auto", color_continuous_scale=CONTINUOUS_SCALE, zmin=0, zmax=max(df_pivot.max().max(), 1)
    )
    fig.update_traces(
        hovertemplate="<b>N° of tracks</b>: %{z}<br>"
        "<b>Datetime</b>: %{x}<br>"
        "<b>Hour</b>: %{y}<br>"
        "<extra></extra>"
    )
    fig.update_layout(
        template="mantine_dark" if theme == "dark" else "mantine_light",
        xaxis=dict(title="Datetime", showgrid=False, zeroline=False),
        yaxis=dict(title="Hour", showgrid=False, zeroline=False),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
        coloraxis_colorbar=dict(title="Trackers"),
        coloraxis_colorbar_title_side="right",
        hoverlabel=dict(
            bgcolor="#2E6F40",
            font=dict(color="white"),
        ),
    )

    return fig
