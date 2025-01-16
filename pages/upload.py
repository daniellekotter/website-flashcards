import pandas as pd
import base64
import io
import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, Input, Output, State, callback


dash.register_page(
    __name__,
    path='/upload',
    title='Upload',
    name='Upload',
    order=1
)


upload_form = dbc.Card(
    [
        dbc.CardHeader("Upload Study Content"),
        dbc.CardBody(
            dbc.Form([
                dbc.Row([
                    dbc.Label("Choose an Excel File:"),
                    dcc.Upload(
                        id="upload-data",
                        children=html.Button("Upload File", className="btn btn-danger"),
                        multiple=False
                    ),
                ]),
                dbc.Row([
                    dbc.Label("Select study manner:"),
                    dbc.RadioItems(
                        id='study-order-dropdown',
                        options=[
                            {'label': 'Random', 'value': 'random'},
                            {'label': 'In Order', 'value': 'in_order'}
                        ],
                        value='random',
                        className="mb-3"
                    ),
                ]),
                html.Div(
                    dbc.Button("Submit", id="submit-button", color="danger", disabled=False),
                    className="d-grid gap-2 col-6 mx-auto",
                ),
            ]),
        ),
    ],
)


upload_content = dbc.Card(
    [
        dbc.CardHeader("Study Content"),
        dbc.CardBody(children=[
            html.Div(id='output-file-info'),
            html.Div(id='table-container', className="mt-3"),
            dcc.Store(id='form-submitted', data=False),  # Store to track form submission status,
            dbc.Button("Start Studying", id="start-button", href= "/study", color="danger", disabled=True)
        ])
    ]
)


layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col(upload_form,
                    width=3),
            dbc.Col(upload_content,
                    width=8)
        ])
    ]
)


@callback(
    [
        Output('output-file-info', 'children'),  # Feedback for file upload
        Output('table-container', 'children'),  # Display table with file content
        Output('upload-data', 'disabled'),      # Disable upload after submission
        Output('submit-button', 'disabled'),    # Disable submit button after processing
        Output('start-button', 'disabled'),     # Enable start button after submission
        Output('form-submitted', 'data'),       # Track if form is submitted
    ],
    [
        Input('submit-button', 'n_clicks'),      # Trigger when submit button is clicked
    ],
    [
        State('study-order-dropdown', 'value'),  # Study order (random/in order)
        State('form-submitted', 'data'),         # Form submission status
        State('upload-data', 'contents'),        # Uploaded file contents
        State('upload-data', 'filename'),        # Uploaded file name
    ]
)
def update_table(n_clicks_submit, study_order, form_submitted, file_contents=None, filename=None):
    # If no file is uploaded, return a message
    if file_contents is None:
        return "Please upload an Excel file.", None, False, False, True, False

    # If form is already submitted or submit button not clicked, do nothing
    if n_clicks_submit is None or form_submitted:
        return "", None, False, False, True, form_submitted

    try:
        # Decode and load the Excel file into a DataFrame
        content_type, content_string = file_contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_excel(io.BytesIO(decoded))

        # Shuffle rows if 'random' is selected
        if study_order == 'random':
            df = df.sample(frac=1).reset_index(drop=True)

        # Generate table header and body
        table_header = html.Thead(html.Tr([html.Th(col) for col in df.columns]))
        table_body = html.Tbody([
            html.Tr([html.Td(df.iloc[i, col]) for col in range(len(df.columns))])
            for i in range(len(df))
        ])
        table = dbc.Table(
            [table_header, table_body],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
        )

        # Return feedback, display table, disable upload and submit, and enable start button
        return (
            f"File '{filename}' uploaded and processed successfully.",
            table,
            True,  # Disable upload
            False,  # Disable submit
            False, # Disable start
            True   # Form is submitted
        )

    except Exception as e:
        # Handle file processing errors
        return f"Error processing file: {str(e)}", None, False, False, True, form_submitted
