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

app = dash.Dash(__name__)


app.layout = html.Div([
    html.H4('Status of Net-Zero Target'),
    dcc.Graph(id="graph"),
    html.P("Names:"),
    dcc.Dropdown(id='names',
        options=['smoker', 'day', 'time', 'sex'],
        value='day', clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(id='values',
        options=['total_bill', 'tip', 'size'],
        value='total_bill', clearable=False
    ),
])


@app.callback(
    Output("graph", "figure"), 
    Input("names", "value"), 
    Input("values", "value"))
def generate_chart(names, values):
    df = px.data.tips() # replace with your own data source
    fig = px.pie(df, values=values, names=names, hole=.3)
    return fig


app.run_server(debug=True)