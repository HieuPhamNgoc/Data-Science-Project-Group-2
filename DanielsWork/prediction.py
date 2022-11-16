from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

co2_data = pd.read_excel(io="DanielsWork\EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx", sheet_name="fossil_CO2_totals_by_country")
co2_data = co2_data[co2_data["Country"] == "GLOBAL TOTAL"]
co2_data.drop(columns=["Country", "EDGAR Country Code", "Substance"], inplace=True)
co2_data.reset_index(drop=True, inplace=True)
co2_data["id"] = 0

co2_data = pd.melt(co2_data, id_vars="id", var_name="Year", value_name="Realized CO2 [Mt/year]")
co2_data.drop(columns=["id"], inplace=True)
co2_data.set_index("Year", inplace=True)

# super simple once-differenced AR model (with drift i.e., constant term c)
model = ARIMA(co2_data, order=(1,1,0), trend="t")
result = model.fit()
# predict 5 years out
mat_pred = result.get_prediction(start=1, end=56)
# default plots by statsmodels in matplotlib WHICH DONT FUCKING WORK WITH DASH!!!
pred_df = mat_pred.summary_frame()
pred_df.drop(columns=["mean_se"], inplace=True)
pred_df.columns = ["Predicted CO2 [Mt/year]", "Lower CI (95%)", "Higher CI (95%)"]
pred_df.loc[-1] = [None, None, None]
pred_df.index = pred_df.index + 1
pred_df = pred_df.sort_index()
pred_df["Year"] = [year for year in range(1970,2027)]
pred_df.set_index("Year", inplace=True)
# hardcode future years into og timeseries
co2_data.loc[2022] = [None]
co2_data.loc[2023] = [None]
co2_data.loc[2024] = [None]
co2_data.loc[2025] = [None]
co2_data.loc[2026] = [None]

shitos = pd.concat([co2_data, pred_df], axis=1)

#print(shitos)

prediction_plot = go.Figure([
    go.Scatter(
        name="Predicted",
        x=shitos.index,
        y=shitos["Predicted CO2 [Mt/year]"],
        mode="lines",
        line=dict(color="rgb(31,119,180)")
    ),
    go.Scatter(
        name="Upper CI",
        x=shitos.index,
        y=shitos["Higher CI (95%)"],
        mode="lines",
        marker=dict(color="#444"),
        line=dict(width=0)
    ),
    go.Scatter(
        name="Lower CI",
        x=shitos.index,
        y=shitos["Lower CI (95%)"],
        mode="lines",
        marker=dict(color="#444"),
        line=dict(width=0,),
        fillcolor="rgba(68,68,68,0.3)",
        fill="tonexty"
    ),
    go.Scatter(
        name="Realized",
        x=shitos.index,
        y=shitos["Realized CO2 [Mt/year]"],
        mode="lines",
        line=dict(color="rgb(250,150,20)")
    )
])

prediction_plot.update_layout(
    xaxis_title="Year",
    yaxis_title="CO2 emissions [Mt CO2/year]",
    hovermode="x",
    template="none"
)

app = Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1('CO2 emissions 5 year forecast', style = {'text-align':'center'}),
        html.Br(),
        dcc.Graph(id ='emissions_forecast', figure=prediction_plot, style = {'margin-left':'150px'}),
        html.Br()
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
