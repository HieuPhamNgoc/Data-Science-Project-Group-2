from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

raw_data = pd.read_excel(io="DanielsWork\EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx", sheet_name="fossil_CO2_by_sector_and_countr")
data = raw_data.drop(columns=["Substance", "EDGAR Country Code", "Country"]) # drop unnecessary columns
data.fillna(0, inplace=True) # replace unreported emissions with 0
data = data.groupby("Sector", as_index=False).sum() # group by sector, aggregate by summing yearly emissions
data.columns = data.columns.astype(str) # change names to string
data = pd.melt(data, id_vars = "Sector", value_vars=data.columns, var_name="Year", value_name = "CO_2 emissions", ignore_index=True)

app = Dash(__name__)

fig = px.area(data, x="Year", y="CO_2 emissions", color="Sector")

app.layout = html.Div(
    children = [
        html.H1('Global CO_2 emissions by sector', style = {'text-align':'center'}),
        html.Br(),
        dcc.Graph(id = 'sector_emissions_graph', figure = fig, style = {'margin-left':'150px'})
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)