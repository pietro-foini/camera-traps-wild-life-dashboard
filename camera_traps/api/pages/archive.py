from pathlib import Path

import dash
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash import Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate

from camera_traps.data import Classes
from camera_traps.db.config import db
from camera_traps.settings import S

dash.register_page(__name__, path="/archive", title="Monitoring", order=2)


layout = dmc.Container(
    fluid=True,
    p="md",
    children=[
        dmc.Grid(
            gutter="md",
            children=[
                dmc.GridCol(
                    span=5,
                    children=dcc.Loading(
                        color="var(--primary)",
                        type="circle",
                        children=dag.AgGrid(
                            id="archive-grid",
                            rowData=[],
                            columnDefs=[
                                {
                                    "field": "filename",
                                    "headerName": "File",
                                    "headerTooltip": "Video file name",
                                },
                                {
                                    "field": "trackers",
                                    "headerName": "Trackers",
                                    "headerTooltip": "Number of distinct tracked individuals in the video",
                                },
                                {
                                    "field": "species",
                                    "headerName": "Species",
                                    "headerTooltip": "Number of distinct species detected in the video",
                                },
                                {
                                    "field": "labels",
                                    "headerName": "Labels",
                                    "headerTooltip": "List of species identified by the model",
                                },
                                {
                                    "field": "date",
                                    "headerName": "Date",
                                    "headerTooltip": "Video creation date and time",
                                },
                            ],
                            style={"height": "80vh", "width": "100%"},
                            defaultColDef={"flex": 1, "filter": True},
                            dashGridOptions={
                                "rowSelection": {"mode": "singleRow"},
                                "tooltipShowDelay": 200,
                            },
                        ),
                    ),
                ),
                dmc.GridCol(
                    span=7,
                    children=[
                        dmc.Stack(
                            children=[
                                html.Div(
                                    id="video-container",
                                    style={
                                        "height": "40vh",
                                        "backgroundColor": "#f1f3f5",
                                        "borderRadius": "8px",
                                    },
                                ),
                                dmc.Stack(
                                    h="38vh",
                                    gap="xs",
                                    p="xs",
                                    style={
                                        "backgroundColor": "#f1f3f5",
                                        "borderRadius": "8px",
                                    },
                                    children=[
                                        dag.AgGrid(
                                            id="validation-grid",
                                            rowData=[],
                                            columnDefs=[
                                                {
                                                    "field": "tracker_id",
                                                    "headerName": "Tracker ID",
                                                    "editable": False,
                                                    "maxWidth": 150,
                                                },
                                                {
                                                    "field": "label",
                                                    "headerName": "Label",
                                                    "editable": True,
                                                    "cellEditor": "agSelectCellEditor",
                                                    "cellEditorParams": {
                                                        "values": [c.value for c in Classes],
                                                    },
                                                },
                                            ],
                                            defaultColDef={"flex": 1},
                                            dashGridOptions={
                                                "singleClickEdit": True,
                                                "stopEditingWhenCellsLoseFocus": True,
                                            },
                                            style={"flex": 1, "width": "100%"},
                                        ),
                                        dmc.Group(
                                            justify="flex-start",
                                            children=[
                                                dmc.Button(
                                                    children="Save validation",
                                                    id="save-validation-btn",
                                                )
                                            ],
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


@callback(Output("archive-grid", "rowData"), Input("date-range-picker", "value"))
def update_table(date_range: None | list[str | None]):
    """Update table"""

    if not date_range or not date_range[0] or not date_range[1]:
        raise PreventUpdate

    params = {"start_date": date_range[0], "end_date": date_range[1]}
    df = db.run_sql_file("get_archive_eligible.sql", parameters=params)

    return df.to_dict("records")


@callback(
    Output("video-container", "children"),
    Input("archive-grid", "selectedRows"),
)
def display_video(selected_rows: list[dict]):
    """Load the selected video"""

    if not selected_rows:
        return dmc.Center(children="Select a record to visualize video", h="100%", c="dimmed")

    filename = Path(selected_rows[0]["filename"]).name

    return html.Video(
        src=f"{S.S3_ENDPOINT_URL}/buckets/bucket-cameratraps/output/{filename}",
        controls=True,
        autoPlay=True,
        style={
            "width": "100%",
            "height": "100%",
            "borderRadius": "8px",
            "objectFit": "contain",
            "backgroundColor": "black",
        },
    )


@callback(
    Output("validation-grid", "rowData"),
    Input("archive-grid", "selectedRows"),
)
def display_validation(selected_rows: list[dict]):
    """Load trackers data for the selected video"""

    if not selected_rows:
        return []

    params = {"video_id": selected_rows[0]["id"]}
    df = db.run_sql_file("get_trackers.sql", parameters=params)

    return df.to_dict("records")


# @callback(
#     Output("archive-grid", "rowData", allow_duplicate=True),
#     Input("save-validation-btn", "n_clicks"),
#     State("validation-grid", "rowData"),
#     State("date-range-picker", "value"),
#     prevent_initial_call=True,
# )
# def save_validation(n_clicks, validation_rows, date_range):
#     """Save updated labels to DB when button is clicked"""
#     if not n_clicks or not validation_rows:
#         raise PreventUpdate
#
#     # Aggiorna ogni tracker del video
#     for row in validation_rows:
#         db.execute_query(
#             """
#             UPDATE video_outputs
#             SET label = :label
#             WHERE video_input_id = :video_id
#               AND tracker_id = :tracker_id
#             """,
#             parameters={
#                 "label": row["label"],
#                 "video_id": row["video_input_id"],
#                 "tracker_id": row["tracker_id"],
#             },
#         )
#
#     # Ricarica i dati della tabella principale a sinistra per mostrare le nuove label
#     return update_datatable(date_range)
