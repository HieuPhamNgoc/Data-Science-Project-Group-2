from typing import Container
import pandas as pd
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_excel(io='EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx', sheet_name='fossil_CO2_totals_by_country')

year = [{'label': str(c), 'value': c} for c  in df.columns[3:]]
print(year)

app.layout = html.Div([
    html.H1('Testing webpage', style = {'text-align':'left'}),

    dcc.Dropdown(id = 'year',
                 options=year,
                 multi=False,
                 value = year[0]['value'],
                 style={'width':'30%'}),

    html.Div(id = 'output_container', children = []),
    html.Br(),
    dcc.Graph(id = 'co2_graph', figure = {})

])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id = 'co2_graph', component_property='figure')],
    [Input(component_id='year', component_property='value')]
)

def update_graph(option_slctd): # number of arguments is the same as the number of inputs
    print(option_slctd)
    print(type(option_slctd))

    container = 'The year chosen was: {}'.format(option_slctd)

    dff = df.copy()
    dff = dff[['Country', option_slctd]]
    
    print(dff.head())

    fig = px.choropleth(
        data_frame=dff,
        locationmode='country names',
        locations=dff['Country'],
        color= option_slctd

    )
    return container, fig



if __name__ == '__main__':
    app.run_server(debug=True)