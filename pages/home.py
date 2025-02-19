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
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src="assets/study.png",
                                    className="overlay-img"
                                ),
                                dbc.Button(
                                    "Get started!",
                                    id="get-started-button",
                                    color="danger",
                                    href="/upload",
                                    className="overlay-btn col-2"
                                ),
                            ],
                            className="overlay-img-container"
                        ),
                    ]
                ),
            ),
            justify="center",
        ),
    ],
    fluid=True,
    style={"margin": "0px", "padding": "0px"}
)