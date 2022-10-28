import pandas as pd
import dash
import openpyxl
import pycountry_convert as pc

from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import plotly.express as px

#### Preprocessing data
# CO2 per capita
df_CO2_capita = pd.read_excel(io = 'LinhWork/co2_by_capita.xlsx')
df_CO2_capita = df_CO2_capita.drop(columns=['Substance', 'EDGAR Country Code'])
scope = list(df_CO2_capita["Country"].unique())
df_CO2_capita = pd.melt(df_CO2_capita, id_vars='Country', value_vars= df_CO2_capita.columns[1:],  var_name='Year', value_name='CO2_per_capita')
df_CO2_capita['Year'] = df_CO2_capita['Year'].astype("int")
df_CO2_capita['Country'] = df_CO2_capita['Country'].astype("string")

# GDP per capita
df_GDP_capita = pd.read_excel(io = 'LinhWork/GDP_per_capita.xlsx', skiprows = 3)
df_GDP_capita = df_GDP_capita.drop(columns= df_GDP_capita.columns[1:34])
df_GDP_capita = df_GDP_capita.rename(columns={"Country Name": "Country"})
df_GDP_capita = pd.melt(df_GDP_capita, id_vars='Country', value_vars= df_GDP_capita.columns[1:],  var_name='Year', value_name='GDP_per_capita')
df_GDP_capita['Year'] = df_GDP_capita['Year'].astype("int")
df_GDP_capita['Country'] = df_GDP_capita['Country'].astype("string")

# Population
df_population = pd.read_csv('LinhWork/Population.csv', skiprows = 4)
df_population = df_population.drop(columns= df_population.columns[1:4])
df_population = df_population.drop(columns= df_population.columns[-1])
df_population = df_population.rename(columns={"Country Name": "Country"})
df_population = pd.melt(df_population, id_vars='Country', value_vars= df_population.columns[1:],  var_name='Year', value_name='Population')
df_population['Year'] = df_population['Year'].astype("int")
df_population['Country'] = df_population['Country'].astype("string")
df_population = df_population.dropna()

# Final dataset
df = pd.merge(df_CO2_capita, df_GDP_capita, on=["Country","Year"],how = 'inner')
df = pd.merge(df, df_population, on=["Country","Year"],how = 'inner')

# Group by country
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

df['Continent'] =  df['Country'].apply(lambda x: country_to_continent(x))

# Add Nordics into data sets
df_nordics = df[df['Country'].isin(nordic_countries)]
df_nordics['Continent'] = 'Nordics'
df = pd.concat([df, df_nordics])

# Region
region = [{'label':c, 'value': c} for c in ['World', 'Asia', 'Africa', 'Europe', 'North America', 'Nordic', 'Oceania', 'South America']]
df = df[df['Continent'] != 'Unspecified']

### DASH
app = Dash(__name__)

app.layout = html.Div(
    children= [
        html.H1('GDP per capita and CO2 emissions per capita by region and by country', style = {'text-align':'center'}),
        html.Div(
            children= [
                html.Div([
                    html.Br(),
                    dcc.RadioItems(
                        ['Linear', 'Log'],
                        'Log',
                        id='crossfilter-type',
                        #labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                        )
                        ],
                        style={'width': '49%', 'display': 'inline-block'}),
        ]),
        html.Br(),


html.Div([
    dcc.Graph(
        id='scatterplot-percapita',
        hoverData={'points': [{'id': 'Finland'}]}
    )
    ], style={'width': '55%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '40%'}),
    ])

@app.callback(
    Output('scatterplot-percapita', 'figure'),
    Input('crossfilter-type', 'value')
    )



def update_graph( type):

    fig = px.scatter(
         df,
         x="GDP_per_capita", 
         y="CO2_per_capita",
         size="Population", 
         color='Continent',
         hover_name= "Country",
         animation_frame="Year",
         animation_group="Country",
         size_max=55
         ) 
    
    fig.update_traces(customdata= df['Country'])

    fig.update_xaxes(
        title= 'GDP per capita (current US$)', 
        type='linear' if type == 'Linear' else 'log',
        )

    fig.update_yaxes(
        title= 'CO2 per capita (Tonnes/person)',
        type='linear' if type == 'Linear' else 'log')

    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
        hovermode='closest',
        height= 500,
        transition_duration=500 )
    return fig


def create_time_series(filtered_df, axis_type, title, y_axis):
    fig = px.scatter(filtered_df, x='Year', y=y_axis)
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        type='linear' if axis_type == 'Linear' else 'log',
        title = "CO2/capita (tonnes/person)" if y_axis == 'CO2_per_capita' else 'GDP/capita (current US$)')
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)
    fig.update_layout(height=255, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

@app.callback(
    Output('x-time-series', 'figure'),
    Input('scatterplot-percapita', 'hoverData'),
    Input('crossfilter-type', 'value'))


def update_y_timeseries(hoverData, axis_type):
    country_name = hoverData['points'][0]['id']
    if country_name in nordic_countries:
        filtered_df = df_nordics[df_nordics['Country'] == country_name]
    else:
        filtered_df = df[df['Country'] == country_name]
    title = country_name
    return create_time_series(filtered_df, axis_type, title, 'GDP_per_capita')


@app.callback(
    Output('y-time-series', 'figure'),
    Input('scatterplot-percapita', 'hoverData'),
    Input('crossfilter-type', 'value'))


def update_x_timeseries(hoverData, axis_type):
    country_name = hoverData['points'][0]['id']
    if country_name in nordic_countries:
        filtered_df = df_nordics[df_nordics['Country'] == country_name]
    else:
        filtered_df = df[df['Country'] == country_name]
    title = country_name
    return create_time_series(filtered_df, axis_type, title, 'CO2_per_capita')



if __name__ == '__main__':
    app.run_server(debug=True)
