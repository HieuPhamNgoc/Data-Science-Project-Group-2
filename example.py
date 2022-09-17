#install dash and dash_bootstrap_components

""""
pip install dash
pip install dash-bootstrap-components
"""

#Go to http://127.0.0.1:8050/ after running this.

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(__name__, prevent_initial_callbacks=False, external_stylesheets=[dbc.themes.LUX])

#Start of the web app configuration and layout
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [40, 11, 22, 24, 45, 65],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Simple Example'),

    html.Div(children='''
        Some graph to for the sake of it
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)