# coding: iso-8859-1

import pandas as pd
import numpy as np
from pycountry import countries


raw_countries_to_final_countries = {
    'Bahamas, The'                  :'Bahamas',
    'British Virgin Islands'        :'Virgin Islands, British',
    'Congo, Dem. Rep.'              :'Congo, The Democratic Republic of the',
    'Congo, Rep.'                   :'Congo',
    'Egypt, Arab Rep.'              :'Egypt',
    'Eswatini'                      :'Swaziland',
    'Gambia, The'                   :'Gambia',
    'Hong Kong SAR, China'          :'Hong Kong',
    'Iran, Islamic Rep.'            :'Iran, Islamic Republic of',
    'Korea, Dem. People’s Rep.'     :'Korea, Democratic People\'s Republic of',
    'Korea, Rep.'                   :'Korea, Republic of',
    'Kyrgyz Republic'               :'Kyrgyzstan',
    'Lao PDR'                       :'Lao People\'s Democratic Republic',
    'Macao SAR, China'              :'Macao',
    'Micronesia, Fed. Sts.'         :'Micronesia, Federated States of',
    'Moldova'                       :'Moldova, Republic of',
    'North Macedonia'               :'Macedonia, Republic of',
    'Slovak Republic'               :'Slovakia',
    'St. Kitts and Nevis'           :'Saint Kitts and Nevis',
    'St. Lucia'                     :'Saint Lucia',
    'St. Martin (French part)'      :'Saint Martin (French part)',
    'St. Vincent and the Grenadines':'Saint Vincent and the Grenadines',
    'Tanzania'                      :'Tanzania, United Republic of',
    'Venezuela, RB'                 :'Venezuela, Bolivarian Republic of',
    'Virgin Islands (U.S.)'         :'Virgin Islands, U.S.',
    'Yemen, Rep.'                   :'Yemen',
    'Vietnam'                       :'Viet Nam',
    'Czech Republic'                :'Czechia',
    'Curacao'                       :'Curaçao',
    'Cote d\'Ivoire'                :'Côte d\'Ivoire',
    'Bolivia'                       :'Bolivia, Plurinational State of'
}


def transform_data(data, target_structure):
    for i in range(1, len(target_structure.keys())):
        for j in range(data[i-1].shape[0]):
            values = data[i-1].loc[j].values.tolist()
            # Remove metadata that is not needed
            del values[0:4]
            target_structure[list(target_structure.keys())[i]] += [float(x) for x in values]
    for i in range(data[0].shape[0]):
        values = data[0].loc[i].values.tolist()
        country = values[0]
        target_structure["Country and year"] += [country + " " + x for x in [str(x) for x in range(1960, 2021)]]

    # verify the values of the different metrics that were combined correspond to the same countries
    countries_per_file = []
    for i in range(0, len(target_structure.keys()) - 1):
        countries = []
        for k in range(data[i].shape[0]):
            values = data[0].loc[k].values.tolist()
            countries.append(values[0])
        countries_per_file.append(countries)
    for i in range(0, len(countries_per_file)):
        if i != len(countries_per_file) - 1:
            assert countries_per_file[i] == countries_per_file[i + 1]

    return pd.DataFrame(target_structure)

def remove_aggregated_data(data):
    # additional adjustment, needed because of naming-discrepancies between the given data and the used library
    for raw_country, final_country in raw_countries_to_final_countries.items():
        for index in data[data["Country and year"].str.contains(raw_country)].index.values:
            data.at[index, "Country and year"] = final_country + data.at[index, "Country and year"][-5:]

    countries_list = []
    for country in countries:
        countries_list.append(country.name)
    countries_list.extend(['West Bank and Gaza', 'Kosovo'])

    country_indices = np.array([])
    for country in countries_list:
        country_indices = np.concatenate((country_indices, data[data["Country and year"].str.startswith(country)].index.values))

    return data.loc[country_indices].reset_index(drop = True)

def remove_rows_without_sufficient_neighbors(data):
    row_indices_to_keep = []
    values = data["Country and year"].tolist()

    for index in range(len(values)):
        if not index in [0, 1]:
            same_country_as_previous_value0 = values[index - 1][0:-4] == values[index - 2][0:-4]
            same_country_as_previous_value1 = values[index][0:-4] == values[index - 1][0:-4]
            if same_country_as_previous_value0 and same_country_as_previous_value1:
                if int(values[index][-4:]) == int(values[index - 1][-4:]) + 1 and int(values[index - 1][-4:]) == int(values[index - 2][-4:]) + 1:
                    row_indices_to_keep.append(index - 2)
                    row_indices_to_keep.append(index - 1)
                    row_indices_to_keep.append(index)

    row_indices_to_keep = list(set(row_indices_to_keep))
    all_current_indices = list(data.index.values)
    row_indices_to_drop = [x for x in all_current_indices if x not in row_indices_to_keep]

    return data.drop(row_indices_to_drop).reset_index(drop = True)

