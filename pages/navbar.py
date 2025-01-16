import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc


nav_links = [
    dbc.NavItem(dbc.NavLink(
        page["name"],
        href=page["path"],
        active="exact",
    ))
    for page in dash.page_registry.values()
]

navbar_item = dbc.Navbar(
    children=[
        dbc.Container(children=[
            dbc.Row([
                dbc.Col(children=[
                    html.Img(src="assets/lightning.png", height="30px"),
                    dbc.NavbarBrand("FlashStudy", href="/home"),
                ],
                    className="d-flex",
                    width="auto"
                ),
                dbc.Col(children=nav_links,
                    className="d-flex",
                    width=2
                ),
            ],
                align="center",
                justify="between"
            )
        ])
    ],
    class_name="navbar",
    dark=True
)
