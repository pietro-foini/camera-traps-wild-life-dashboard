from datetime import datetime, timedelta

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc, page_container, page_registry
from dash_iconify import DashIconify
from flask import session

from camera_traps.api.server import server
from camera_traps.data import Classes
from camera_traps.settings import SITES

app = Dash(
    __name__,
    server=server,
    use_pages=True,
    pages_folder="pages",
    assets_folder="assets",
    external_stylesheets=dmc.styles.ALL,
)
app.title = "Dashboard"

app.layout = dmc.MantineProvider(
    id="mantine-provider",
    forceColorScheme="light",
    theme={
        "colors": {
            "palette": [
                "#eaf4ed",
                "#cbe4d2",
                "#a9d3b5",
                "#85c196",
                "#66b27c",
                "#489860",
                "#2E6F40",
                "#255a34",
                "#1c4527",
                "#122f1a",
            ]
        },
        "primaryColor": "palette",
        "defaultRadius": "md",
        "fontFamily": "'Avenir Next', Avenir, system-ui, -apple-system, 'Segoe UI', sans-serif",
        "fontFamilyMonospace": "ui-monospace, 'Cascadia Code', Menlo, Monaco, monospace",
        "headings": {
            "fontFamily": "'Avenir Next', Avenir, system-ui, -apple-system, 'Segoe UI', sans-serif",
            "fontWeight": "600",
        },
    },
    children=[
        dcc.Store(id="session-user-store", storage_type="session"),
        dmc.AppShell(
            header={"height": 60},
            padding=0,
            children=[
                dmc.AppShellHeader(
                    bg="palette.6",
                    px="md",
                    style={"borderBottom": "none"},
                    children=[
                        dmc.Group(
                            justify="space-between",
                            align="center",
                            h="100%",
                            children=[
                                dmc.Group(
                                    gap="xs",
                                    children=[
                                        dcc.Link(
                                            href="/",
                                            style={"textDecoration": "none"},
                                            children=dmc.Group(
                                                gap="xs",
                                                mr="md",
                                                children=[
                                                    DashIconify(icon="tabler:paw", width=24, color="white"),
                                                    dmc.Text(children="Dashboard", fw=700, size="lg", c="white"),
                                                ],
                                            ),
                                        ),
                                        *[
                                            dmc.NavLink(
                                                label=page["name"],
                                                href=page["relative_path"],
                                                active="exact",
                                                className="nav-header-link",
                                                w="auto",
                                                px="sm",
                                                py="xs",
                                                c="white",
                                                style={"borderRadius": "6px"},
                                            )
                                            for page in page_registry.values()
                                            if page["path"] != "/"
                                        ],
                                    ],
                                ),
                                dmc.Group(
                                    gap="lg",
                                    align="center",
                                    children=[
                                        dmc.Group(
                                            gap="xs",
                                            align="center",
                                            children=[
                                                dmc.Text(children="Appearance", size="sm", fw=600, c="white"),
                                                dmc.RadioGroup(
                                                    id="theme-radio",
                                                    value="light",
                                                    size="sm",
                                                    children=dmc.Group(
                                                        gap="sm",
                                                        children=[
                                                            dmc.Radio(
                                                                label="Light",
                                                                value="light",
                                                                color="palette.8",
                                                                styles={
                                                                    "label": {"color": "white", "paddingLeft": "6px"}
                                                                },
                                                            ),
                                                            dmc.Radio(
                                                                label="Dark",
                                                                value="dark",
                                                                color="palette.8",
                                                                styles={
                                                                    "label": {"color": "white", "paddingLeft": "6px"}
                                                                },
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                            ],
                                        ),
                                        dmc.Group(
                                            gap="xs",
                                            align="center",
                                            children=[
                                                dmc.Text(children="Language", size="sm", fw=600, c="white"),
                                                dmc.Select(
                                                    id="language-select",
                                                    data=[
                                                        {"value": "en", "label": "English"},
                                                    ],
                                                    value="en",
                                                    w=120,
                                                    size="xs",
                                                    allowDeselect=False,
                                                ),
                                            ],
                                        ),
                                        dmc.Tooltip(
                                            dmc.Avatar(radius="xl", color="white"),
                                            id="user-tooltip",
                                            position="bottom",
                                            label="Guest",
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                dmc.AppShellMain(
                    children=[
                        dmc.Paper(
                            id="filters-bar",
                            px="md",
                            py="sm",
                            radius=0,
                            style={"borderBottom": "1px solid var(--mantine-color-default-border)"},
                            children=[
                                dmc.Group(
                                    gap="sm",
                                    align="center",
                                    children=[
                                        dmc.ActionIcon(
                                            id="toggle-filters-btn",
                                            variant="outline",
                                            color="palette",
                                            size="lg",
                                            radius="sm",
                                            children=DashIconify(icon="lucide:sliders-horizontal", width=20),
                                        ),
                                        dmc.Text(children="Filters", fw=500, size="sm"),
                                    ],
                                ),
                                dmc.Collapse(
                                    id="filters-collapse",
                                    opened=True,
                                    children=[
                                        dmc.SimpleGrid(
                                            cols={"base": 1, "sm": 2, "md": 5},
                                            spacing="md",
                                            pt="md",
                                            pb="xs",
                                            px="md",
                                            children=[
                                                dmc.DatePickerInput(
                                                    id="date-range-picker",
                                                    label="Date Range",
                                                    type="range",
                                                    value=[
                                                        datetime.now().date() - timedelta(days=7),
                                                        datetime.now().date(),
                                                    ],
                                                ),
                                                dmc.MultiSelect(
                                                    id="site-filter",
                                                    value=[],
                                                    label="Site",
                                                    placeholder="All",
                                                    data=[
                                                        {"value": k, "label": v.get("name")} for k, v in SITES.items()
                                                    ],
                                                    clearable=True,
                                                ),
                                                dmc.MultiSelect(
                                                    id="class-filter",
                                                    value=[],
                                                    label="Class",
                                                    placeholder="All",
                                                    data=[c.value for c in Classes],
                                                    clearable=True,
                                                ),
                                                dmc.Stack(
                                                    gap=6,
                                                    children=[
                                                        dmc.Group(
                                                            justify="space-between",
                                                            children=[
                                                                dmc.Text("Time Range", size="sm", fw=500),
                                                                dmc.Badge(
                                                                    id="hour-range-label",
                                                                    children="00:00 - 24:00",
                                                                    variant="light",
                                                                    color="palette",
                                                                    size="sm",
                                                                ),
                                                            ],
                                                        ),
                                                        dmc.RangeSlider(
                                                            id="hour-range-slider",
                                                            min=0,
                                                            max=24,
                                                            step=1,
                                                            value=[0, 24],
                                                            minRange=1,
                                                            color="palette",
                                                            marks=[
                                                                {"value": 0, "label": "00"},
                                                                {"value": 6, "label": "06"},
                                                                {"value": 12, "label": "12"},
                                                                {"value": 18, "label": "18"},
                                                                {"value": 24, "label": "24"},
                                                            ],
                                                            mb="sm",
                                                        ),
                                                    ],
                                                ),
                                                dmc.Group(
                                                    justify="flex-end",
                                                    align="flex-end",
                                                    children=[
                                                        dmc.Button(
                                                            children="Reset",
                                                            id="reset-filters-btn",
                                                            variant="outline",
                                                        )
                                                    ],
                                                ),
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        ),
                        dmc.Box(
                            page_container,
                            style={"position": "relative", "zIndex": 1},
                        ),
                    ]
                ),
            ],
        ),
    ],
)


@callback(
    Output("session-user-store", "data"),
    Output("filters-bar", "display"),
    Input("_pages_location", "pathname"),
)
def store_user_session(pathname: str):
    """Read session user data and hide filters on welcome page"""

    user = session.get("user", {})
    user_data = {
        "email": user.get("email", ""),
        "name": user.get("name", "User"),
    }

    return user_data, "none" if pathname == "/" else "block"


@callback(
    Output("filters-collapse", "opened"),
    Input("toggle-filters-btn", "n_clicks"),
    State("filters-collapse", "opened"),
    prevent_initial_call=True,
)
def toggle_filters(n_clicks: int, is_open: bool):
    """Open or close filters header"""

    return not is_open


@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("theme-radio", "value"),
    prevent_initial_call=True,
)
def switch_theme(theme_value: str):
    """Change the theme colorscheme"""

    return theme_value


@callback(
    Output("user-tooltip", "label"),
    Input("session-user-store", "data"),
)
def update_header_user(user_data: dict[str, str]):
    """Update the user tooltip"""

    return user_data.get("name", "Guest")


@callback(
    Output("hour-range-label", "children"),
    Input("hour-range-slider", "value"),
)
def update_hour_badge(hours: list[int]):
    """Update the hour range label"""

    return f"{hours[0]:02d}:00 – {hours[1]:02d}:00"


@callback(
    Output("date-range-picker", "value"),
    Output("site-filter", "value"),
    Output("class-filter", "value"),
    Output("hour-range-slider", "value"),
    Input("reset-filters-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(n_clicks: int):
    """Reset filters to default values"""

    return [datetime.now().date() - timedelta(days=30), datetime.now().date()], [], [], [0, 24]
