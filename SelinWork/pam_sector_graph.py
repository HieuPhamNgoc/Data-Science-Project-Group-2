
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pycountry

# NOT COMPLETED 
#Preprocessing
data=pd.read_excel("PaM_number.xlsx")
data =data.rename(columns={"Objective(s)_lookup_only4facets":"Sector"})

for i in range(len(data)):
    sector_name=data["Sector"][i]
    if(isinstance(sector_name, str)):
        if(sector_name.split()[0]=="Energy" or sector_name.split()[0]=="Energy:"):
            data["Sector"][i] ="Energy"
        elif(sector_name.split()[0]=="Agriculture" or sector_name.split()[0]=="Agriculture:" or sector_name.split()[0]=="Land" or sector_name.split()[0]=="Land:"):
            data["Sector"][i] ="Agriculture & Land"
        elif(sector_name.split()[0]=="Waste" or sector_name.split()[0]=="Waste:"):
            data["Sector"][i] ="Waste"
        elif(sector_name.split()[0]=="Transport" or sector_name.split()[0]=="Transport:"):
            data["Sector"][i] ="Transportation"
        elif(sector_name.split()[0]=="Industrial" or sector_name.split()[0]=="Industrial:"):
            data["Sector"][i] ="Industry"
        elif(sector_name.split()[0]=="Other"):
            data["Sector"][i] ="Other"
    else:
         data["Sector"][i] ="Other"

df=data["Country"].value_counts()
df=df.reset_index()
df.rename(columns={"index":"Country",
                "Country":"Total"}
          ,inplace=True)

input_countries = df["Country"]
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]

df["code"]=codes

energy=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Sector"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"sector",
                "Sector":"Number"}
          ,inplace=True)
    liste=df_coun_value["sector"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Energy'):
            holder=i
            break
    if( holder != -1):
            energy.append(df_coun_value["Number"][holder])
    else:
            energy.append(0)
            
agri_land=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Sector"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"sector",
                "Sector":"Number"}
          ,inplace=True)
    liste=df_coun_value["sector"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == "Agriculture & Land"):
            holder=i
            break
    if( holder != -1):
            agri_land.append(df_coun_value["Number"][holder])
    else:
            agri_land.append(0)

waste=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Sector"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"sector",
                "Sector":"Number"}
          ,inplace=True)
    liste=df_coun_value["sector"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Waste'):
            holder=i
            break
    if( holder != -1):
            waste.append(df_coun_value["Number"][holder])
    else:
            waste.append(0)
            
other=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Sector"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"sector",
                "Sector":"Number"}
          ,inplace=True)
    liste=df_coun_value["sector"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Other'):
            holder=i
            break
    if( holder != -1):
            other.append(df_coun_value["Number"][holder])
    else:
            other.append(0)
            
transport=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Sector"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"sector",
                "Sector":"Number"}
          ,inplace=True)
    liste=df_coun_value["sector"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Transportation'):
            holder=i
            break
    if( holder != -1):
            transport.append(df_coun_value["Number"][holder])
    else:
           transport.append(0)  
indust=[]
for i in range(len(df)):
    country_name=df["Country"][i]
    df_coun=data[data["Country"]==country_name]
    df_coun_value=df_coun["Sector"].value_counts()
    df_coun_value=df_coun_value.reset_index()
    df_coun_value.rename(columns={"index":"sector",
                "Sector":"Number"}
          ,inplace=True)
    liste=df_coun_value["sector"].unique()
    holder= -1
    for i in range(len(liste)):
        if (liste[i] == 'Industry'):
            holder=i
            break
    if( holder != -1):
            indust.append(df_coun_value["Number"][holder])
    else:
           indust.append(0)  
           
df["Energy"]=energy
df["Waste"]=waste
df["Agriculture & Land"] = agri_land
df["Industry"]=indust
df["Transportation"]=transport
df["Other"]=other

#---------------#
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H4('Number of Policies and measurements by Sector'),
    html.P("Select the Sector"),
    dcc.Dropdown(id = 'sector',
                        options=["Total","Energy", "Waste", "Trasportation","Industry","Agriculture & Land","Other"],
                        multi=False,
                        value = 'Total',
                        style={'width':'60%'}),       
    dcc.Graph(id="graph")
])
@app.callback(
    Output("graph", "figure"), 
    Input("sector", "value"))

def display_choropleth(sector):
    df_use = df # replace with your own data source
    fig = px.choropleth(
        df_use, color=sector,locations="code",
        projection="mercator", range_color=[0, 220],scope="europe", hover_name="Country",colorscale = 'Reds')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)













