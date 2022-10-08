import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
#Not completed
#preprocessing the net-zero-target csv 
data = pd.read_csv("SelinWork/net-zero-targets.csv")
in_policy=len(data[data['Status of net-zero target'] == 'In policy document'])
pledge=len(data[data['Status of net-zero target'] == 'Pledge'])
achieved=len(data[data['Status of net-zero target'] == 'Achieved'])
in_law=len(data[data['Status of net-zero target'] == 'In law'])
# number of countries in the world is 195
no_net_zero=195- (len(data))
# create a new dataframe for the pie chart
percentages=[in_policy,pledge,achieved,in_law,no_net_zero]
variables=['In policy document', 'Pledge', 'Achieved', 'In law',"No data"]
data_percent={"Data":variables,"Numbers":percentages}
df_percent= pd.DataFrame(data_percent)
fig = px.pie(df_percent, values="Numbers", names="Data")
fig.show()

#------
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H4('Status of net-zero target'),
    html.P("Select the status of net-zero target :"),
    dcc.RadioItems(
        id='status', 
        options=["In policy1,],
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


