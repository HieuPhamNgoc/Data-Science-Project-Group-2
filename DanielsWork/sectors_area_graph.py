from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


# PREPROCESSING ETC
sector_data = pd.read_excel(io="DanielsWork\EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx", sheet_name="fossil_CO2_by_sector_and_countr")
sector_data.drop(columns=["Substance"], inplace=True) # drop unnecessary columns
scope = sorted([*set(sector_data["Country"])]); scope.append("Global emissions") # selectable countries + GLOBAL VIEW

pop_data = pd.read_csv("DanielsWork\API_SP.POP.TOTL_DS2_en_csv_v2_4685015.csv", skiprows=4)

drop_years = [str(y) for y in range(1960,1970)] # more than necessary population data
drop_cols = drop_years + ["Indicator Name", "Indicator Code", "Unnamed: 66"] 
pop_data.drop(columns=drop_cols, inplace=True) # drop unnecessary cols

sector_data_per_capita = sector_data.copy() # we build the emissions/sector/capita into this

years = range(1970,2022)

for row in sector_data_per_capita.itertuples():
    country = row._2
    pop_ts = pop_data[pop_data["Country Code"] == country]
    if not pop_ts.empty:
        pop_ts.reset_index(drop=True,inplace=True)
        for year in years:
            pop = pop_ts.at[0,str(year)]
            co2 = sector_data_per_capita.at[row.Index, year]
            sector_data_per_capita.at[row.Index, year] = 10**6 * co2 / pop # convert from Mt => t

app = Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1('CO2 emissions per sector per capita', style = {'text-align':'center'}),
        html.Div(
            children = [
            html.H3('Select scope:'),
            dcc.Dropdown(id = 'scope',
                        options=scope,
                        multi=False,
                        value = 'Global emissions',
                        style={'width':'60%'})
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
    data = sector_data_per_capita.copy()
    if selection == "Global emissions":
        data.drop(columns=["Country"], inplace=True) # not needed on global scope
        data = data.groupby("Sector", as_index=False).sum() # group by sector, aggregate by summing yearly emissions
        data.columns = data.columns.astype(str) # change names to string to ensure sound processing
        # we need the data from wide-form to long-form (see internet or plotly docs on why):
        data = pd.melt(data, id_vars = "Sector", value_vars=data.columns, var_name="Year", value_name = "CO2 emissions [Tonnes/person]", ignore_index=True)
        fig = px.area(data, x="Year", y="CO2 emissions [Tonnes/person]", color="Sector", template="none")
    else:
        # dont know why this slightly bugs out. Python thinks selecting row based on column criteria
        # produces a series when it produces a dataframe. Works when running so no problem
        data = data[data["Country"] == selection] # select country data
        data.drop(columns=["Country"], inplace=True)
        data.columns = data.columns.astype(str) # change names to string to ensure sound processing
        # we need the data from wide-form to long-form (see internet or plotly docs on why):
        data = pd.melt(data, id_vars = "Sector", value_vars=data.columns[1:], var_name="Year", value_name = "CO2 emissions [Tonnes/person]", ignore_index=True)
        fig = px.area(data, x="Year", y="CO2 emissions [Tonnes/person]", color="Sector", template="none")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)