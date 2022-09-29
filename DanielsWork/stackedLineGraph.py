from re import T
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


# PREPROCESSING ETC

raw_data = pd.read_excel(io="DanielsWork\EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx", sheet_name="fossil_CO2_by_sector_and_countr")
raw_data.drop(columns=["Substance", "EDGAR Country Code"], inplace=True) # drop unnecessary columns
scope = [*set(raw_data["Country"])]; scope.append("Global emissions") # selectable countries + GLOBAL VIEW
raw_data.fillna(0, inplace=True) # replace unreported emissions with 0

app = Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1('CO2 emissions by sector', style = {'text-align':'center'}),
        html.Div(
            children = [
            html.H3('Select scope:'),
            dcc.Dropdown(id = 'scope',
                        options=scope,
                        multi=False,
                        value = 'Global emissions',
                        style={'width':'40%'})
            ],
            style={'width': '50%', 'margin-left': '50px'}
        ),
        html.Br(),
        dcc.Graph(id ='sector_emissions_graph', style = {'margin-left':'150px'}),
        html.Br()
    ]
)

@app.callback(
    Output("sector_emissions_graph", "figure"), 
    Input("scope", "value"))

def update_graph(selection):
    data = raw_data.copy()
    if selection == "Global emissions":
        data.drop(columns=["Country"], inplace=True) # not needed on global scope
        data = data.groupby("Sector", as_index=False).sum() # group by sector, aggregate by summing yearly emissions
        data.columns = data.columns.astype(str) # change names to string to ensure sound processing
        # we need the data from wide-form to long-form (see internet or plotly docs on why):
        data = pd.melt(data, id_vars = "Sector", value_vars=data.columns, var_name="Year", value_name = "CO2 emissions", ignore_index=True)
        fig = px.area(data, x="Year", y="CO2 emissions", color="Sector")
    else:
        data = data[data["Country"] == selection] # select country data
        data.drop(columns=["Country"], inplace=True)
        data.columns = data.columns.astype(str) # change names to string to ensure sound processing
        # we need the data from wide-form to long-form (see internet or plotly docs on why):
        data = pd.melt(data, id_vars = "Sector", value_vars=data.columns[1:], var_name="Year", value_name = "CO2 emissions", ignore_index=True)
        fig = px.area(data, x="Year", y="CO2 emissions", color="Sector")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)