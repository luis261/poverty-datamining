import pandas as pd

all_data = []

# TODO compress
agriculture_data = pd.read_csv("data_raw/agriculture_gdp_perc.csv", decimal = ",")
# remove last column since it does not contain any data
agriculture_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)
all_data.append(agriculture_data)

gdp_per_cap_data = pd.read_csv("data_raw/constant_us_gdp_per_capita.csv", decimal = ",")
gdp_per_cap_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)
all_data.append(gdp_per_cap_data)

industry_gdp_perc_data = pd.read_csv("data_raw/industry_gdp_perc.csv", decimal = ",")
industry_gdp_perc_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)
all_data.append(industry_gdp_perc_data)

infant_mort_data = pd.read_csv("data_raw/infant_mort_per_1000_life_births.csv", decimal = ",")
infant_mort_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)
all_data.append(infant_mort_data)

prim_compl_rate_data = pd.read_csv("data_raw/perc_primary_compl_rate.csv", decimal = ",")
prim_compl_rate_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)
all_data.append(prim_compl_rate_data)

population_data = pd.read_csv("data_raw/population.csv", decimal = ",")
population_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)
all_data.append(population_data)

population_density_data = pd.read_csv("data_raw/population_density.csv", decimal = ",")
population_density_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)
all_data.append(population_density_data)

service_gdp_perc_data = pd.read_csv("data_raw/service_gdp_perc.csv", decimal = ",")
service_gdp_perc_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)
all_data.append(service_gdp_perc_data)

life_expectancy_data = pd.read_csv("data_raw/years_life_expectancy_at_birth.csv", decimal = ",")
life_expectancy_data.drop(labels = "Unnamed: 65", axis = 1, inplace = True)
all_data.append(life_expectancy_data)

print(life_expectancy_data.head())
print("shape")
print(life_expectancy_data.shape)

transformed_data = {"Country and year": [], "Agriculture percentage of GDP": [], "GDP per capita (in USD 2010)": [], "Industry percentage of GDP": [], "Infant mortality per 1000 life births": [], "Primary education completion percentage": [], "Population": [], "Population density (people per sq. km)": [], "Service percentage of GDP": [], "Life expectancy (in years) at births": []}

# print(list(transformed_data.keys())[0])


for i in range(1, len(transformed_data.keys())):
    for j in range(all_data[i-1].shape[0]):
        values = all_data[i-1].loc[j].values.tolist()
        # Remove metadata that is not needed
        del values[0:4]
        transformed_data[list(transformed_data.keys())[i]] += [float(x) for x in values]

for k in range(all_data[0].shape[0]):
    values = all_data[0].loc[k].values.tolist()
    country = values[0]
    transformed_data["Country and year"] += [country + " " + x for x in [str(x) for x in range(1960, 2021)]]

print(len(transformed_data["Country and year"]))
print(len(transformed_data["Agriculture percentage of GDP"]))

print("xxx")
for key in transformed_data.keys():
    print(len(transformed_data[key]))

final_df = pd.DataFrame(transformed_data).dropna().reset_index(drop = True)

print(final_df)

"""
row0 = []
row0.append(values[0])

print("country:")
print(values[0])

year = 1960
for i in range(4, len(values)):
    print("year:")
    print(year)
    print("value:")
    print(values[i])
    row0.append(values[i])
    year += 1

data = []
"""

"""
print(data.head())
print(data.shape)
print(data.loc[0, "1960"])
print(data["1960"])

print("count:")
print(data["Unnamed: 65"].isna().sum())
"""

"""
TODO next steps:
- remove all rows which do not have "neighbors"
- generate new dataframe which does not contain the individual components of our "HDI" but the actual values
- generate new dataframe which does not contain absolute values, but contains the changes instead
"""
