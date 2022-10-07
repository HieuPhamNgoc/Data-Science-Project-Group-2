import dash
from dash import html, dcc, Input, Output, callback

import plotly.express as px
import numpy as np
import pandas as pd

dash.register_page(__name__, path="/graphs")
path = "~/git/Data-Science-Project-Group-2/HieuWork/EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx"
# Daniel graph
raw_data = pd.read_excel(
    io=path,
    sheet_name="fossil_CO2_by_sector_and_countr",
)
raw_data.drop(
    columns=["Substance", "EDGAR Country Code"], inplace=True
)  # drop unnecessary columns
daniel_scope = sorted([*set(raw_data["Country"])])
daniel_scope.append("Global emissions")  # selectable countries + GLOBAL VIEW
raw_data.fillna(0, inplace=True)  # replace unreported emissions with 0

#  Hieu graph

df_CO2_country = pd.read_excel(io=path, sheet_name="fossil_CO2_totals_by_country")

nordic_countries = [
    "Denmark",
    "Finland",
    "Iceland",
    "Norway",
    "Sweden",
    "Greenland",
    "Faroes",
]

# Convert country name into continent name


def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(
            country_continent_code
        )
    except:
        return "Unspecified"
    return country_continent_name


df_CO2_country["Continent"] = df_CO2_country["Country"].apply(
    lambda x: country_to_continent(x)
)

region = [
    {"label": c, "value": c}
    for c in [
        "World",
        "Asia",
        "Africa",
        "Europe",
        "North America",
        "Nordic",
        "Oceania",
        "South America",
    ]
]

year = [{"label": str(c), "value": c} for c in df_CO2_country.columns[3:]]

# Linh graph
df_co2 = pd.read_excel(
    "~/git/Data-Science-Project-Group-2/LinhWork/co2_by_country.xlsx"
)
df_co2 = df_co2.drop(columns=["Substance", "EDGAR Country Code"])
df_co2 = df_co2.drop(columns=df_co2.columns[1:21])
scope = list(df_co2["Country"].unique())

df = df_co2.copy()
df = pd.melt(
    df,
    id_vars="Country",
    value_vars=df.columns[1:],
    var_name="Year",
    value_name="Change in CO2 emissions",
)
year = set(df.Year.unique())

df_GDP = pd.read_excel(
    "~/git/Data-Science-Project-Group-2/LinhWork/GDP_by_country_current_international_dollar.xlsx",
    skiprows=3,
)
df_GDP = df_GDP.drop(columns=df_GDP.columns[1:34])

layout = html.Div(
    children=[
        html.Div(
            children="""
        This is our Home page content.
    """
        ),
        html.Div(
            [
                "How many friends do you have: ",
                dcc.Input(id="my-input", value="", type="number"),
            ]
        ),
        html.Div(
            [
                "What you can do:",
                dcc.Checklist(
                    [
                        "Walk/cycle to work",
                        "Use better energy home appliance",
                        "Cook more at home to reduce food waste",
                    ],
                    [],
                    id="activities",
                ),
            ]
        ),
        html.Br(),
        html.Div(id="my-output"),
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            "CO2 emissions by sector", style={"text-align": "center"}
                        ),
                        html.Div(
                            children=[
                                html.H3("Select scope:"),
                                dcc.Dropdown(
                                    id="daniel_scope",
                                    options=daniel_scope,
                                    multi=False,
                                    value="Global emissions",
                                    style={"width": "60%"},
                                ),
                            ],
                            style={"width": "50%", "margin-left": "50px"},
                        ),
                        html.Br(),
                        dcc.Graph(
                            id="sector_emissions_graph", style={"margin-left": "150px"}
                        ),
                        html.Br(),
                    ],
                    style={"order": 2, "margin": "50px"},
                ),
                html.Div(
                    [
                        html.H1(
                            "Worldwide CO2 emission", style={"text-align": "center"}
                        ),
                        html.Div(
                            children=[
                                html.H3("Choose a region:"),
                                dcc.Dropdown(
                                    id="region",
                                    options=region,
                                    multi=False,
                                    value="World",
                                    style={"width": "40%"},
                                ),
                            ],
                            style={"width": "50%", "margin-left": "50px"},
                        ),
                        html.Br(),
                        dcc.Graph(
                            id="co2_graph", figure={}, style={"margin-left": "150px"}
                        ),
                        html.Br(),
                        html.Div(
                            children=[
                                dcc.Slider(
                                    min=1970,
                                    max=2021,
                                    step=1,
                                    value=2021,
                                    marks=None,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": False,
                                    },
                                    id="year_slider",
                                )
                            ],
                            style={"width": "50%", "margin-left": "480px"},
                        ),
                        html.Div(
                            id="output_container",
                            children=[],
                            style={"text-align": "center", "font-size": "25px"},
                        ),
                    ],
                    style={"order": 1, "margin": "50px"},
                ),
                html.Div(
                    [
                        html.H1(
                            "Changes in CO2 emissions and GDP",
                            style={"text-align": "center"},
                        ),
                        html.Div(
                            children=[
                                html.H3("Select scope:"),
                                dcc.Dropdown(
                                    id="scope",
                                    options=scope,
                                    multi=False,
                                    value="Finland",
                                    style={"width": "60%"},
                                ),
                            ],
                            style={"width": "50%", "margin-left": "50px"},
                        ),
                        html.Br(),
                        dcc.Graph(
                            id="C02_change_emissions_graph",
                            style={"margin-left": "150px"},
                        ),
                        html.Br(),
                        html.Div(
                            children=[
                                html.H3("Select year:"),
                                dcc.RangeSlider(
                                    min=1990,
                                    max=2021,
                                    step=1,
                                    value=[2000, 2021],
                                    marks={
                                        int(i): "{}".format(i)
                                        for i in range(1990, 2022)
                                    },
                                    id="my-range-slider",
                                ),
                            ]
                        ),
                    ], style={'order':3, 'margin':'50px'}
                ),
            ],
            style={"display": "flex", "flex-direction": "column"},
        ),
    ],
)


