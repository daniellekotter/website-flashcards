import dash
import dash_bootstrap_components as dbc
from dash import html, dcc


# Initialize the Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    use_pages=True
)

app.title = "Flashcard Study"


nav_drop = [
    dbc.NavItem(dbc.NavLink(
        page["name"],
        href=page["path"],
        active="exact",
    ))
    for page in dash.page_registry.values()
    if page["module"] != "pages.not_found_404" and page["name"] != "Home"
]

navbar_item = dbc.Navbar(
    children=[
        dbc.Container(children=[
            dbc.Row([
                dbc.Col(children=[
                    html.Img(src="assets/lightning.png", height="30px"),
                    dbc.NavbarBrand("FlashStudy", href="/"),
                ],
                    className="d-flex",
                    width="auto"
                ),
                dbc.Col(children=nav_drop,
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

# Initialize layout of the app
app.layout = html.Div(children=[
    dcc.Location(id="url", refresh=False),  # To track the URL changes
    navbar_item,
    html.Div(
        dash.page_container,
        className="page-content"
    )
    
])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
