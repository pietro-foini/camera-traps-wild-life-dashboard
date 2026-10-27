import dash
import dash_mantine_components as dmc
from dash import Input, Output, callback, html

dash.register_page(__name__, path="/", name="Welcome")

data = [
    {
        "image": "https://images.unsplash.com/photo-1572363420552-058bd41af8c7?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "wolf",
    },
    {
        "image": "https://images.unsplash.com/photo-1785952638293-06412e0284e9?q=80&w=670&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "boar",
    },
    {
        "image": "https://images.unsplash.com/photo-1602483914471-907994df5618?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "fox",
    },
    {
        "image": "https://images.unsplash.com/photo-1630514168444-69eaf2ed8089?q=80&w=627&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "hare",
    },
    {
        "image": "https://images.unsplash.com/photo-1503256207526-0d5d80fa2f47?q=80&w=686&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "dog",
    },
    {
        "image": "https://images.unsplash.com/photo-1503777119540-ce54b422baff?q=80&w=686&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "cat",
    },
    {
        "image": "https://images.unsplash.com/photo-1560510051-3035e7d523f3?q=80&w=1118&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "weasel",
    },
    {
        "image": "https://images.unsplash.com/photo-1783868107116-fc358afb32ce?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "bear",
    },
    {
        "image": "https://images.unsplash.com/photo-1778525211398-83a1389ddda8?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "deer",
    },
    {
        "image": "https://images.unsplash.com/photo-1776023518975-239b68071e65?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "badger",
    },
    {
        "image": "https://images.unsplash.com/photo-1590079015089-875baa76cc8d?q=80&w=764&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "squirrel",
    },
    {
        "image": "https://images.unsplash.com/photo-1596733430284-f7437764b1a9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "cow",
    },
    {
        "image": "https://images.unsplash.com/photo-1767288832044-c522467b24e1?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
        "category": "bird",
    },
]


def make_card(image: str, category: str):
    """Create a card with the given image and category"""

    return dmc.Paper(
        children=[
            html.Div(
                [
                    dmc.Text(category.upper(), c="white", opacity=0.9, fw=700),
                ]
            ),
            dmc.Button(children="Explore", variant="white", color="dark"),
        ],
        shadow="md",
        p="xl",
        radius="md",
        style={
            "backgroundImage": f"url({image})",
            "height": 540,
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "space-between",
            "alignItems": "flex-start",
            "backgroundSize": "cover",
            "backgroundPosition": "center",
        },
    )


layout = dmc.Box(
    pos="relative",
    mih="calc(100vh - 120px)",
    style={"overflow": "hidden", "display": "flex", "alignItems": "center"},
    py="xl",
    px="md",
    children=[
        dmc.Container(
            size="xl",
            w="100%",
            pos="relative",
            style={"zIndex": 2},
            children=dmc.Grid(
                gutter=50,
                align="center",
                children=[
                    dmc.GridCol(
                        span={"base": 12, "md": 7},
                        children=dmc.Stack(
                            gap="md",
                            children=[
                                dmc.Badge(
                                    children="Camera Traps Monitoring",
                                    variant="light",
                                    color="palette",
                                    size="lg",
                                    w="fit-content",
                                ),
                                dmc.Title(
                                    id="welcome-user-title",
                                    order=1,
                                    style={"fontSize": "clamp(2.2rem, 4vw, 3.4rem)", "lineHeight": 1.15},
                                ),
                                dmc.Text(
                                    children="Explore the data collected by camera traps, monitor active sites, and analyze wildlife statistics.",
                                    size="lg",
                                    c="dimmed",
                                ),
                            ],
                        ),
                    ),
                    dmc.GridCol(
                        span={"base": 12, "md": 5},
                        children=dmc.Carousel(
                            [dmc.CarouselSlide(make_card(d["image"], d["category"])) for d in data],
                            id="carousel-cards",
                            w=500,
                            emblaOptions={"loop": True, "align": "start"},
                        ),
                    ),
                ],
            ),
        ),
    ],
)


@callback(
    Output("welcome-user-title", "children"),
    Input("session-user-store", "data"),
)
def render_welcome_message(user: dict | None):
    """Render welcome message"""

    name = (user or {}).get("name", "Guest")
    return [
        "Welcome, ",
        dmc.Text(
            f"{name}!",
            span=True,
            inherit=True,
            variant="gradient",
            gradient={"from": "palette.5", "to": "palette.8", "deg": 45},
        ),
    ]
