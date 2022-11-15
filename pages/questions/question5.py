import dash
from dash import Input, Output, callback, ctx, dcc, html

dash.register_page(__name__, path="/question5")
layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "How many percent of the global warming we are experiencing today is caused by methane in the atmosphere?",
                    className="question",
                ),
                html.Div(
                    [
                        html.Button(
                            "20%",
                            className="stuff",
                            id="first_button_quest5",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "25%",
                            className="stuff",
                            id="second_button_quest5",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "50%",
                            className="stuff",
                            id="third_button_quest5",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "60%",
                            className="stuff",
                            id="fourth_button_quest5",
                            style={"margin": "6px"},
                        ),
                    ],
                    className="answer_4",
                ),
            ],
            id="question5",
        ),
    ]
)


@callback(
    Output("question5", "children"),
    Input("first_button_quest5", "n_clicks"),
    Input("second_button_quest5", "n_clicks"),
    Input("third_button_quest5", "n_clicks"),
    Input("fourth_button_quest5", "n_clicks"),
    prevent_initial_call=True,
)
def update_log(b1, b2, b3, b4):
    triggered_id = ctx.triggered_id
    if triggered_id == "second_button_quest5":
        return html.Div(
            [
                html.H1("You are right", className="solution"),
                dcc.Link(
                    "To Knowledge",
                    href="/graphs",
                    className="stuff next_button",
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1("Incorrect", className="solution"),
                dcc.Link(
                    "To Knowledge",
                    href="/graphs",
                    className="stuff next_button",
                ),
            ]
        )