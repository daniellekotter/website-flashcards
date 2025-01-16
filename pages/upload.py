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
                    [
                        dbc.Button("Submit", id="submit-button", color="danger", disabled=False, className="me-2"),
                        dbc.Button("Reset", id="reset-button", color="secondary", disabled=True)
                    ],
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
            dcc.Store(id='form-submitted', data=False),  # Store to track form submission status
            dbc.Button("Start Studying", id="start-button", href="/study", color="danger", disabled=True)
        ])
    ]
)

layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col(upload_form, width=3),
            dbc.Col(upload_content, width=8)
        ])
    ]
)

@callback(
    [
        Output('output-file-info', 'children'),  # Feedback for file upload
        Output('table-container', 'children'),  # Display table with file content
        Output('upload-data', 'disabled'),      # Disable upload after submission
        Output('submit-button', 'disabled'),    # Disable submit button after processing
        Output('reset-button', 'disabled'),     # Enable reset button
        Output('start-button', 'disabled'),     # Enable start button after submission
        Output('form-submitted', 'data'),       # Track if form is submitted
    ],
    [
        Input('submit-button', 'n_clicks'),
        Input('reset-button', 'n_clicks'),
    ],
    [
        State('study-order-dropdown', 'value'),  # Study order (random/in order)
        State('form-submitted', 'data'),         # Form submission status
        State('upload-data', 'contents'),        # Uploaded file contents
        State('upload-data', 'filename'),        # Uploaded file name
    ]
)
def update_table(n_clicks_submit, n_clicks_reset, study_order, form_submitted, file_contents=None, filename=None):
    start_outcome = "Please upload an Excel file.", None, False, False, True, True, False
    if file_contents is None:
        return start_outcome

    if n_clicks_reset is not None and form_submitted:
        return start_outcome

    try:
        content_type, content_string = file_contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_excel(io.BytesIO(decoded))

        if study_order == 'random':
            df = df.sample(frac=1).reset_index(drop=True)

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

        return (
            f"File '{filename}' uploaded and processed successfully.",
            table,
            True,  # Disable upload
            True,  # Disable submit
            False, # Enable reset button
            False, # Enable start button
            True   # Form is submitted
        )

    except Exception as e:
        return f"Error processing file: {str(e)}", None, False, False, True, True, True
