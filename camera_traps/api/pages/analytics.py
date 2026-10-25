import dash
import dash_mantine_components as dmc
import plotly.express as px
import plotly.io as pio
from dash import Input, Output, callback, dcc
from dash.exceptions import PreventUpdate

from camera_traps.api.components import create_card
from camera_traps.api.config import CONTINUOUS_SCALE, GRAPH_CONFIG
from camera_traps.db.config import db

dash.register_page(__name__, path="/analytics", title="Analytics", order=1)

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
                                        cols=4,
                                        spacing="md",
                                        children=[
                                            create_card(id="kpi-validated-videos", title="Validated videos"),
                                            create_card(id="kpi-validated-tracks", title="Validated tracks"),
                                            create_card(id="kpi-model-accuracy", title="Model accuracy"),
                                            create_card(id="kpi-human-corrections", title="Human corrections"),
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
                                                dmc.Text(children="Validation outcome", size="lg", fw=400, ta="center"),
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
                            span=7,
                            children=dmc.Paper(
                                withBorder=True,
                                radius="md",
                                p="md",
                                style={"height": "100%"},
                                children=dmc.Stack(
                                    gap="xs",
                                    children=[
                                        dmc.Text(
                                            children="Confusion matrix",
                                            size="lg",
                                            fw=400,
                                            ta="center",
                                        ),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="confusion-matrix-chart",
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
                                        dmc.Text(
                                            children="Validation outcome by species", size="lg", fw=400, ta="center"
                                        ),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="species-validation-bar",
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
                                        dmc.Text(
                                            children="Frames per tracker distribution", size="lg", fw=400, ta="center"
                                        ),
                                        dcc.Loading(
                                            color="var(--primary)",
                                            type="circle",
                                            children=dcc.Graph(
                                                id="tracker-frames-boxplot",
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
    Output("kpi-validated-videos", "children"),
    Output("kpi-validated-tracks", "children"),
    Output("kpi-model-accuracy", "children"),
    Output("kpi-human-corrections", "children"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_validation_kpi(date_range: list[str | None], sites: list[str]):
    """Display the Validation KPI cards"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_kpi = db.run_sql_file("analytics/get_kpi.sql", parameters=params)

    total_videos = df_kpi["total_videos"].iloc[0] or 0
    total_tracks = df_kpi["total_validated"].iloc[0] or 0
    modified = df_kpi["total_modified"].iloc[0] or 0
    accuracy = ((total_tracks - modified) / total_tracks * 100) if total_tracks > 0 else 0

    return (
        f"{total_videos:,.0f}",
        f"{total_tracks:,.0f}",
        f"{accuracy:.1f}%",
        f"{modified:,.0f}",
    )


@callback(
    Output("validation-outcome-chart", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_validation_outcome(date_range: list[str | None], sites: list[str]):
    """Display donut chart of confirmed vs modified vs manual additions"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_outcome = db.run_sql_file("analytics/get_validation.sql", parameters=params)

    # Create figure.
    fig = px.pie(
        df_outcome,
        names="validation_status",
        values="total",
        hole=0.5,
        color_discrete_sequence=pio.templates[pio.templates.default].layout.colorway[1:],
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
    Output("confusion-matrix-chart", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_confusion_matrix(date_range: list[str | None], sites: list[str]):
    """Display confusion matrix between predicted label and validated label"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_cm = db.run_sql_file("analytics/get_confusion.sql", parameters=params)
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
        "<b>Count</b>: %{z}<br>"
        "<extra></extra>"
    )
    fig.update_layout(
        xaxis=dict(title="Predicted species", showgrid=False, zeroline=False),
        yaxis=dict(title="Validated species", showgrid=False, zeroline=False),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
        coloraxis_colorbar=dict(title="Tracks"),
        coloraxis_colorbar_title_side="right",
    )

    return fig


@callback(
    Output("species-validation-bar", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_species_validation_bar(date_range: list[str | None], sites: list[str]):
    """Display horizontal stacked bar chart of confirmed vs modified per species"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_species_val = db.run_sql_file("analytics/get_validation_species.sql", parameters=params)

    # Create figure.
    fig = px.bar(
        df_species_val,
        x="total",
        y="species",
        color="validation_status",
        orientation="h",
        barmode="stack",
        color_discrete_sequence=pio.templates[pio.templates.default].layout.colorway[1:],
    )
    fig.update_traces(
        hovertemplate="<b>Species</b>: %{y}<br><b>Count</b>: %{x}<extra></extra>",
    )
    fig.update_layout(
        xaxis=dict(title="Number of tracks"),
        yaxis=dict(title="Species"),
        legend=dict(title_text=""),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
    )

    return fig


@callback(
    Output("tracker-frames-boxplot", "figure"),
    Input("date-range-picker", "value"),
    Input("site-filter", "value"),
)
def update_tracker_frames_boxplot(date_range: list[str | None], sites: list[str]):
    """Display box plot of number of frames per tracker grouped by species"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    # Retrieve data.
    params = {"start_date": date_range[0], "end_date": date_range[1], "sites": sites if sites else None}
    df_frames = db.run_sql_file("analytics/get_frames_tracks.sql", parameters=params)

    # Create figure.
    fig = px.box(
        df_frames,
        x="num_frames",
        y="species",
        color="species",
        orientation="h",
        points="outliers",
        color_discrete_sequence=pio.templates[pio.templates.default].layout.colorway[1:],
    )
    fig.update_traces(opacity=0.75, name="")
    fig.update_layout(
        showlegend=False,
        hovermode="y unified",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.9)"),
        xaxis=dict(title="Frames count (Track duration)"),
        yaxis=dict(title="Species"),
        margin=dict(l=20, r=20, t=10, b=20),
        autosize=True,
    )

    return fig
