import pandas as pd


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

def calculate_poverty_index(data, column_names):
    # convert three parts of the index to values relative to the maximum value
    for i in [2, 5, 9]:
        max_value = data.loc[data[column_names[i]].idxmax()][column_names[i]]
        data[column_names[i]] = [x/max_value for x in list(data[column_names[i]])]

    calculated_poverty_index_values = []
    for index in data.index.values:
        row = data.loc[index]
        calculated_poverty_index_values.append(1 - (row[column_names[2]] * row[column_names[5]] * row[column_names[9]])**(1/3))
    data["Calculated poverty index"] = calculated_poverty_index_values

    for i in [2, 5, 9]:
        del data[column_names[i]]

    return data

def calculate_yearly_changes(given_data):
    result = pd.DataFrame(columns = ["Country and timespan", "Agriculture percentage of GDP (change)", "Industry percentage of GDP (change)", "Infant mortality per 1000 life births (change)", "Population (change)", "Population density (people per sq. km) (change)", "Service percentage of GDP (change)", "Poverty index increased", "Poverty index increased next year"])
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
                for i in range(1, 7):
                    new_row.append(values_pre_row[i]/values_pre_pre_row[i])
                new_row.append(values_pre_row[7]/values_pre_pre_row[7])
                new_row.append(values_this_row[7]/values_pre_row[7])
                result.loc[index] = new_row

    mean_change = (result["Poverty index increased"].mean() + result["Poverty index increased next year"].mean())/2
    print("mean_change: " + str(mean_change))
    poverty_change_rel_to_mean = []
    for value in result["Poverty index increased"].tolist():
        change_greater_than_mean_change = 1.0 if value - mean_change > 0 else 0.0
        poverty_change_rel_to_mean.append(change_greater_than_mean_change)
    poverty_future_change_rel_to_mean = []
    for value in result["Poverty index increased next year"].tolist():
        change_greater_than_mean_change = 1.0 if value - mean_change > 0 else 0.0
        poverty_future_change_rel_to_mean.append(change_greater_than_mean_change)

    result["Poverty index increased more than mean change"] = poverty_change_rel_to_mean
    result["Poverty index next year increased more than mean change"] = poverty_future_change_rel_to_mean

    result = result.drop(columns = ["Poverty index increased", "Poverty index increased next year"])

    return result.reset_index(drop = True)


def main():
    path_to_data = "data_raw/"
    file_names = ["agriculture_gdp_perc.csv", "constant_us_gdp_per_capita.csv", "industry_gdp_perc.csv", "infant_mort_per_1000_life_births.csv", "perc_primary_compl_rate.csv", "population.csv", "population_density.csv", "service_gdp_perc.csv", "years_life_expectancy_at_birth.csv"]
    all_data = []
    for file_name in file_names:
        all_data.append(pd.read_csv(path_to_data + file_name, decimal = ","))
        # remove last column since it does not contain any data
        all_data[-1].drop(labels = "Unnamed: 65", axis = 1, inplace = True)

    target_structure = {"Country and year": [], "Agriculture percentage of GDP": [], "GDP per capita (in USD 2010)": [], "Industry percentage of GDP": [], "Infant mortality per 1000 life births": [], "Primary education completion percentage": [], "Population": [], "Population density (people per sq. km)": [], "Service percentage of GDP": [], "Life expectancy (in years) at births": []}
    transformed_data = transform_data(all_data, target_structure)
    # remove rows with missing data
    transformed_data = transformed_data.dropna().reset_index(drop = True)
    transformed_data = remove_rows_without_sufficient_neighbors(transformed_data)
    transformed_data = calculate_poverty_index(transformed_data, list(target_structure.keys()))
    transformed_data = calculate_yearly_changes(transformed_data)

    print(transformed_data)
    print(transformed_data.loc[0])
    # persist dataframe to file
    transformed_data.to_pickle("transformed_data.pkl")

if __name__ == "__main__":
    main()
