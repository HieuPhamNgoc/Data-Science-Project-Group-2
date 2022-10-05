import pandas as pd
import plotly.express as px
import numpy as np
import pycountry_convert as pc

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# http://127.0.0.1:8050/ to go to the website

app = dash.Dash(__name__)

path = 'HieuWork/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx'

df_CO2_country = pd.read_excel(io = path, sheet_name='fossil_CO2_totals_by_country')

nordic_countries = ['Denmark', 'Finland', 'Iceland', 'Norway', 'Sweden', 'Greenland', 'Faroes']

# Convert country name into continent name

def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    except:
        return 'Unspecified'
    return country_continent_name

df_CO2_country['Continent'] = df_CO2_country['Country'].apply(lambda x: country_to_continent(x))

region = [{'label':c, 'value': c} for c in ['World', 'Asia', 'Africa', 'Europe', 'North America', 'Nordic', 'Oceania', 'South America']]

year = [{'label': str(c), 'value': c} for c  in df_CO2_country.columns[3:]]
#print(year)

app.layout = html.Div(
    children = [
        html.H1('Worldwide CO2 emission', style = {'text-align':'center'}),

        html.Div(
            children = [
            html.H3('Choose a region:'),
            dcc.Dropdown(id = 'region',
                        options=region,
                        multi=False,
                        value = 'World',
                        style={'width':'40%'})
            ],
            style={'width': '50%', 'margin-left': '50px'}
        ),
        html.Br(),
        dcc.Graph(id = 'co2_graph', figure = {}, style = {'margin-left':'150px'}),
        html.Br(),
        html.Div(
            children = 
                [dcc.Slider(min = 1970, 
                            max = 2021, 
                            step = 1, 
                            value = 2021, 
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": False}, 
                            id = 'year_slider')],
            style = {'width': '50%', 'margin-left':'480px'}
        ),
        html.Div(id = 'output_container', children = [], style={'text-align':'center', 'font-size':'25px'})
    ]
)


@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id = 'co2_graph', component_property='figure')],
    [Input(component_id='region', component_property='value'),
    Input(component_id='year_slider', component_property='value')]
)

def update_graph(region_slctd,year_slctd): # number of arguments is the same as the number of inputs
    print(region_slctd)
    print(type(region_slctd))

    print(year_slctd)
    print(type(year_slctd))

    container = ' CO2 emission in {}'.format(year_slctd)

    if (region_slctd == 'World'):
        df_CO2 = df_CO2_country.copy()

    elif (region_slctd == 'Nordic'):
        df_CO2 = df_CO2_country[df_CO2_country['Country'].isin(nordic_countries)]

    else:
        df_CO2 = df_CO2_country[df_CO2_country['Continent'] == region_slctd]

    df_CO2 = df_CO2[['Country', year_slctd]]
    df_CO2[year_slctd] = np.round(df_CO2[year_slctd], 3)
    

    fig = px.choropleth(
        data_frame=df_CO2,
        locationmode='country names',
        locations= 'Country',
        color= year_slctd,
        range_color=[0, 6000],
        color_continuous_scale=px.colors.sequential.Aggrnyl,
        hover_data={'Country': False},
        labels={str(year_slctd): 'CO2 emission'},
        hover_name='Country'
        
    )
    fig.update_layout(margin = {'r':0,'t':0,'l':0,'b':0}) # template in ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
    return container, fig



if __name__ == '__main__':
    app.run_server(debug=True)