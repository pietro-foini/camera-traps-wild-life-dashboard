from datetime import date, timedelta

import dash_mantine_components as dmc
from dash import Dash, page_container, page_registry

app = Dash(
    __name__,
    use_pages=True,
    pages_folder="pages",
    assets_folder="assets",
)
app.title = "Dashboard"

app.layout = dmc.MantineProvider(
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
        "fontFamily": "'Inter', sans-serif",
    },
    children=dmc.AppShell(
        header={"height": 60},
        padding="md",
        children=[
            dmc.AppShellHeader(
                bg="palette.6",
                px="md",
                c="red",
                children=[
                    dmc.Group(
                        justify="space-between",
                        align="center",
                        h="100%",
                        children=[
                            dmc.Group(
                                gap="xs",
                                children=[
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
                                            style={"borderRadius": "6px"},
                                        )
                                        for page in page_registry.values()
                                    ],
                                ],
                            ),
                            dmc.DatePickerInput(
                                id="date-range-picker",
                                type="range",
                                placeholder="Select date interval",
                                value=[
                                    date.today() - timedelta(days=30),
                                    date.today(),
                                ],
                                w=360,
                                clearable=True,
                            ),
                        ],
                    )
                ],
            ),
            dmc.AppShellMain(page_container),
        ],
    ),
)
