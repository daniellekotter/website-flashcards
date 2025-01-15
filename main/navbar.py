from dash import html
import dash_bootstrap_components as dbc


LOGO = "assets/lightning.png"

navbar_item = dbc.Navbar(
    children=[
        dbc.Container(children=[
            dbc.Row([
                dbc.Col(children=[
                    html.Img(src=LOGO, height="30px"),
                    dbc.NavbarBrand("FlashStudy", href="/home"),
                ],
                    className="d-flex",
                    width="auto"
                ),
                dbc.Col(children=[
                    dbc.NavItem(dbc.NavLink("Upload", href="/upload")),
                    dbc.NavItem(dbc.NavLink("Study", href="/study"))
                ],
                    className="d-flex",
                    width=2
                )
            ],
                align="center",
                justify="between"
            ),
        ])
    ],
    class_name="navbar",
    dark=True
)
