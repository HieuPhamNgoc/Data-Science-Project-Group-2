import pandas as pd

path_co2 = 'data_processing/data_edga_2018/v60_GHG_CO2_excl_short-cycle_org_C_1970_2018/'
path_n2o = 'data_processing/data_edga_2018/v60_GHG_N2O_1970_2018/'
path_ch4 = 'data_processing/data_edga_2018/v60_GHG_CH4_1970_2018/'

def read_and_save_nordic(path, filename, sheet, emission, feature):
    df = pd.read_excel(path + filename, sheet_name=sheet)
    nordic = ['Finland', 'Denmark', 'Iceland', 'Norway', 'Sweden']
    df = df[df['Name'].isin(nordic)]
    df.to_csv(path + emission + ' emission ' + feature + ' nordic countries.csv')

'''
Taking CO2 emission data for nordic countries
'''


read_and_save_nordic(path_co2, 'v60_CO2_excl_short-cycle_org_C_1970_2018_raw.xls', 'v6.0_EM_CO2_fossil_IPCC2006', 'CO2', 'features')

read_and_save_nordic(path_co2, 'v60_CO2_excl_short-cycle_org_C_1970_2018_raw.xls','TOTALS BY COUNTRY', 'CO2', 'sum')

'''
Taking CH4 emission data for nordic countries
'''

read_and_save_nordic(path_ch4, 'v60_CH4_1970_2018_raw.xls', 'v6.0_EM_CH4_IPCC2006', 'CH4', 'features')

read_and_save_nordic(path_ch4, 'v60_CH4_1970_2018_raw.xls', 'TOTALS BY COUNTRY', 'CH4', 'sum')

'''
Taking N2O emission data for nordic countries
'''

read_and_save_nordic(path_n2o, 'v60_N2O_1970_2018_raw.xls', 'v6.0_EM_N2O_IPCC2006', 'N2O', 'features')

read_and_save_nordic(path_n2o, 'v60_N2O_1970_2018_raw.xls', 'TOTALS BY COUNTRY', 'N2O', 'sum')

