import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(
    __name__,
    path='/',
    title='Home',
    name='Home',
    order=0
)

layout = dbc.Container(
    children=[
        dbc.Row(
            dbc.Col(
                [
                    html.Div([
                        html.H2("Welcome!", style={"textAlign": "center"}),
                        html.Img(src="assets/study.png", height="600px"),
                        dbc.Button(
                            "Get started!",
                            id="get-started-button",
                            color="danger",
                            href="/upload",
                            className="d-grid gap-2 col-4 mx-auto"
                        ),
                    ], className="d-grid gap-2 col-6 mx-auto")
                ],
            ),
            justify="center",
        ),
    ]
)
