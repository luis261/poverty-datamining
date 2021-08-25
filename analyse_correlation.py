import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


def shorten_column_names(df):
    df.columns = ["Country and timespan", "AGR GDP %", "GDPPC", "IND GDP %", "IMR", "PECR", "POP", "POPD", "SVCS GDP %", "LE", "POV", "POV NXT"]
    return df

def main():
    data = pd.read_pickle("transformed_data.pkl")
    data = shorten_column_names(data)

    print(data.corr(method = "pearson", min_periods = 1))

    plt.figure(figsize=(9, 6))
    hm = sb.heatmap(data.corr(method = "pearson", min_periods = 1), annot = True)
    hm.set_yticklabels(hm.get_yticklabels(), rotation = 0, fontsize = 8)
    hm.set_xticklabels(hm.get_xticklabels(), rotation = 45, fontsize = 8)
    plt.show()

    del data["POPD"]
    data.to_pickle("final_data.pkl")


if __name__ == "__main__":
    main()
