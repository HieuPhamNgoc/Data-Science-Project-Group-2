import pandas as pd
import dash
import openpyxl
import pycountry_convert as pc

from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import plotly.express as px

# Preprocessing data


### CO2 per capita
df_CO2_capita = pd.read_excel(io = 'LinhWork/co2_by_capita.xlsx')
df_CO2_capita = df_CO2_capita.drop(columns=['Substance', 'EDGAR Country Code'])
scope = list(df_CO2_capita["Country"].unique())
df_CO2_capita = pd.melt(df_CO2_capita, id_vars='Country', value_vars= df_CO2_capita.columns[1:],  var_name='Year', value_name='CO2_per_capita')
### GDP per capita
df_CO2_capita['Year'] = df_CO2_capita['Year'].astype("int")
df_CO2_capita['Country'] = df_CO2_capita['Country'].astype("string")


df_GDP_capita = pd.read_excel(io = 'LinhWork/GDP_per_capita.xlsx', skiprows = 3)
df_GDP_capita = df_GDP_capita.drop(columns= df_GDP_capita.columns[1:34])
df_GDP_capita = df_GDP_capita.rename(columns={"Country Name": "Country"})
df_GDP_capita = pd.melt(df_GDP_capita, id_vars='Country', value_vars= df_GDP_capita.columns[1:],  var_name='Year', value_name='GDP_per_capita')
df_GDP_capita['Year'] = df_GDP_capita['Year'].astype("int")
df_GDP_capita['Country'] = df_GDP_capita['Country'].astype("string")

df = pd.merge(df_CO2_capita, df_GDP_capita, on=["Country","Year"],how = 'inner')

### Group by country
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



df_nordics = df[df['Country'].isin(nordic_countries)]
df_nordics['Continent'] = 'Nordics'

df = pd.concat([df, df_nordics])

region = [{'label':c, 'value': c} for c in ['World', 'Asia', 'Africa', 'Europe', 'North America', 'Nordic', 'Oceania', 'South America']]

print(df.head(5))
### DASH
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='scatterplot-percapita'),
    dcc.Slider(
        1990,
        2021,
        step=1,
        value=1990,
        marks={int(i): '{}'.format(i) for i in range(1990,2022)},
        id='year-slider'
    )
])


@app.callback(
    Output('scatterplot-percapita', 'figure'),
    Input('year-slider', 'value'))


def update_figure(selected_year):
    filtered_df = df[df.Year == selected_year]

    fig = px.scatter(
        filtered_df,
         x="GDP_per_capita", 
         y="CO2_per_capita",
         size="CO2_per_capita", 
         color="Continent", 
         hover_name="Country",
        log_x=True,
        size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
