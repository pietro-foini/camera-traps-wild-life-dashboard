import dash_mantine_components as dmc


def create_card(id: str, title: str):
    """Creates a card with the given title"""

    return dmc.Card(
        withBorder=True,
        radius="md",
        shadow="sm",
        p="md",
        style={
            "backgroundImage": "linear-gradient(135deg, transparent 55%, #48986026 100%)",
            "borderLeft": "4px solid #2E6F40",
        },
        children=[
            dmc.Text(children=title, size="xs", fw=400, tt="uppercase"),
            dmc.Text(
                children="—",
                id=id,
                size="xl",
                fw=700,
                mt="xs",
            ),
        ],
    )
