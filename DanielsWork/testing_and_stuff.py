import pandas as pd

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

global_sector_per_capita = sector_data.copy()
global_sector_per_capita.drop(columns=["Country", "EDGAR Country Code"], inplace=True) # not needed on global scope
global_sector_per_capita = global_sector_per_capita.groupby("Sector", as_index=False).sum() # group by sector, aggregate by summing yearly emissions
global_sector_per_capita.columns = global_sector_per_capita.columns.astype(str) # change names to string to ensure sound processing

years = range(1970,2022)

for row in global_sector_per_capita.itertuples():
    for year in years:
        pop = pop_totals[str(year)]
        co2 = global_sector_per_capita.at[row.Index, str(year)]
        global_sector_per_capita.at[row.Index, str(year)] = 10**6 * co2 / pop # convert from Mt => t

print(global_sector_per_capita)

for row in sector_per_capita.itertuples():
    country = row._2
    pop_ts = pop_data[pop_data["Country Code"] == country]
    if not pop_ts.empty:
        pop_ts.reset_index(drop=True,inplace=True)
        for year in years:
            pop = pop_ts.at[0,str(year)]
            co2 = sector_per_capita.at[row.Index, year]
            sector_per_capita.at[row.Index, year] = 10**6 * co2 / pop # convert from Mt => t
