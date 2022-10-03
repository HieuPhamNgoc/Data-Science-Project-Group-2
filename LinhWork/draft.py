import pandas as pd
import dash

from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import plotly.express as px


# Preprocessing data
df_co2 = pd.read_excel('co2_by_country.xlsx')
df_co2 = df_co2.drop(columns=['Substance', 'EDGAR Country Code'])
df_co2 = df_co2.drop(columns= df_co2.columns[1:21])
scope = list(df_co2["Country"].unique())

#df_co2 = df_co2.reset_index(drop=True).set_index('Country')
#df_co2 = pd.melt(df_co2, id_vars='Country', value_vars= df_co2.columns[1:],  var_name='Year', value_name='Change in CO2 emissions')

df = df_co2.copy()
df = pd.melt(df, id_vars='Country', value_vars= df.columns[1:],  var_name='Year', value_name='Change in CO2 emissions')
year = set(df.Year.unique())

# df_GDP = pd.read_excel('GDP_by_country_current_international_dollar.xlsx', skiprows = 3)
# df_GDP = df_GDP.drop(columns= df_GDP.columns[1:34])
# df_GDP = df_GDP.reset_index(drop=True).set_index('Country Name')
# df_GDP = df_GDP.pct_change(axis=1).fillna(0)


# df.iloc[:, 1:] = (df.iloc[:, 1:] - df.iloc[0, 1:].values.squeeze())
# .div(df.iloc[:, 1:])



app = Dash(__name__)


app.layout = html.Div(
    children = [
        html.H1('Changes in CO2 emissions', style = {'text-align':'center'}),
        html.Div(
            children = [
            html.H3('Select scope:'),
            dcc.Dropdown(id = "scope",
                        options=scope,
                        multi=False,
                        value = "Finland",
                        style={'width':'60%'})
            ],
            style={'width': '50%', 'margin-left': '50px'}
        ),
        html.Br(),
        dcc.Graph(id ='C02_change_emissions_graph', style = {'margin-left':'150px'}),
        html.Br(),
         html.Div(
            children = [
            html.H3('Select year:'),
            dcc.RangeSlider( 
                min = 1990, 
                max = 2021,  
                step = 1 ,
                value = [1990,1995],
                marks={int(i): '{}'.format(i) for i in range(1990,2022)},
                id='my-range-slider')
            ]
                )
            ], style={'width': '80%', 'margin-left': '50px'}
        )

@app.callback(
    Output('C02_change_emissions_graph', "figure"), 
    Input("scope", "value"),
    [Input('my-range-slider', 'value')],
    )



def update_graph(scope_selected, years_selected):
    data = df_co2.copy()
    data = data[data["Country"] == scope_selected]
    #data.iloc[:,1:] = data.iloc[:, 1:].pct_change(axis=1).fillna(0)
    data.columns = data.columns.astype(str) 
    data = pd.melt(data, id_vars='Country', value_vars= data.columns[1:],  var_name='Year', value_name='Change', ignore_index=True)
    data['Year'] = data['Year'].astype('int')
    data = data[(data["Year"] >= years_selected[0]) & (data["Year"] <= years_selected[1])]
    data.drop(columns=["Country"], inplace=True)
    #data['Change'] = data.iloc[1:,:].apply(lambda row: row)
    #data.iloc[1:,1] = ( data.iloc[1:,1] - data.iloc[0,1].values.squeeze())
    data.iloc[:,1] = data.iloc[:,1].apply(lambda row : (row - data.iloc[0,1]) /  data.iloc[0,1])
    fig = px.line(data, x= "Year", y="Change", template="none")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)