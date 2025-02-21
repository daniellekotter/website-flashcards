import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from io import StringIO
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
            ]
        ),
        dbc.ButtonGroup(
            [
                dbc.Button(
                    "Show Answer",
                    id="show-answer-btn",
                    n_clicks=0,
                    color="secondary"
                ),
                dbc.Button(
                    "Correct",
                    id="correct-question-btn",
                    n_clicks=0,
                    color="success"
                ),
                dbc.Button(
                    "Incorrect",
                    id="incorrect-question-btn",
                    n_clicks=0,
                    color="danger"
                ),
            ]
        ),
    ],
    class_name="flash-card"
)


layout = dbc.Container(children=[
    dbc.Row([
        html.Div(
            dbc.Progress(id="progress-bar", striped=True, animated=True, className="mb-3 mt-1"),
        ),
        dbc.Col(flash_card, width={"size": 4, "offset": 4}),
    ]),
    dcc.Store(id='uploaded-data', storage_type='session'),
    dcc.Store(id='current-questions', storage_type='session'),
    dcc.Store(id='correct-answers', storage_type='session', data=[]),
    ],
    style={"padding": "10px 20px 10px 20px"}
)


@callback(
    Output('current-questions', 'data', allow_duplicate=True),
    Input('url', 'pathname'),
    State('uploaded-data', 'data'),
    prevent_initial_call='initial_duplicate'
)
def initialize_questions(pathname, uploaded_data):
    # Activating this callback when navigating to this page
    if pathname == '/study' and uploaded_data:
        df = pd.read_json(StringIO(uploaded_data), orient='split')
        questions = df.to_dict('records')
        return questions
    return []


# Display Flashcard and Handle Logic
@callback(
    [
        Output("question-div", "children"),
        Output("answer-div", "children"),
        Output("progress-bar", "label"),
        Output("progress-bar", "value"),
        Output('current-questions', 'data'),
        Output('correct-answers', 'data')
    ],
    [
        Input('url', 'pathname'),
        Input("show-answer-btn", "n_clicks"),
        Input("correct-question-btn", "n_clicks"),
        Input("incorrect-question-btn", "n_clicks")
    ],
    [
        State("current-questions", "data"),
        State("correct-answers", "data"),
        State("answer-div", "children")
    ]
)
def update_flashcard(pathname, show_clicks, correct_clicks, incorrect_clicks, questions, correct_answers, answer_div):
    if not questions:
        return "No Questions", "Please upload the content you want to study.", "0%", 0, [], []
    
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print("button pressed: " + button_id)
    # Get the first question
    current_question = questions[0]

    if button_id == "show-answer-btn":
        # Show the answer
        return (
            current_question["Question"],
            current_question["Answer"],
            get_progress_label(correct_answers, questions),
            get_progress_value(correct_answers, questions),
            questions,
            correct_answers
        )

    elif button_id == "correct-question-btn":
        # Move question to correct answers and go to next question
        correct_answers.append(current_question)
        questions.pop(0)

        # If all questions are done, show completion message
        if not questions:
            return (
                "Congrats!",
                f"You've answered all questions! Correct: {len(correct_answers)} / {len(correct_answers)}",
                "100%",
                100,
                questions,
                correct_answers
            )

        # Move to the next question
        next_question = questions[0]
        return (
            next_question["Question"],
            "",
            get_progress_label(correct_answers, questions),
            get_progress_value(correct_answers, questions),
            questions,
            correct_answers
        )

    elif button_id == "incorrect-question-btn":
        # Keep the question in the list and go to the next
        questions.append(questions.pop(0))
        
        # Move to the next question
        next_question = questions[0]
        return (
            next_question["Question"],
            "",
            get_progress_label(correct_answers, questions),
            get_progress_value(correct_answers, questions),
            questions,
            correct_answers
        )

    # Default display
    return (
        current_question["Question"],
        "",
        get_progress_label(correct_answers, questions),
        get_progress_value(correct_answers, questions),
        questions,
        correct_answers
    )


# Progress Helper Functions
def get_progress_label(correct_answers, questions):
    total = len(correct_answers) + len(questions)
    correct = len(correct_answers)
    return f"{correct} / {total} Correct"

def get_progress_value(correct_answers, questions):
    total = len(correct_answers) + len(questions)
    correct = len(correct_answers)
    return (correct / total) * 100 if total > 0 else 0
