
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

