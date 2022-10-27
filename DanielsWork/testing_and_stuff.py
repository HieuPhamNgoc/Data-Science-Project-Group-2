import pandas as pd

sector_data = pd.read_excel(io="DanielsWork\EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx", sheet_name="fossil_CO2_by_sector_and_countr")
sector_data.drop(columns=["Substance"], inplace=True) # drop unnecessary columns
scope = sorted([*set(sector_data["Country"])]); scope.append("Global emissions") # selectable countries + GLOBAL VIEW

pop_data = pd.read_csv("DanielsWork\API_SP.POP.TOTL_DS2_en_csv_v2_4685015.csv", skiprows=4)

drop_years = [str(y) for y in range(1960,1970)] # more than necessary population data
drop_cols = drop_years + ["Indicator Name", "Indicator Code", "Unnamed: 66"] 
pop_data.drop(columns=drop_cols, inplace=True) # drop unnecessary cols

sector_per_capita = sector_data.copy() # we build the emissions/sector/capita into this

years = range(1970,2022)

for row in sector_per_capita.itertuples():
    country = row._2
    pop_ts = pop_data[pop_data["Country Code"] == country]
    if not pop_ts.empty:
        pop_ts.reset_index(drop=True,inplace=True)
        for year in years:
            pop = pop_ts.at[0,str(year)]
            co2 = sector_per_capita.at[row.Index, year]
            sector_per_capita.at[row.Index, year] = 10**6 * co2 / pop # convert from Mt => t




 

    




#print(sector_data)
#print(pop_data)
