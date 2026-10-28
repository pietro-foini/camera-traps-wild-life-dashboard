from pathlib import Path

import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots

from camera_traps.api.components import create_card, create_title
from camera_traps.api.config import CONTINUOUS_SCALE, EDIT_COLOR_MAP, GRAPH_CONFIG
from camera_traps.db.config import db
from camera_traps.settings import S

dash.register_page(__name__, path="/analytics", title="Analytics", order=1)

layout = dmc.Container(
    fluid=True,
    p="md",
    children=[
        dmc.Tabs(
            value="predictions",
            variant="default",
            color="palette.8",
            radius=0,
            children=[
                dmc.TabsList(
                    grow=True,
                    mt="-md",
                    mx="-md",
                    mb="md",
                    children=[
                        dmc.TabsTab(children="Predictions", value="predictions", py="sm", fw=600),
                        dmc.TabsTab(children="Validation", value="validation", py="sm", fw=600),
                    ],
                ),
                dmc.TabsPanel(
                    value="predictions",
                    children=[
                        dmc.Stack(
                            gap="md",
                            children=[
                                dmc.Grid(
                                    gutter="md",
                                    children=[
                                        dmc.GridCol(
                                            span=6,
                                            children=dmc.Stack(
                                                gap="md",
                                                children=[
                                                    dmc.SimpleGrid(
                                                        cols=4,
                                                        spacing="md",
                                                        children=[
                                                            create_card(
                                                                id="kpi-predicted-videos",
                                                                title="Predicted videos",
                                                                info="Total number of successfully processed videos in which at least one of the selected classes was predicted by the model.",
                                                            ),
                                                            create_card(
                                                                id="kpi-predicted-tracks",
                                                                title="Predicted tracks",
                                                                info="Total number of predicted tracks for the selected classes in the successfully processed videos.",
                                                            ),
                                                            create_card(
                                                                id="kpi-average-confidence",
                                                                title="Avg Confidence",
                                                                info="Average model confidence score across all frame-level predictions for the selected classes of the successfully processed videos.",
                                                            ),
                                                            create_card(
                                                                id="kpi-predicted-classes",
                                                                title="Predicted classes",
                                                                info="Total number of predicted classes across the the successfully processed videos.",
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
                                                                        "Example · ",
                                                                        html.Span(
                                                                            id="video-example-value",
                                                                            children="0",
                                                                            style={"fontWeight": 500},
                                                                        ),
                                                                    ],
                                                                    size="xs",
                                                                    c="dimmed",
                                                                    fw=300,
                                                                    tt="uppercase",
                                                                    mb="xs",
                                                                ),
                                                                html.Div(
                                                                    id="video-example-container",
                                                                    style={"height": "34vh", "width": "100%"},
                                                                ),
                                                            ],
                                                        ),
                                                    ),
                                                ],
                                            ),
                                        ),
                                        dmc.GridCol(
                                            span=6,
                                            children=dmc.Paper(
                                                withBorder=True,
                                                radius="md",
                                                p="md",
                                                style={"height": "100%"},
                                                children=dmc.Stack(
                                                    gap="xs",
                                                    children=[
                                                        create_title(
                                                            title="Predicted classes",
                                                            info="Breakdown of predicted tracks per identified class and their track-level confidence distribution.",
                                                        ),
                                                        dcc.Loading(
                                                            color="var(--primary)",
                                                            type="circle",
                                                            children=dcc.Graph(
                                                                id="predicted-species-histogram",
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
                                            span=5,
                                            children=dmc.Paper(
                                                withBorder=True,
                                                radius="md",
                                                p="md",
                                                style={"height": "38vh"},
                                                children=dmc.Stack(
                                                    gap="xs",
                                                    children=[
                                                        create_title(
                                                            title="Predicted tracks per video",
                                                            info=".",
                                                        ),
                                                        dcc.Loading(
                                                            color="var(--primary)",
                                                            type="circle",
                                                            children=dcc.Graph(
                                                                id="predicted-tracks-histogram",
                                                                config=GRAPH_CONFIG,
                                                                style={"height": "30vh", "width": "100%"},
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                            ),
                                        ),
                                        dmc.GridCol(
                                            span=7,
                                            children=dmc.Paper(
                                                withBorder=True,
                                                radius="md",
                                                p="md",
                                                style={"height": "38vh"},
                                                children=dmc.Stack(
                                                    gap="xs",
                                                    children=[
                                                        create_title(
                                                            title="Predicted hourly tracks",
                                                            info="Hourly distribution of predicted tracks.",
                                                        ),
                                                        dcc.Loading(
                                                            color="var(--primary)",
                                                            type="circle",
                                                            children=dcc.Graph(
                                                                id="predicted-hourly-heatmap",
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
                ),
                dmc.TabsPanel(
                    value="validation",
                    children=[
                        dmc.Stack(
                            gap="md",
                            children=[
                                dmc.Grid(
                                    gutter="md",
                                    children=[
                                        dmc.GridCol(
                                            span=6,
                                            children=dmc.Stack(
                                                gap="md",
                                                children=[
                                                    dmc.SimpleGrid(
                                                        cols=4,
                                                        spacing="md",
                                                        children=[
                                                            create_card(
                                                                id="kpi-validated-videos",
                                                                title="Validated videos",
                                                                info="Number of total validated videos by users.",
                                                            ),
                                                            create_card(
                                                                id="kpi-validated-tracks",
                                                                title="Validated tracks",
                                                                info="Number of total validated tracks contained into the validated videos.",
                                                            ),
                                                            create_card(
                                                                id="kpi-model-accuracy",
                                                                title="Model accuracy",
                                                                info="Accuracy of the recognition model keeping detected tracks as base.",
                                                            ),
                                                            create_card(
                                                                id="kpi-human-corrections",
                                                                title="Human edits",
                                                                info="Number of total human corrections on recognized specie into detected tracks.",
                                                            ),
                                                        ],
                                                    ),
                                                    dmc.Paper(
                                                        withBorder=True,
                                                        radius="md",
                                                        p="md",
                                                        style={"height": "40vh"},
                                                        children=dmc.Stack(
                                                            gap="xs",
                                                            children=[
                                                                create_title(
                                                                    title="Validation outcome",
                                                                    info="Proportion of tracks categorized by their human validation result.",
                                                                ),
                                                                dcc.Loading(
                                                                    color="var(--primary)",
                                                                    type="circle",
                                                                    children=dcc.Graph(
                                                                        id="validation-outcome-chart",
                                                                        config=GRAPH_CONFIG,
                                                                        style={"height": "32vh", "width": "100%"},
                                                                    ),
                                                                ),
                                                            ],
                                                        ),
                                                    ),
                                                ],
                                            ),
                                        ),
                                        dmc.GridCol(
                                            span=6,
                                            children=dmc.Paper(
                                                withBorder=True,
                                                radius="md",
                                                p="md",
                                                style={"height": "100%"},
                                                children=dmc.Stack(
                                                    gap="xs",
                                                    children=[
                                                        create_title(
                                                            title="Validated classes",
                                                            info="Breakdown of confirmed and corrected tracks for each identified classes.",
                                                        ),
                                                        dcc.Loading(
                                                            color="var(--primary)",
                                                            type="circle",
                                                            children=dcc.Graph(
                                                                id="validated-species-bar",
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
                                            span=5,
                                            children=dmc.Paper(
                                                withBorder=True,
                                                radius="md",
                                                p="md",
                                                style={"height": "38vh"},
                                                children=dmc.Stack(
                                                    gap="xs",
                                                    children=[
                                                        create_title(
                                                            title="Confusion matrix",
                                                            info="Comparison between model-predicted classes and human-validated classes.",
                                                        ),
                                                        dcc.Loading(
                                                            color="var(--primary)",
                                                            type="circle",
                                                            children=dcc.Graph(
                                                                id="confusion-matrix-chart",
                                                                config=GRAPH_CONFIG,
                                                                style={"height": "30vh", "width": "100%"},
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                            ),
                                        ),
                                        dmc.GridCol(
                                            span=7,
                                            children=dmc.Paper(
                                                withBorder=True,
                                                radius="md",
                                                p="md",
                                                style={"height": "38vh"},
                                                children=dmc.Stack(
                                                    gap="xs",
                                                    children=[
                                                        create_title(
                                                            title="Validated hourly tracks",
                                                            info="Hourly distribution of validated tracks.",
                                                        ),
                                                        dcc.Loading(
                                                            color="var(--primary)",
                                                            type="circle",
                                                            children=dcc.Graph(
                                                                id="validated-hourly-heatmap",
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
                ),
            ],
        )
    ],
)


@callback(
    Output("kpi-predicted-videos", "children"),
    Output("kpi-predicted-tracks", "children"),
    Output("kpi-average-confidence", "children"),
    Output("kpi-predicted-classes", "children"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("class-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_prediction_kpi(date_range: list[str | None], sites: list[str], classes: list[str], hour_range: list[int]):
    """Display the prediction KPI cards"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_kpi = db.run_sql_file("analytics/predictions/get_kpi.sql", parameters=params)

    total_videos = df_kpi["total_videos"].iloc[0] or 0
    total_tracks = df_kpi["total_tracks"].iloc[0] or 0
    avg_confidence = (df_kpi["avg_confidence"].iloc[0] or 0) * 100
    total_species = df_kpi["total_species"].iloc[0] or 0

    return f"{total_videos:,.0f}", f"{total_tracks:,.0f}", f"{avg_confidence:.1f}%", f"{total_species:,.0f}"


@callback(
    Output("kpi-validated-videos", "children"),
    Output("kpi-validated-tracks", "children"),
    Output("kpi-model-accuracy", "children"),
    Output("kpi-human-corrections", "children"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("class-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_validation_kpi(date_range: list[str | None], sites: list[str], classes: list[str], hour_range: list[int]):
    """Display the validation KPI cards"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_kpi = db.run_sql_file("analytics/validation/get_kpi.sql", parameters=params)

    total_videos = df_kpi["total_videos"].iloc[0] or 0
    total_tracks = df_kpi["total_validated"].iloc[0] or 0
    modified = df_kpi["total_modified"].iloc[0] or 0
    accuracy = ((total_tracks - modified) / total_tracks * 100) if total_tracks > 0 else 0

    return f"{total_videos:,.0f}", f"{total_tracks:,.0f}", f"{accuracy:.1f}%", f"{modified:,.0f}"


@callback(
    Output("video-example-container", "children"),
    Output("video-example-value", "children"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("class-filter", "value"),
    Input("hour-range-slider", "value"),
)
def display_video_example(date_range: list[str | None], sites: list[str], classes: list[str], hour_range: list[int]):
    """Load the selected video"""

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_video = db.run_sql_file("analytics/predictions/get_example.sql", parameters=params)

    if df_video.empty:
        return html.Video(), ""

    return (
        html.Video(
            src=f"{S.S3_ENDPOINT_URL}/buckets/bucket-cameratraps/output/{Path(df_video.iloc[0]['filename']).name}",
            controls=True,
            autoPlay=True,
            style={
                "width": "100%",
                "height": "100%",
                "borderRadius": "8px",
                "objectFit": "contain",
                "backgroundColor": "black",
            },
        ),
        Path(df_video.iloc[0]["filename"]).name,
    )


@callback(
    Output("validation-outcome-chart", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("class-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_validation_outcome(
    date_range: list[str | None], sites: list[str], classes: list[str], hour_range: list[int]
):
    """Display donut chart of confirmed vs modified vs manual additions"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_validation = db.run_sql_file("analytics/validation/get_validation.sql", parameters=params)
    df_validation = df_validation.groupby("validation_status", as_index=False).agg(total=("total", "sum"))

    # Create figure.
    fig = px.pie(
        df_validation,
        names="validation_status",
        values="total",
        hole=0.5,
        color="validation_status",
        color_discrete_map=EDIT_COLOR_MAP,
        category_orders={"status": ["Confirmed", "Relabeled", "Added"]},
    )
    fig.update_traces(
        textinfo="percent+value",
        hovertemplate="<b>Outcome</b>: %{label}<br>"
        "<b>N° of tracks</b>: %{value}<br>"
        "<b>Percentage</b>: %{percent}<br>"
        "<extra></extra>",
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=15, b=15),
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=0, title_text=""),
        autosize=True,
    )

    return fig


@callback(
    Output("predicted-species-histogram", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("class-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_predictions_by_species(
    date_range: list[str | None], sites: list[str], classes: list[str], hour_range: list[int]
):
    """Display horizontal bar chart of predicted species and box plot of confidence"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_predictions = db.run_sql_file("analytics/predictions/get_predictions.sql", parameters=params)
    df_predictions["species"] = df_predictions["species"].str.capitalize()
    df_confidence = db.run_sql_file("analytics/predictions/get_confidence.sql", parameters=params)
    df_confidence["species"] = df_confidence["species"].str.capitalize()

    # Create figure.
    fig = make_subplots(
        rows=1,
        cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.04,
        column_widths=[0.55, 0.45],
    )
    fig.add_trace(
        go.Bar(
            x=df_predictions["total"],
            y=df_predictions["species"],
            orientation="h",
            opacity=0.9,
            text=df_predictions["total"],
            textposition="auto",
            marker=dict(color="#2E6F40"),
            name="",
            hovertemplate="<b>N° of tracks</b>: %{x}<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Box(
            x=df_confidence["avg_confidence"],
            y=df_confidence["species"],
            orientation="h",
            boxpoints="outliers",
            opacity=0.75,
            marker=dict(color="#E07A5F"),
            name="",
        ),
        row=1,
        col=2,
    )
    fig.update_layout(
        showlegend=False,
        hovermode="y unified",
        # hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.9)"),
        xaxis=dict(
            title="Number of tracks",
            zeroline=False,
        ),
        xaxis2=dict(
            title="Confidence (%)",
            hoverformat=".1f",
            zeroline=False,
            showgrid=True,
        ),
        yaxis=dict(
            title="Classes",
            categoryorder="array",
            categoryarray=df_predictions["species"],
        ),
        yaxis2=dict(
            showline=True,
            linecolor="lightgray",
            linewidth=1,
        ),
        margin=dict(l=20, r=20, t=10, b=20),
        autosize=True,
    )

    return fig


@callback(
    Output("validated-species-bar", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("class-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_validation_outcome_by_species(
    date_range: list[str | None], sites: list[str], classes: list[str], hour_range: list[int]
):
    """Display horizontal stacked bar chart of confirmed vs modified per species"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_validation = db.run_sql_file("analytics/validation/get_validation.sql", parameters=params)
    df_validation = df_validation.groupby(["species", "validation_status"], as_index=False).agg(total=("total", "sum"))
    df_validation["species"] = df_validation["species"].str.capitalize()

    # Create figure.
    fig = px.bar(
        df_validation,
        x="total",
        y="species",
        color="validation_status",
        orientation="h",
        barmode="stack",
        color_discrete_map=EDIT_COLOR_MAP,
        category_orders={"status": ["Confirmed", "Relabeled", "Added"]},
    )
    fig.update_traces(
        hovertemplate="<b>Class</b>: %{y}<br><b>N° of tracks</b>: %{x}<extra></extra>",
    )
    fig.update_layout(
        xaxis=dict(title="Number of tracks"),
        yaxis=dict(title="Classes"),
        legend=dict(title_text=""),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
    )

    return fig


@callback(
    Output("predicted-tracks-histogram", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("class-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_tracks_histogram(date_range: list[str | None], sites: list[str], classes: list[str], hour_range: list[int]):
    """Display histogram of tracks per video"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_tracks = db.run_sql_file("analytics/predictions/get_tracks.sql", parameters=params)

    # Create figure.
    fig = px.histogram(
        df_tracks,
        x="total",
        text_auto=True,
        opacity=0.8,
        color_discrete_sequence=["#3D5A80"],
    )
    fig.update_traces(
        hovertemplate="<b>N° of videos</b>: %{y}<br>" "<b>N° of tracks</b>: %{x}<br>" "<extra></extra>",
        xbins=dict(size=1),
    )
    fig.update_layout(
        bargap=0.2,
        xaxis=dict(title="Number of tracks", dtick=1),
        yaxis=dict(title="Number of videos", dtick=1),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
    )

    return fig


@callback(
    Output("confusion-matrix-chart", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("class-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_confusion_matrix(date_range: list[str | None], sites: list[str], classes: list[str], hour_range: list[int]):
    """Display confusion matrix between predicted label and validated label"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_cm = db.run_sql_file("analytics/validation/get_confusion.sql", parameters=params)
    df_cm["predicted_label"] = df_cm["predicted_label"].str.capitalize()
    df_cm["validated_label"] = df_cm["validated_label"].str.capitalize()

    df_pivot = df_cm.pivot_table(
        index="validated_label", columns="predicted_label", values="total", aggfunc="sum", fill_value=0
    )

    # Create figure.
    fig = px.imshow(
        df_pivot,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=CONTINUOUS_SCALE,
    )
    fig.update_traces(
        hovertemplate="<b>Predicted</b>: %{x}<br>"
        "<b>Validated</b>: %{y}<br>"
        "<b>N° of tracks</b>: %{z}<br>"
        "<extra></extra>"
    )
    fig.update_layout(
        xaxis=dict(title="Predicted classes", showgrid=False, zeroline=False),
        yaxis=dict(title="Validated classes", showgrid=False, zeroline=False),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
        coloraxis_colorbar=dict(title="Number of tracks"),
        coloraxis_colorbar_title_side="right",
        hoverlabel=dict(
            bgcolor="#2E6F40",
            bordercolor="#2E6F40",
        ),
    )

    return fig


@callback(
    Output("predicted-hourly-heatmap", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("hour-range-slider", "value"),
    Input("class-filter", "value"),
)
def update_predicted_hourly_heatmap(
    date_range: list[str | None], sites: list[str], hour_range: list[int], classes: list[str]
):
    """Display hourly heatmap of predicted tracks"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_hourly = db.run_sql_file("analytics/predictions/get_hourly_tracks.sql", parameters=params)
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
        xaxis=dict(title="Datetime", showgrid=False, zeroline=False),
        yaxis=dict(title="Hour", showgrid=False, zeroline=False),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
        coloraxis_colorbar=dict(title="Number of tracks"),
        coloraxis_colorbar_title_side="right",
        hoverlabel=dict(
            bgcolor="#2E6F40",
            bordercolor="#2E6F40",
        ),
    )

    return fig


@callback(
    Output("validated-hourly-heatmap", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
    Input("class-filter", "value"),
    Input("hour-range-slider", "value"),
)
def update_validated_hourly_heatmap(
    date_range: list[str | None], sites: list[str], classes: list[str], hour_range: list[int]
):
    """Display hourly heatmap of validated tracks"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {
        "start_date": date_range[0],
        "end_date": date_range[1],
        "sites": sites if sites else None,
        "start_hour": hour_range[0],
        "end_hour": hour_range[1],
        "species": classes if classes else None,
    }
    df_hourly = db.run_sql_file("analytics/validation/get_hourly_tracks.sql", parameters=params)
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
        xaxis=dict(title="Datetime", showgrid=False, zeroline=False),
        yaxis=dict(title="Hour", showgrid=False, zeroline=False),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
        coloraxis_colorbar=dict(title="Number of tracks"),
        coloraxis_colorbar_title_side="right",
        hoverlabel=dict(
            bgcolor="#2E6F40",
            bordercolor="#2E6F40",
        ),
    )

    return fig
