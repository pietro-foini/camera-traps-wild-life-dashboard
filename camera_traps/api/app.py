from datetime import datetime, timedelta

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, page_container, page_registry
from dash_iconify import DashIconify

from camera_traps.settings import SITES

dmc.add_figure_templates()

app = Dash(
    __name__,
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
    children=dmc.AppShell(
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
                                    DashIconify(icon="tabler:paw", width=24, color="white"),
                                    dmc.Text(children="Dashboard", fw=700, size="lg", mr="md", c="white"),
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
                                                            styles={"label": {"color": "white", "paddingLeft": "6px"}},
                                                        ),
                                                        dmc.Radio(
                                                            label="Dark",
                                                            value="dark",
                                                            color="palette.8",
                                                            styles={"label": {"color": "white", "paddingLeft": "6px"}},
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
                                ],
                            ),
                        ],
                    )
                ],
            ),
            dmc.AppShellMain(
                children=[
                    dmc.Paper(
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
                                        cols={"base": 1, "sm": 2, "md": 4},
                                        spacing="lg",
                                        pt="md",
                                        pb="xs",
                                        px="xl",
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
                                                data=[{"value": k, "label": v.get("name")} for k, v in SITES.items()],
                                                searchable=True,
                                            ),
                                            dmc.Box(visibleFrom="md"),
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
                        p="md",
                        style={"position": "relative", "zIndex": 1},
                    ),
                ]
            ),
        ],
    ),
)


@callback(
    Output("filters-collapse", "opened"),
    Input("toggle-filters-btn", "n_clicks"),
    State("filters-collapse", "opened"),
    prevent_initial_call=True,
)
def toggle_filters(n_clicks, is_open):
    """Open or close filters header"""

    return not is_open


@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("theme-radio", "value"),
    prevent_initial_call=True,
)
def switch_theme(theme_value):
    """Change the theme colorscheme"""

    return theme_value


@callback(
    Output("date-range-picker", "value"),
    Output("site-filter", "value"),
    Input("reset-filters-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(n_clicks):
    """Reset filters to default values"""

    return [datetime.now().date() - timedelta(days=30), datetime.now().date()], []
