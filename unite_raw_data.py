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

rows_without_missing_values = pd.DataFrame(transformed_data).dropna().reset_index(drop = True)

row_indices_to_keep = []
values = rows_without_missing_values["Country and year"].tolist()

for index in range(len(values)):
    if not index == 0:
        same_country_as_previous_value = values[index][0:-4] == values[index - 1][0:-4]
        if same_country_as_previous_value:
            if int(values[index][-4:]) == int(values[index - 1][-4:]) + 1:
                row_indices_to_keep.append(index - 1)
                row_indices_to_keep.append(index)

row_indices_to_keep = list(set(row_indices_to_keep))
all_current_indices = list(rows_without_missing_values.index.values)
row_indices_to_drop = [x for x in all_current_indices if x not in row_indices_to_keep]

rows_without_missing_values = rows_without_missing_values.drop(row_indices_to_drop).reset_index(drop = True)

# convert three parts of "our" HDI to values relative to the maximum value
for i in [2, 5, 9]:
    max_value = rows_without_missing_values.loc[rows_without_missing_values[list(transformed_data.keys())[i]].idxmax()][list(transformed_data.keys())[i]]
    rows_without_missing_values[list(transformed_data.keys())[i]] = [x/max_value for x in list(rows_without_missing_values[list(transformed_data.keys())[i]])]

calculated_poverty_index_values = []
for index in rows_without_missing_values.index.values:
    row = rows_without_missing_values.loc[index]
    calculated_poverty_index_values.append(1 - (row[list(transformed_data.keys())[2]] * row[list(transformed_data.keys())[5]] * row[list(transformed_data.keys())[9]])**(1/3))
rows_without_missing_values["Calculated poverty index"] = calculated_poverty_index_values

for i in [2, 5, 9]:
    del rows_without_missing_values[list(transformed_data.keys())[i]]

print(rows_without_missing_values)
print(rows_without_missing_values.loc[0])

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
- generate new dataframe which does not contain absolute values, but contains the changes instead
- correlation analysis
"""
