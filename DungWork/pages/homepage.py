import dash
import random
import math
from dash import html, dcc, Input, Output, callback

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.Div([
        "How many friends do you have: ",
        dcc.Input(id='my-input', value='', type='number', min = 1)
    ]),
    html.Div([
        "What you can do:",
        dcc.Checklist(
    ["Live car free", "Eat a plant based diet", "Recycle","Hang dry clothes"], 
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
        # Assume that each year, you are able to persuade 10% of your friends to follow your path
        # and then your friends, which has the same number of friends as you, will do the same.
        # We can have a simple simulation like this
        each_person_reduce = 0
        if "Live car free" in activities:
            each_person_reduce += 2.2
        if "Eat a plant based diet" in activities:
            each_person_reduce += 0.8
        if "Recycle" in activities:
            each_person_reduce += 0.2
        if "Hang dry clothes" in activities:
            each_person_reduce += 0.2
        current_number_doing_activities = input_value
        ans = 0
        for i in range(2022, 2051):
            ran_percentage = random.randint(5,30)
            current_number_doing_activities += math.floor(current_number_doing_activities * ran_percentage / 100)
            ans += current_number_doing_activities * each_person_reduce 
        return html.H1("You can reduce {:0.0f} tons carbon emission by 2050".format(ans,0), style={'margin-left':'35%', 'margin-right':'30%', 'color':'red'})
