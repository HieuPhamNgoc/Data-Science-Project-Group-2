from dash import Dash, html, dcc, Input, Output
import plotly.express as px
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

#print(co2_data)

model = ARIMA(co2_data, order=(1,1,0))
result = model.fit()
fig = px.line(result.fittedvalues)

fig.show()