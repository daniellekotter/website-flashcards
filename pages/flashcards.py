import dash
from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd


dash.register_page(
    __name__,
    path='/study',
    title='Study',
    name='Study',
    order=2
)


flash_card = dbc.Card(
    children=[
        dbc.CardHeader(
            id="question-div",
            className="card-title"
        ),
        dbc.CardBody(
            [
                html.P(
                    id="answer-div",
                    className="card-text"
                ),
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            "Show Answer",
                            id="show-answer-btn",
                            n_clicks=0,
                            color="secondary",
                        ),
                        dbc.Button(
                            "Correct",
                            id="correct-question-btn",
                            n_clicks=0,
                            color="success",
                        ),
                        dbc.Button(
                            "Incorrect",
                            id="incorrect-question-btn",
                            n_clicks=0,
                            color="danger",
                        ),
                    ]
                ),
            ]
        ),
    ],
    class_name="flash_card"
)


layout = dbc.Container(children=[
    dbc.Row([
        html.Br(),
        dbc.Progress(id="progress-bar", striped=True, animated=True, className="mb-3"),
        dbc.Col(flash_card, width={"size": 4, "offset": 4}),
    ]),
])


# Helper to get a random question
def get_random_card(df):
    if df.empty:
        return "No study content yet", "Please upload the content you want to study."  # Return None when the DataFrame is empty

    card = df.sample(n=1).iloc[0]
    df.drop(card.name, inplace=True)  # Remove the selected card from the DataFrame
    return card["Question"], card["Answer"]

# Store state of the current flashcard
current_card = {"question": None, "answer": None, "revealed": False}


# Callback for updating the question
@callback(
    [
        Output("question-div", "children"),
        Output("answer-div", "children"),
        Output("progress-bar", "label"),
        Output("progress-bar", "value")
    ],[
        Input("correct-question-btn", "n_clicks"),
        Input("show-answer-btn", "n_clicks"),
        Input('uploaded-data', 'data')  # Access stored data
    ],[
        State("answer-div", "children"),
        State("progress-bar", "value")
    ]
)
def update_flashcard(next_clicks, show_clicks, uploaded_data, answer_div, progress):
    if uploaded_data is None:
        return html.P("No data uploaded yet.")

    # Convert the JSON back to a DataFrame
    df = pd.read_json(uploaded_data, orient='split')

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    progress = round((next_clicks / len(df)) * 100)

    if button_id == "correct-question-btn":
        # Fetch a new card
        question, answer = get_random_card(df)
        # If the result is None, this means that all the answers have been asked
        if not question:
            return "Congrats", "You have made it to the end!", f"100%", 100

        current_card["question"] = question
        current_card["answer"] = answer
        current_card["revealed"] = False
        return question, "",  f"{progress}%", progress

    elif button_id == "show-answer-btn":
        if not current_card["revealed"]:
            current_card["revealed"] = True
            return current_card["question"], current_card["answer"], f"{progress} %", progress

    # Default return values
    return "Press Next to start!", "", "0%", 0
