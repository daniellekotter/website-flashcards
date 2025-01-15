from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(children=[
     dbc.Row(
        dbc.Col(
            [
                html.H2("Welcome!", style={"textAlign": "center"}),
                html.Img(src="assets/study.png", height="400px"),
            ],
            width={"size": 6},
        ),
        justify="center",
    ),
])
