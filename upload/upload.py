from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import base64
import io


upload_page = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload Study Data'),
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    html.Div(id='table-container')  # This will display the table
])

# Function to parse the uploaded Excel file
def parse_contents(contents):
    # Decode the base64 contents
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        # Read the file into a pandas dataframe
        df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

# Callback to handle the file upload and display the contents
def register_callbacks(app=None):
    @app.callback(
        [Output('output-data-upload', 'children'),
        Output('table-container', 'children')],
        [Input('upload-data', 'contents')]
    )
    def update_output(contents):
        if contents is None:
            return "Upload an Excel file to get started.", None

        # Parse the uploaded Excel file
        df = parse_contents(contents)
        
        if df is not None:
            # Display a success message
            output = f"File successfully uploaded! It contains {len(df)} questions and answers."
            
            # Display the first few rows of the dataframe as a table
            return output, html.Table(
                # Header
                [html.Tr([html.Th(col) for col in df.columns])] +
                # Rows
                [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(10, len(df)))]
            )
        else:
            return "Error in file processing.", None
