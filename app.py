import dash
import dash_bootstrap_components as dbc
import layout
import upload
import main.navbar as navbar


# Initialize the Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(
    external_stylesheets=external_stylesheets,
)
app.title = "Flashcard Study"

# Initialize layout of the app
app.layout = layout.create_layout()

navbar.register_callbacks(app)
layout.register_callbacks(app)
upload.register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
