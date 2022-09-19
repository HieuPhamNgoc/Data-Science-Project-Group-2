import pandas as pd

path = 'data_processing/data_edga_2020/'
df_dict = pd.read_excel(path + 'EDGARv6.0_FT2020_fossil_CO2_GHG_booklet2021.xls', sheet_name = None)

print(df_dict.keys())

for key in df_dict.keys():
    
    if (key == 'info'):
        continue

    df = df_dict[key]
    df.to_csv(path + key + '.csv')

