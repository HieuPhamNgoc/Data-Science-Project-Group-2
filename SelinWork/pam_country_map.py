import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pycountry

#Preprocessing
data=pd.read_excel("SelinWork/PaM_number.xlsx")
df=data["Country"].value_counts()
df=df.reset_index()
df.rename(columns={"index":"Country",
                "Country":"Total"}
          ,inplace=True)
planned=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Status of implementation"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"status",
                "Status of implementation":"Number"}
          ,inplace=True)
    liste=df_coun_value["status"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Planned'):
            holder=i
            break
    if( holder != -1):
            planned.append(df_coun_value["Number"][holder])
    else:
            planned.append(0)
            
implemented=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Status of implementation"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"status",
                "Status of implementation":"Number"}
          ,inplace=True)
    liste=df_coun_value["status"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Implemented'):
            holder=i
            break
    if( holder != -1):
            implemented.append(df_coun_value["Number"][holder])
    else:
            implemented.append(0)

expired=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Status of implementation"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"status",
                "Status of implementation":"Number"}
          ,inplace=True)
    liste=df_coun_value["status"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Expired'):
            holder=i
            break
    if( holder != -1):
            expired.append(df_coun_value["Number"][holder])
    else:
            expired.append(0)
            
other=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Status of implementation"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"status",
                "Status of implementation":"Number"}
          ,inplace=True)
    liste=df_coun_value["status"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Other'):
            holder=i
            break
    if( holder != -1):
            other.append(df_coun_value["Number"][holder])
    else:
            other.append(0)
            
adopted=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Status of implementation"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"status",
                "Status of implementation":"Number"}
          ,inplace=True)
    liste=df_coun_value["status"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Adopted'):
            holder=i
            break
    if( holder != -1):
            adopted.append(df_coun_value["Number"][holder])
    else:
            adopted.append(0) 


df["Implemented"]=implemented
df["Planned"]=planned
df["Expired"]=expired
df["Adopted"]=adopted
df["Other"]=other


input_countries = df["Country"]
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]
df["code"]=codes

#-------------#
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H4('Number of Policies and measurements'),
    html.P("Select the status of policies and measurements:"),
    dcc.RadioItems(
        id='status', 
        options=["Total","Implemented", "Planned", "Adopted","Expired","Other"],
        value="Total",
        inline=True
    ),
    dcc.Graph(id="graph"),
])
@app.callback(
    Output("graph", "figure"), 
    Input("status", "value"))

def display_choropleth(status):
    df_use = df # replace with your own data source
    fig = px.choropleth(
        df_use, color=status,locations="code",
        projection="mercator", range_color=[0, 220],scope="europe", hover_name="Country",color_continuous_scale="Viridis")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)













