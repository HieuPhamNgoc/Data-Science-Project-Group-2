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

# super simple AR model (once differenced)
model = ARIMA(co2_data, order=(1,1,0))
result = model.fit()
# predict 5 years out
mat_pred = result.get_prediction(start=1, end=56)
# default plots by statsmodels in matplotlib WHICH DONT FUCKING WORK WITH DASH!!!
pred_df = mat_pred.summary_frame()
pred_df.drop(columns=["mean_se"], inplace=True)
pred_df.columns = ["Prediction", "Lower CI (95%)", "Higher CI (95%)"]
#pred_df.insert(0, {"Prediction": None, "Lower CI (95%)": None, "Higher CI (95%)": None})
pred_df["Year"] = [year for year in range(1971,2027)]
pred_df.set_index("Year", inplace=True)
#pred_df.insert(1970, {"Prediction": None, "Lower CI (95%)": None, "Higher CI (95%)": None})
print(pred_df)
print(co2_data)
'''
plot_pred = fig_to_plotly(mat_pred)
fig = px.line(plot_pred)


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
'''