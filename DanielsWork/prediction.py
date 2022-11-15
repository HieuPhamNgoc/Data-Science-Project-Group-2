from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.tools as tls
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

co2_data = pd.read_excel(io="DanielsWork\EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx", sheet_name="fossil_CO2_totals_by_country")
co2_data = co2_data[co2_data["Country"] == "GLOBAL TOTAL"]
co2_data.drop(columns=["Country", "EDGAR Country Code", "Substance"], inplace=True)
co2_data.reset_index(drop=True, inplace=True)
co2_data["id"] = 0

co2_data = pd.melt(co2_data, id_vars="id", var_name="Year", value_name="Mt CO2")
co2_data.drop(columns=["id"], inplace=True)
co2_data.set_index("Year", inplace=True)

model = ARIMA(co2_data, order=(1,1,0))
result = model.fit()
pred = result.get_prediction(steps=5)
fig = px.line(pred)

app = Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1('CO2 emissions forecast', style = {'text-align':'center'}),
        html.Br(),
        dcc.Graph(id ='emissions_forecast', figure=fig, style = {'margin-left':'150px'}),
        html.Br()
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
