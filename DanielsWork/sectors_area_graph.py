from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


# PREPROCESSING ETC => Rather not do this every update so perform here
sector_data = pd.read_excel(io="DanielsWork\EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx", sheet_name="fossil_CO2_by_sector_and_countr")
sector_data.drop(columns=["Substance"], inplace=True) # drop unnecessary columns
scope = sorted([*set(sector_data["Country"])]); scope.append("Global emissions") # selectable countries + GLOBAL VIEW

pop_data = pd.read_csv("DanielsWork\API_SP.POP.TOTL_DS2_en_csv_v2_4685015.csv", skiprows=4)

drop_years = [str(y) for y in range(1960,1970)] # more than necessary population data
drop_cols = drop_years + ["Country Name", "Indicator Name", "Indicator Code", "Unnamed: 66"] 
pop_data.drop(columns=drop_cols, inplace=True) # drop unnecessary cols

# computing total populations per year (from our underlying data rather than external source to
# maintain consistancy with ratios)
pop_totals = pop_data.copy()
pop_totals = pop_totals[pop_totals["Country Code"].isin([*set(sector_data["EDGAR Country Code"])])]
pop_totals.drop(columns=["Country Code"], inplace=True)
pop_totals = pop_totals.sum() # series of total populations per year

sector_per_capita = sector_data.copy() # we build the emissions/sector/capita into this

# The global scope
global_sector_per_capita = sector_data.copy()
global_sector_per_capita.drop(columns=["Country", "EDGAR Country Code"], inplace=True) # not needed on global scope
global_sector_per_capita = global_sector_per_capita.groupby("Sector", as_index=False).sum() # group by sector, aggregate by summing yearly emissions
global_sector_per_capita.columns = global_sector_per_capita.columns.astype(str) # change names to string to ensure sound processing

years = range(1970,2022)

# dividing the earlier aggregated total co2 by population
for row in global_sector_per_capita.itertuples():
    for year in years:
        pop = pop_totals[str(year)]
        co2 = global_sector_per_capita.at[row.Index, str(year)]
        global_sector_per_capita.at[row.Index, str(year)] = 10**6 * co2 / pop # convert from Mt => t

# same as above but country specific
for row in sector_per_capita.itertuples():
    country = row._2
    pop_ts = pop_data[pop_data["Country Code"] == country]
    if not pop_ts.empty:
        pop_ts.reset_index(drop=True,inplace=True)
        for year in years:
            pop = pop_ts.at[0,str(year)]
            co2 = sector_per_capita.at[row.Index, year]
            sector_per_capita.at[row.Index, year] = 10**6 * co2 / pop # convert from Mt => t

app = Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1('CO2 emissions per sector', style = {'text-align':'center'}),
        html.Div(
            children = [
            html.H3('Select scope:'),
            dcc.Dropdown(id = 'scope',
                        options=scope,
                        multi=False,
                        value = 'Global emissions',
                        style={'width':'60%'}),
            html.Br(),
            dcc.RadioItems(id = 'scale',
                          options=["Total CO2", "CO2 / capita"],
                          value="CO2 / capita")
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
    Input("scope", "value"),
    Input("scale", "value"))

def update_graph(select, scale):
    if scale == "CO2 / capita":
        if select == "Global emissions":
            data = global_sector_per_capita.copy()
            # we need the data from wide-form to long-form (see internet or plotly docs on why):
            data = pd.melt(data, id_vars = "Sector", value_vars=data.columns, var_name="Year", value_name = "CO2 emissions [Tonnes/person]", ignore_index=True)
            fig = px.area(data, x="Year", y="CO2 emissions [Tonnes/person]", color="Sector", template="none")
        else:
            # dont know why this slightly bugs out. Python thinks selecting row based on column criteria
            # produces a series when it produces a dataframe. Works when running so no problem
            data = sector_per_capita.copy()
            data = data[data["Country"] == select] # select country data
            data.drop(columns=["Country"], inplace=True)
            data.columns = data.columns.astype(str) # change names to string to ensure sound processing
            # we need the data from wide-form to long-form (see internet or plotly docs on why):
            data = pd.melt(data, id_vars = "Sector", value_vars=data.columns[1:], var_name="Year", value_name = "CO2 emissions [Tonnes/person]", ignore_index=True)
            fig = px.area(data, x="Year", y="CO2 emissions [Tonnes/person]", color="Sector", template="none")
        return fig
    else:
        if select == "Global emissions":
            data = sector_data.copy()
            data.drop(columns=["Country", "EDGAR Country Code"], inplace=True) # not needed on global scope
            data = data.groupby("Sector", as_index=False).sum() # group by sector, aggregate by summing yearly emissions
            data.columns = data.columns.astype(str)
            # we need the data from wide-form to long-form (see internet or plotly docs on why):
            data = pd.melt(data, id_vars = "Sector", value_vars=data.columns, var_name="Year", value_name = "CO2 emissions [Megatonnes]", ignore_index=True)
            fig = px.area(data, x="Year", y="CO2 emissions [Megatonnes]", color="Sector", template="none")
        else:
            # dont know why this slightly bugs out. Python thinks selecting row based on column criteria
            # produces a series when it produces a dataframe. Works when running so no problem
            data = sector_data.copy()
            data = data[data["Country"] == select] # select country data
            data.drop(columns=["Country", "EDGAR Country Code"], inplace=True)
            data.columns = data.columns.astype(str) # change names to string to ensure sound processing
            # we need the data from wide-form to long-form (see internet or plotly docs on why):
            data = pd.melt(data, id_vars = "Sector", value_vars=data.columns[1:], var_name="Year", value_name = "CO2 emissions [Megatonnes]", ignore_index=True)
            fig = px.area(data, x="Year", y="CO2 emissions [Megatonnes]", color="Sector", template="none")
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)