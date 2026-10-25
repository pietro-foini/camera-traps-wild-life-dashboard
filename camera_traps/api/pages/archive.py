from pathlib import Path

import dash
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from camera_traps.data import Classes
from camera_traps.db.config import db
from camera_traps.settings import S

dash.register_page(__name__, path="/archive", title="Archive", order=2)


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
                            id="prediction-table",
                            rowData=[],
                            columnDefs=[
                                {
                                    "field": "filename",
                                    "headerName": "File",
                                    "headerTooltip": "Video file name",
                                },
                                {
                                    "field": "trackers",
                                    "headerName": "N° Tracks",
                                    "headerTooltip": "Number of distinct tracked individuals in the video",
                                },
                                {
                                    "field": "species",
                                    "headerName": "N° Species",
                                    "headerTooltip": "Number of distinct species detected in the video",
                                },
                                {
                                    "field": "labels",
                                    "headerName": "Species",
                                    "headerTooltip": "List of species identified by the model",
                                },
                                {
                                    "field": "date",
                                    "headerName": "Datetime",
                                    "headerTooltip": "Video creation date and time",
                                },
                            ],
                            style={"height": "80vh", "width": "100%"},
                            defaultColDef={"flex": 1, "filter": True},
                            dashGridOptions={"rowSelection": {"mode": "singleRow"}, "tooltipShowDelay": 20},
                        ),
                    ),
                ),
                dmc.GridCol(
                    span=7,
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Paper(
                                    withBorder=True,
                                    radius="md",
                                    p="md",
                                    style={"height": "40vh"},
                                    children=html.Div(
                                        id="video-container",
                                        style={
                                            "height": "36vh",
                                            "borderRadius": "8px",
                                        },
                                    ),
                                ),
                                dmc.Stack(
                                    h="38vh",
                                    gap="xs",
                                    p="xs",
                                    style={
                                        "borderRadius": "8px",
                                    },
                                    children=[
                                        dag.AgGrid(
                                            id="validation-table",
                                            rowData=[],
                                            columnDefs=[
                                                {
                                                    "headerName": "",
                                                    "colId": "delete",
                                                    "cellRenderer": "DeleteButton",
                                                    "lockPosition": "left",
                                                    "maxWidth": 35,
                                                    "filter": False,
                                                    "cellStyle": {"paddingRight": 0, "paddingLeft": 0},
                                                },
                                                {
                                                    "field": "tracker_id",
                                                    "headerName": "Track ID",
                                                    "headerTooltip": "Tracker ID referring to the individual in the video. It cannot be edited. If not true, set Label to None_of_the_above.",
                                                    "editable": False,
                                                    "width": 110,
                                                },
                                                {
                                                    "field": "label",
                                                    "headerName": "Species",
                                                    "headerTooltip": "Label associated to the individual in the video. It can be edited.",
                                                    "editable": True,
                                                    "width": 180,
                                                    "cellEditor": "agSelectCellEditor",
                                                    "cellEditorParams": {
                                                        "values": [c.value for c in Classes],
                                                        "valueListMaxHeight": 120,
                                                        "valueListMaxWidth": 180,
                                                    },
                                                },
                                                {
                                                    "field": "comments",
                                                    "headerName": "Comments",
                                                    "headerTooltip": "Leave an optional comment.",
                                                    "editable": True,
                                                    "cellEditorPopup": True,
                                                    "cellEditor": "agLargeTextCellEditor",
                                                    "flex": 1,
                                                },
                                            ],
                                            defaultColDef={},
                                            dashGridOptions={
                                                "singleClickEdit": True,
                                                "stopEditingWhenCellsLoseFocus": True,
                                                "rowHeight": 40,
                                                "suppressScrollOnNewData": True,
                                                "tooltipShowDelay": 20,
                                            },
                                            style={"height": "38vh", "width": "100%"},
                                        ),
                                        dmc.Group(
                                            justify="flex-start",
                                            children=[
                                                dmc.Group(
                                                    justify="space-between",
                                                    children=[
                                                        dmc.Button(
                                                            children="+",
                                                            id="add-fn-btn",
                                                            variant="light",
                                                            disabled=True,
                                                        ),
                                                        dmc.Button(
                                                            children="Save validation",
                                                            id="save-validation-btn",
                                                            disabled=True,
                                                        ),
                                                    ],
                                                ),
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


@callback(Output("prediction-table", "rowData"), Input("date-range-picker", "value"))
def update_table(date_range: list[str | None]):
    """Update table containing the video predictions that need to be validated"""

    if not date_range[0] or not date_range[1]:
        raise PreventUpdate

    params = {"start_date": date_range[0], "end_date": date_range[1]}
    df = db.run_sql_file("archive/get_archive_eligible.sql", parameters=params)

    return df.to_dict("records")


@callback(
    Output("video-container", "children"),
    Input("prediction-table", "selectedRows"),
)
def display_video(selected_rows: list[dict]):
    """Load the selected video"""

    if not selected_rows:
        return dmc.Center(children="Select a record to visualize video", h="100%", c="dimmed")

    return html.Video(
        src=f"{S.S3_ENDPOINT_URL}/buckets/bucket-cameratraps/output/{Path(selected_rows[0]['filename']).name}",
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
    Output("validation-table", "rowData"),
    Output("add-fn-btn", "disabled"),
    Output("save-validation-btn", "disabled"),
    Input("prediction-table", "selectedRows"),
)
def display_predictions(selected_rows: list[dict]):
    """Load predicted trackers data for the selected video"""

    if not selected_rows:
        return [], True, True

    params = {"video_id": selected_rows[0]["id"]}
    df = db.run_sql_file("archive/get_trackers.sql", parameters=params)
    records = df.to_dict("records")

    return records, False, len(records) == 0


@callback(
    Output("validation-table", "rowData", allow_duplicate=True),
    Output("save-validation-btn", "disabled", allow_duplicate=True),
    Input("add-fn-btn", "n_clicks"),
    State("validation-table", "rowData"),
    State("prediction-table", "selectedRows"),
    prevent_initial_call=True,
)
def add_manual_row(n_clicks: int, current_rows: list[dict], selected_video: list[dict]):
    """Add a manual row"""

    if not n_clicks or not selected_video:
        raise PreventUpdate

    current_rows = current_rows or []
    default_label = next(iter(Classes)).value

    current_rows.append(
        {
            "tracker_id": None,
            "label": default_label,
            "original_label": None,
        }
    )

    return current_rows, False


@callback(
    Output("validation-table", "rowData", allow_duplicate=True),
    Output("save-validation-btn", "disabled", allow_duplicate=True),
    Input("validation-table", "cellClicked"),
    State("validation-table", "rowData"),
    prevent_initial_call=True,
)
def remove_manual_row(cell, current_rows):
    """Sync rowData when a manual row is deleted"""

    if not cell or cell.get("colId") != "delete":
        raise PreventUpdate

    row_index = cell.get("rowIndex")
    if row_index is None or current_rows[row_index].get("tracker_id") is not None:
        raise PreventUpdate

    current_rows.pop(row_index)
    return current_rows, len(current_rows) == 0


@callback(
    Output("prediction-table", "rowData", allow_duplicate=True),
    Output("validation-table", "rowData", allow_duplicate=True),
    Input("save-validation-btn", "n_clicks"),
    State("validation-table", "rowData"),
    State("prediction-table", "selectedRows"),
    State("date-range-picker", "value"),
    prevent_initial_call=True,
)
def save_validation(
    n_clicks: int,
    validation_rows: list[dict],
    selected_video: list[dict],
    date_range: list[str | None],
):
    """Save updated labels to the database"""

    if not n_clicks or not validation_rows or not selected_video:
        raise PreventUpdate

    params = [
        {
            "video_input_id": selected_video[0]["id"],
            "tracker_id": row.get("tracker_id"),
            "label": row["label"],
            "comments": row.get("comments"),
            "is_modified": (row.get("tracker_id") is None) or (row["label"] != row.get("original_label")),
            "validated_by": "admin",
        }
        for row in validation_rows
    ]

    db.execute_sql_file("archive/insert_video_validations.sql", parameters=params)

    return update_table(date_range), []
