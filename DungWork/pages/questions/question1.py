from tkinter.ttk import Style
import dash
from dash import html, dcc, callback, Input, Output, ctx, dcc
from dash_extensions.enrich import DashProxy, html, Input, Output, State
from dash_extensions import EventListener
from dash.exceptions import PreventUpdate

event = {"event": "click", "props": ["srcElement.className", "srcElement.innerText"]}

layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "How much of the excess heat from global warming is captured in the oceans?",
                    style={"margin-left": "30%", "margin-right": "30%"},
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
                    },
                ),
            ],
            id="question1",
        ),
    ]
)


@callback(
    Output("question1", "children"),
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
                    style={"margin-left": "30%", "margin-right": "30%"},
                ),
                dcc.Link(
                    "To Knowledge",
                    href="/",
                    style={"margin-left": "44%", "margin-right": "30%"},
                    className="stuff",
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H1(
                    "You are right", style={"margin-left": "30%", "margin-right": "30%"}
                ),
                html.H2(
                    "But 90%% of people answer wrongly. Most people are unaware that most global warming is hiding in the seas. As long as they think global warming is all about air temperature, they won’t realize the size of the problem.",
                    style={"margin-left": "30%", "margin-right": "30%"},
                ),
                dcc.Link(
                    "To Knowledge",
                    href="/",
                    style={"margin-left": "44%", "margin-right": "30%"},
                    className="stuff",
                ),
            ]
        )
