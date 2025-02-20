import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(
    __name__,
    path='/stats',
    title='Stats',
    name='Stats',
    order=3
)

layout = dbc.Container(children=[
     dbc.Row(
        dbc.Col(
            [
                html.H2("Stats", style={"textAlign": "center"}),
            ],
            width={"size": 6},
        ),
        justify="center",
    ),
])
