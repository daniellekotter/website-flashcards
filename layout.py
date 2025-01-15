from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from main.navbar import navbar_item
import main.home
import upload
import study


def create_layout():
    return html.Div(children=[
        dcc.Location(id="url", refresh=False),  # To track the URL changes
        navbar_item,
        dbc.Container(id="page-content", class_name="page-content"),  # The content will change dynamically
    ])

def register_callbacks(app):
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
    )
    def display_page(pathname):
        if pathname == "/" or pathname == "/home":
            return main.home.layout
        elif pathname == "/upload":
            return upload.layout
        elif pathname == "/study":
            return study.layout
        else:
            return "404 Page Not Found"  # Default fallback if no match
