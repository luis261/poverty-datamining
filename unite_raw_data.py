import pandas as pd

agriculture_data = pd.read_csv("data_raw/agriculture_gdp_perc.csv", decimal = ",")
# remove last column since it does not contain any data
agriculture_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)

gdp_per_cap_data = pd.read_csv("data_raw/constant_us_gdp_per_capita.csv", decimal = ",")
gdp_per_cap_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)

industry_gdp_perc_data = pd.read_csv("data_raw/industry_gdp_perc.csv", decimal = ",")
industry_gdp_perc_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)

infant_mort_data = pd.read_csv("data_raw/infant_mort_per_1000_life_births.csv", decimal = ",")
infant_mort_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)

prim_compl_rate_data = pd.read_csv("data_raw/perc_primary_compl_rate.csv", decimal = ",")
prim_compl_rate_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)

population_data = pd.read_csv("data_raw/population.csv", decimal = ",")
population_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)

population_density_data = pd.read_csv("data_raw/population_density.csv", decimal = ",")
population_density_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)

service_gdp_perc_data = pd.read_csv("data_raw/service_gdp_perc.csv", decimal = ",")
service_gdp_perc_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)

life_expectancy_data = pd.read_csv("data_raw/years_life_expectancy_at_birth.csv", decimal = ",")
life_expectancy_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)

"""
print(data.head())
print(data.shape)
print(data.loc[0, "1960"])
print(data["1960"])

print("count:")
print(data["Unnamed: 65"].isna().sum())
"""