def calculate_yearly_changes(given_data):
    result = pd.DataFrame(columns = ["Country and timespan", "Agriculture percentage of GDP (change)", "GDP per capita (in USD 2010) (change)", "Industry percentage of GDP (change)", "Infant mortality per 1000 life births (change)", "Primary education completion percentage", "Population (change)", "Population density (people per sq. km) (change)", "Service percentage of GDP (change)", "Life expectancy (in years) at births", "Poverty headcount ratio at $1.90 a day (2011 PPP) (% of population) increased", "Poverty headcount ratio increased next year"])
    values = given_data["Country and year"].tolist()
    for index in range(len(values)):
        if index not in  [0, 1]:
            same_country_as_previous_value0 = values[index - 1][0:-4] == values[index - 2][0:-4]
            same_country_as_previous_value1 = values[index][0:-4] == values[index - 1][0:-4]
            if same_country_as_previous_value0 and same_country_as_previous_value1:
                values_this_row = given_data.loc[index].values.tolist()
                values_pre_row = given_data.loc[index - 1].values.tolist()
                values_pre_pre_row = given_data.loc[index - 2].values.tolist()
                new_row = [values_pre_pre_row[0][0:-4] + values_pre_pre_row[0][-4:] + " - " + values_pre_row[0][-4:]]
                for i in range(1, 10):
                    new_row.append(values_pre_row[i]/values_pre_pre_row[i])

                if values_pre_pre_row[10] != 0:
                    new_row.append(values_pre_row[10]/values_pre_pre_row[10])
                else:
                    continue
                if values_pre_row[10] != 0:
                    new_row.append(values_this_row[10]/values_pre_row[10])
                else:
                    continue

                result.loc[len(result)] = new_row

    median_change = result["Poverty headcount ratio at $1.90 a day (2011 PPP) (% of population) increased"].append(result["Poverty headcount ratio increased next year"]).median()
    print("median_change: " + str(median_change))
    poverty_change_rel_to_median = []
    for value in result["Poverty headcount ratio at $1.90 a day (2011 PPP) (% of population) increased"].tolist():
        change_greater_than_median_change = 1.0 if value - median_change > 0 else 0.0
        poverty_change_rel_to_median.append(change_greater_than_median_change)
    poverty_future_change_rel_to_median = []
    for value in result["Poverty headcount ratio increased next year"].tolist():
        change_greater_than_median_change = 1.0 if value - median_change > 0 else 0.0
        poverty_future_change_rel_to_median.append(change_greater_than_median_change)

    result["Poverty headcount ratio increased more than median change"] = poverty_change_rel_to_median
    result["Poverty headcount ratio next year increased more than median change"] = poverty_future_change_rel_to_median

    result = result.drop(columns = ["Poverty headcount ratio at $1.90 a day (2011 PPP) (% of population) increased", "Poverty headcount ratio increased next year"])

    return result.reset_index(drop = True)


def main():
    path_to_data = "data_raw/"
    file_extension = ".csv"
    file_names = ["agriculture_gdp_perc", "constant_us_gdp_per_capita", "industry_gdp_perc", "infant_mort_per_1000_life_births", "perc_primary_compl_rate", "population", "population_density", "service_gdp_perc", "years_life_expectancy_at_birth", "poverty_ratio"]
    all_data = []
    for file_name in file_names:
        all_data.append(pd.read_csv(path_to_data + file_name + file_extension, decimal = ","))
        # remove last column since it does not contain any data
        all_data[-1].drop(labels = "Unnamed: 65", axis = 1, inplace = True)

    target_structure = {"Country and year": [], "Agriculture percentage of GDP": [], "GDP per capita (in USD 2010)": [], "Industry percentage of GDP": [], "Infant mortality per 1000 life births": [], "Primary education completion percentage": [], "Population": [], "Population density (people per sq. km)": [], "Service percentage of GDP": [], "Life expectancy (in years) at births": [], "Poverty headcount ratio at $1.90 a day (2011 PPP) (% of population)": []}
    transformed_data = transform_data(all_data, target_structure)
    transformed_data = remove_aggregated_data(transformed_data)
    for column in transformed_data.columns:
        print("column: " + column)
        print(transformed_data[column].isna().sum()/len(transformed_data))
    # remove rows with missing data
    transformed_data = transformed_data.dropna().reset_index(drop = True)
    transformed_data = remove_rows_without_sufficient_neighbors(transformed_data)
    transformed_data = calculate_yearly_changes(transformed_data)

    print(transformed_data)
    # persist dataframe to file
    transformed_data.to_pickle("transformed_data.pkl")

if __name__ == "__main__":
    main()
