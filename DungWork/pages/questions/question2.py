from multiprocessing.sharedctypes import Value
from tkinter.ttk import Style
import dash
from dash import html, dcc, callback, Input, Output, ctx, dcc
from dash_extensions.enrich import DashProxy, html, Input, Output, State
from dash_extensions import EventListener
from dash.exceptions import PreventUpdate
import time
dash.register_page(__name__)
event = {"event": "click", "props": ["srcElement.className", "srcElement.innerText"]}

layout = html.Div([
    html.Div([
    html.H1("How many people in the world live in areas that are 5 meters or less above sea level?",
    style={'margin-left':'30%', 'margin-right':'30%'})
    ,
    html.Div([
        html.Button("Around 11%", className="stuff", id='first_button', style={'margin':'6px'}),
        html.Button("Around 31%", className="stuff", id='second_button', style={'margin':'6px'}),
        html.Button("Around 51%", className="stuff", id='third_button', style={'margin':'6px'}),
      ], style={ 'display':'flex','flex-direction': 'column', 'margin-left':'30%', 'margin-right':'30%'})
    ], id='question2'),
])
@callback(
    Output('question2','children'),
    Input('first_button', 'n_clicks'),
    Input('second_button', 'n_clicks'),
    Input('third_button', 'n_clicks'),
    prevent_initial_call=True
)
def update_log(b1,b2,b3):
    triggered_id = ctx.triggered_id
    if triggered_id == 'first_button' or triggered_id == 'second_button':
         return html.Div([
            html.H1(" Far to the beach ", style={'margin-left':'30%', 'margin-right':'30%'}),
            html.H2("Most people overestimate the population at risk from rising sea levels. When you overestimate how many homes can be reached by rising sea levels, you may think it’s impossible for so many people to find new places to live.",
            style={'margin-left':'30%', 'margin-right':'30%'}),
            dcc.Link("To Knowledge", href="/", style={'margin-left':'44%', 'margin-right':'30%'}, className="stuff"),
         ])
    else:
         return html.Div([
            html.H1("You are right", style={'margin-left':'30%', 'margin-right':'30%'}),
            html.H2("But 77% of people answer wrongly. Most people overestimate the population at risk from rising sea levels. When they overestimate how many homes can be reached by rising sea levels, they may think it’s impossible for so many people to find new places to live.",
            style={'margin-left':'30%', 'margin-right':'30%'}
            ),
            dcc.Link("To Knowledge", href="/", style={'margin-left':'44%', 'margin-right':'30%'}, className="stuff"),
            ])
