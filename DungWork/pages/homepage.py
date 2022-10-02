import dash
from dash import html, dcc, Input, Output, callback

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='This is our Home page'),

    html.Div(children='''
        This is our Home page content.
    '''),
    html.Div([
        "How many friends do you have: ",
        dcc.Input(id='my-input', value='', type='number')
    ]),
    html.Div([
        "What you can do:",
        dcc.Checklist(
    ['Walk/cycle to work','Use better energy home appliance', 'Cook more at home to reduce food waste'], 
    [],
    id='activities'
    )
    ]),
    html.Br(),
    html.Div(id='my-output'),
])
@callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value'),
    Input('activities','value'),
    prevent_initial_call=True
)
def update_output_div(input_value, activities):
    if len(activities) == 0 or input_value is None :
        ans = 0
        return ""
    else:
        ans = input_value * len(activities) 
        return html.H1("You can reduce {} tons carbon emission by 2050".format(ans), style={'margin-left':'35%', 'margin-right':'30%', 'color':'red'})
