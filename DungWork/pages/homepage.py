import dash
from dash import html, dcc, Input, Output, callback, ctx

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "How much of the excess heat from global warming is captured in the oceans?",
                    style={
                        "margin-left": "30%",
                        "margin-right": "30%",
                        "font-size": "60px",
                    },
                ),
                html.Div(
                    [
                        html.Button(
                            "Around 10%",
                            className="stuff",
                            id="first_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "Around 50%",
                            className="stuff",
                            id="second_button",
                            style={"margin": "6px"},
                        ),
                        html.Button(
                            "Around 90%",
                            className="stuff",
                            id="third_button",
                            style={"margin": "6px"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "margin-left": "30%",
                        "margin-right": "30%",
                        "font-size": "40px",
                    },
                ),
            ],
            id="hook_question",
            style={"margin-top": "15%"},
        ),
    ]
)


@callback(
    Output("hook_question", "children"),
    Input("first_button", "n_clicks"),
    Input("second_button", "n_clicks"),
    Input("third_button", "n_clicks"),
    prevent_initial_call=True,
)
def update_log(b1, b2, b3):
    triggered_id = ctx.triggered_id
    if triggered_id == "first_button" or triggered_id == "second_button":
        return html.Div(
            [
                html.H1(
                    "Don’t look for global warming outside your window",
                    style={
                        "margin-left": "30%",
                        "margin-right": "30%",
                        "font-size": "70px",
                    },
                ),
                dcc.Link(
                    "To Knowledge",
                    href="/graphs",
                    style={
                        "margin-left": "44%",
                        "margin-right": "30%",
                        "font-size": "40px",
                    },
                    className="stuff",
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1(
                    "You are right",
                    style={
                        "margin-left": "30%",
                        "margin-right": "30%",
                        "font-size": "70px",
                    },
                ),
                html.P(
                    "But 90%% of people answer wrongly. Most people are unaware that most global warming is hiding in the seas. As long as they think global warming is all about air temperature, they won’t realize the size of the problem.",
                    style={
                        "margin-left": "30%",
                        "margin-right": "30%",
                        "font-size": "30px",
                    },
                ),
                dcc.Link(
                    "To Knowledge",
                    href="/graphs",
                    style={
                        "margin-left": "44%",
                        "margin-right": "30%",
                        "font-size": "40px",
                    },
                    className="stuff",
                ),
            ]
        )
