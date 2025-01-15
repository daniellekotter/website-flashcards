import dash
import dash_bootstrap_components as dbc
import layout
import upload
import study


# Initialize the Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)
app.title = "Flashcard Study"

# Initialize layout of the app
app.layout = layout.create_layout()

layout.register_callbacks(app)
upload.register_callbacks(app)
study.register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
