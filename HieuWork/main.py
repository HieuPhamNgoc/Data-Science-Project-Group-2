from typing import Container
import pandas as pd
import plotly.express as px
import numpy as np

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

path = 'HieuWork/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx'

df = pd.read_excel(io = path, sheet_name='fossil_CO2_totals_by_country')

year = [{'label': str(c), 'value': c} for c  in df.columns[3:]]
#print(year)

app.layout = html.Div(
    children = [
        html.H1('Worldwide CO2 emission', style = {'text-align':'center'}),

        html.Div(
            children = [
            html.H3('Please choose a year:'),
            dcc.Dropdown(id = 'year',
                        options=year,
                        multi=False,
                        value = year[-1]['value'],
                        style={'width':'40%'})
            ],
            style={'width': '50%', 'margin-left': '50px'}
        ),
        html.Br(),
        dcc.Graph(id = 'co2_graph', figure = {}, style = {'margin-left':'150px'}),
        html.Br(),
        html.Div(id = 'output_container', children = [], style={'text-align':'center', 'font-size':'25px'})
    ]
)


@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id = 'co2_graph', component_property='figure')],
    [Input(component_id='year', component_property='value')]
)

def update_graph(option_slctd): # number of arguments is the same as the number of inputs
    print(option_slctd)
    print(type(option_slctd))

    container = ' CO2 emission in {}'.format(option_slctd)

    dff = df.copy()
    dff = dff[['Country', option_slctd]]
    dff[option_slctd] = np.round(dff[option_slctd], 3)
    

    fig = px.choropleth(
        data_frame=dff,
        locationmode='country names',
        locations= 'Country',
        color= option_slctd,
        range_color=[0, 6000],
        color_continuous_scale=px.colors.sequential.Aggrnyl,
        hover_data={'Country': False},
        labels={str(option_slctd): 'CO2 emission'},
        hover_name='Country'
        
    )
    fig.update_layout(margin = {'r':0,'t':0,'l':0,'b':0}) # template in ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
    return container, fig



if __name__ == '__main__':
    app.run_server(debug=True)