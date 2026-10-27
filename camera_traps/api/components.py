import dash_mantine_components as dmc
from dash_iconify import DashIconify


def create_title(title: str, info: str = ""):
    """Create title with given info"""

    return dmc.Group(
        gap=6,
        align="center",
        justify="center",
        children=[
            dmc.Text(children=title, size="lg", fw=400),
            dmc.Tooltip(
                label=info,
                multiline=True,
                color="#2E6F40",
                w=280,
                transitionProps={
                    "transition": "skew-up",
                    "duration": 200,
                    "timingFunction": "ease",
                },
                children=DashIconify(
                    icon="ic:outline-help-outline",
                    width=15,
                    style={"display": "block", "cursor": "pointer"},
                ),
            ),
        ],
    )


def create_card(id: str, title: str, info: str = ""):
    """Creates a card with the given title and info"""

    return dmc.Card(
        withBorder=True,
        radius="md",
        shadow="sm",
        p="md",
        style={
            "backgroundImage": ("linear-gradient(135deg, transparent 55%, #48986026 100%)"),
            "borderLeft": "4px solid #2E6F40",
        },
        children=[
            dmc.Group(
                gap=6,
                align="center",
                children=[
                    dmc.Text(children=title, size="xs", fw=400, tt="uppercase"),
                    dmc.Tooltip(
                        label=info,
                        multiline=True,
                        color="#2E6F40",
                        maw=280,
                        transitionProps={
                            "transition": "skew-up",
                            "duration": 200,
                            "timingFunction": "ease",
                        },
                        children=DashIconify(
                            icon="ic:outline-help-outline",
                            width=15,
                            style={"display": "block", "cursor": "pointer"},
                        ),
                    ),
                ],
            ),
            dmc.Text(
                children="—",
                id=id,
                size="xl",
                fw=700,
                mt="xs",
            ),
        ],
    )
