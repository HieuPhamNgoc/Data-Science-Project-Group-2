#install dash and dash_bootstrap_components

""""
pip install dash
pip install dash-bootstrap-components
"""

#Go to http://127.0.0.1:8050/ after running this.

from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

path = 'TeemusWork/data.xls'
data = pd.read_excel(io= path, sheet_name= "fossil_CO2_totals_by_country").T
data.columns = data.iloc[0]
data = data[1:]

app = Dash(__name__, prevent_initial_callbacks=False, external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div([
    html.H4("Country's CO2 emissions"),
    html.P("Select country:"),
    dcc.Dropdown(
        id='y-axis',
        options=list(data.columns.values),
        value='Afghanistan'
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("y-axis", "value"))
def display_area(y):
    df = data # replace with your own data source

    fig = px.area(
        df, x=df.index, y=y)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    