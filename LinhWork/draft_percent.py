import pandas as pd
import dash
import openpyxl

from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import plotly.express as px

# Preprocessing data
df_co2 = pd.read_excel( io = "LinhWork/co2_by_country.xlsx")
df_co2 = df_co2.drop(columns=['Substance', 'EDGAR Country Code'])
df_co2 = df_co2.drop(columns= df_co2.columns[1:21])
scope = list(df_co2["Country"].unique())

df = df_co2.copy()
df = pd.melt(df, id_vars='Country', value_vars= df.columns[1:],  var_name='Year', value_name='Change in CO2 emissions')
year = set(df.Year.unique())

df_GDP = pd.read_excel(io = 'LinhWork/GDP_by_country_current_international_dollar.xlsx', skiprows = 3)
df_GDP = df_GDP.drop(columns= df_GDP.columns[1:34])


df_CO2_capita = pd.read_excel(io = 'LinhWork/co2_by_capita.xlsx')
df_CO2_capita = df_CO2_capita.drop(columns=['Substance', 'EDGAR Country Code'])

df_GDP_capita = pd.read_excel(io  = 'LinhWork/GDP_per_capita.xlsx', skiprows = 3)
df_GDP_capita = df_GDP_capita.drop(columns= df_GDP_capita.columns[1:34])


# df.iloc[:, 1:] = (df.iloc[:, 1:] - df.iloc[0, 1:].values.squeeze())
# .div(df.iloc[:, 1:])



app = Dash(__name__)


app.layout = html.Div(
    children = [
        html.H1('Changes in CO2 emissions per capita and GDP per capita from 1990-2021', style = {'text-align':'center'}),
        html.Div(
            children = [
            html.H3('Select scope:'),
            dcc.Dropdown(id = "scope1",
                        options=scope,
                        multi=False,
                        value = "Finland",
                        style={'width':'60%'}),

                        
            ],

            style={'width': '50%', 'margin-left': '50px'}
        ),
        html.Div(
            children = [
            html.H3('Select year:'),
            dcc.RangeSlider( 
                min = 1990, 
                max = 2021,  
                step = 1 ,
                value = [2000, 2021],
                marks={int(i): '{}'.format(i) for i in range(1990,2022)},
                id='my-range-slider')
            ], style={'width': '100%', 'margin-left': '50px'}
        ),
        html.Br(),
        dcc.Graph(id ='C02_change_emissions_graph', style = {'margin-left':'150px'}),
        html.Br(),
            ],
             style={'width': '80%', 'margin-left': '100px'}
        )

@app.callback(
    Output('C02_change_emissions_graph', "figure"), 
    Input("scope1", "value"),
    [Input('my-range-slider', 'value')],
    )



def update_graph(scope_selected, years_selected):
    data = df_co2.copy()
    data1 = df_GDP.copy()
    data2 = df_GDP_capita.copy()
    data3 = df_CO2_capita.copy()

    ### Data for CO2
    data = data[data["Country"] == scope_selected]
    data.columns = data.columns.astype(str) 
    data = pd.melt(data, id_vars='Country', value_vars= data.columns[1:],  var_name='Year', value_name='Change', ignore_index=True)
    data['Year'] = data['Year'].astype('int')
    data = data[(data["Year"] >= years_selected[0]) & (data["Year"] <= years_selected[1])]
    data.drop(columns=["Country"], inplace=True)
    data.iloc[:,1] = data.iloc[:,1].apply(lambda row : (((row - data.iloc[0,1]) /  data.iloc[0,1]) ))
    data["Metric"] = "CO2"

    ###  Data for GDP
    data1 = data1[data1["Country Name"] == scope_selected]
    data1.columns = data1.columns.astype(str)
    data1 = pd.melt(data1, id_vars='Country Name', value_vars= data1.columns[1:],  var_name='Year', value_name='Change', ignore_index=True)
    data1['Year'] = data1['Year'].astype('int')
    data1 = data1[(data1["Year"] >= years_selected[0]) & (data1["Year"] <= years_selected[1])]
    data1.drop(columns=["Country Name"], inplace=True)
    data1.iloc[:,1] = data1.iloc[:,1].apply(lambda row : (((row - data1.iloc[0,1]) /  data1.iloc[0,1]) ))
    data1["Metric"] = "GDP"
    
    ### Data for GDP per capita
    data2 = data2[data2["Country Name"] == scope_selected]
    data2.columns = data2.columns.astype(str)
    data2 = pd.melt(data2, id_vars='Country Name', value_vars= data2.columns[1:],  var_name='Year', value_name='Change', ignore_index=True)
    data2['Year'] = data2['Year'].astype('int')
    data2 = data2[(data2["Year"] >= years_selected[0]) & (data2["Year"] <= years_selected[1])]
    data2.drop(columns=["Country Name"], inplace=True)
    data2.iloc[:,1] = data2.iloc[:,1].apply(lambda row : (((row - data2.iloc[0,1]) /  data2.iloc[0,1]) ))
    data2["Metric"] = "GDP_per_capita"

    ### Data for CO2 per capita
    data3 = data3[data3["Country"] == scope_selected]
    data3.columns = data3.columns.astype(str) 
    data3 = pd.melt(data3, id_vars='Country', value_vars= data3.columns[1:],  var_name='Year', value_name='Change', ignore_index=True)
    data3['Year'] = data3['Year'].astype('int')
    data3 = data3[(data3["Year"] >= years_selected[0]) & (data3["Year"] <= years_selected[1])]
    data3.drop(columns=["Country"], inplace=True)
    data3.iloc[:,1] = data3.iloc[:,1].apply(lambda row : (((row - data3.iloc[0,1]) /  data3.iloc[0,1]) ))
    data3["Metric"] = "CO2_per_capita"



    ### Update graph

    #df  = pd.concat([data,data1.loc[:]]).reset_index(drop=True)
    df  = pd.concat([data2,data3.loc[:]]).reset_index(drop=True)
    fig = px.line(df, x= "Year", y="Change", color="Metric", template="none")
    fig.layout.yaxis.tickformat = ',.1%'

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)