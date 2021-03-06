import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score


def main():
    data = pd.read_pickle("final_data.pkl").drop(columns = ["Country and timespan"])
    print(data)

    print("Percentage of right guesses if you were to guess that the poverty headcount ratio increased more than the median change every year:")
    i = 0
    j = 0
    for x in data["POV"]:
        i += 1
        if x == 1.0:
            j += 1
    print(j/i)

    X = data.drop(columns = ["POV NXT"])
    y = data["POV NXT"]
    scores = cross_val_score(RandomForestClassifier(n_estimators = 10000), X, y, cv = 5)
    print("Percentage of right predictions of the model:")
    print(np.mean(scores))


if __name__ == "__main__":
    main()