@callback(
    Output(component_id="my-output", component_property="children"),
    Input(component_id="my-input", component_property="value"),
    Input("activities", "value"),
    prevent_initial_call=True,
)
def update_output_div(input_value, activities):
    if len(activities) == 0 or input_value is None:
        ans = 0
        return ""
    else:
        ans = input_value * len(activities)
        return html.H1(
            "You can reduce {} tons carbon emission by 2050".format(ans),
            style={"margin-left": "35%", "margin-right": "30%", "color": "red"},
        )


@callback(Output("sector_emissions_graph", "figure"), Input("daniel_scope", "value"))
def update_graph(selection):
    data = raw_data.copy()
    if selection == "Global emissions":
        data.drop(columns=["Country"], inplace=True)  # not needed on global scope
        data = data.groupby(
            "Sector", as_index=False
        ).sum()  # group by sector, aggregate by summing yearly emissions
        data.columns = data.columns.astype(
            str
        )  # change names to string to ensure sound processing
        # we need the data from wide-form to long-form (see internet or plotly docs on why):
        data = pd.melt(
            data,
            id_vars="Sector",
            value_vars=data.columns,
            var_name="Year",
            value_name="CO2 emissions",
            ignore_index=True,
        )
        fig = px.area(
            data, x="Year", y="CO2 emissions", color="Sector", template="none"
        )
    else:
        # dont know why this slightly bugs out. Python thinks selecting row based on column criteria
        # produces a series when it produces a dataframe. Works when running so no problem
        data = data[data["Country"] == selection]  # select country data
        data.drop(columns=["Country"], inplace=True)
        data.columns = data.columns.astype(
            str
        )  # change names to string to ensure sound processing
        # we need the data from wide-form to long-form (see internet or plotly docs on why):
        data = pd.melt(
            data,
            id_vars="Sector",
            value_vars=data.columns[1:],
            var_name="Year",
            value_name="CO2 emissions",
            ignore_index=True,
        )
        fig = px.area(
            data, x="Year", y="CO2 emissions", color="Sector", template="none"
        )
    return fig


@callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="co2_graph", component_property="figure"),
    ],
    [
        Input(component_id="region", component_property="value"),
        Input(component_id="year_slider", component_property="value"),
    ],
)
def update_graph(
    region_slctd, year_slctd
):  # number of arguments is the same as the number of inputs

    container = " CO2 emission in {}".format(year_slctd)

    if region_slctd == "World":
        df_CO2 = df_CO2_country.copy()

    elif region_slctd == "Nordic":
        df_CO2 = df_CO2_country[df_CO2_country["Country"].isin(nordic_countries)]

    else:
        df_CO2 = df_CO2_country[df_CO2_country["Continent"] == region_slctd]

    df_CO2 = df_CO2[["Country", year_slctd]]
    df_CO2[year_slctd] = np.round(df_CO2[year_slctd], 3)

    fig = px.choropleth(
        data_frame=df_CO2,
        locationmode="country names",
        locations="Country",
        color=year_slctd,
        range_color=[0, 6000],
        color_continuous_scale=px.colors.sequential.Aggrnyl,
        hover_data={"Country": False},
        labels={str(year_slctd): "CO2 emission"},
        hover_name="Country",
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )  # template in ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
    return container, fig


@callback(
    Output("C02_change_emissions_graph", "figure"),
    Input("scope", "value"),
    [Input("my-range-slider", "value")],
)
def update_graph(scope_selected, years_selected):
    data = df_co2.copy()
    data1 = df_GDP.copy()
    ###
    data = data[data["Country"] == scope_selected]
    data.columns = data.columns.astype(str)
    data = pd.melt(
        data,
        id_vars="Country",
        value_vars=data.columns[1:],
        var_name="Year",
        value_name="Change",
        ignore_index=True,
    )
    data["Year"] = data["Year"].astype("int")
    data = data[
        (data["Year"] >= years_selected[0]) & (data["Year"] <= years_selected[1])
    ]
    data.drop(columns=["Country"], inplace=True)
    data.iloc[:, 1] = data.iloc[:, 1].apply(
        lambda row: (((row - data.iloc[0, 1]) / data.iloc[0, 1]))
    )
    data["Metric"] = "CO2"

    ###
    data1 = data1[data1["Country Name"] == scope_selected]
    data1.columns = data1.columns.astype(str)
    data1 = pd.melt(
        data1,
        id_vars="Country Name",
        value_vars=data1.columns[1:],
        var_name="Year",
        value_name="Change",
        ignore_index=True,
    )
    data1["Year"] = data1["Year"].astype("int")
    data1 = data1[
        (data1["Year"] >= years_selected[0]) & (data1["Year"] <= years_selected[1])
    ]
    data1.drop(columns=["Country Name"], inplace=True)
    data1.iloc[:, 1] = data1.iloc[:, 1].apply(
        lambda row: (((row - data1.iloc[0, 1]) / data1.iloc[0, 1]))
    )
    data1["Metric"] = "GDP"

    df = pd.concat([data, data1.loc[:]]).reset_index(drop=True)
    fig = px.line(df, x="Year", y="Change", color="Metric", template="none")
    fig.layout.yaxis.tickformat = ",.1%"

    return fig
