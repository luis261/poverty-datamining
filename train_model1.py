import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def main():
    data = pd.read_pickle("final_data.pkl").drop(columns = ["Country and timespan"])
    print(data)

    i = 0
    j = 0
    for x in data["POV"]:
        i += 1
        if x == 1.0:
            j += 1

    print(j/i)

    X = data.drop(columns = ["POV NXT"])
    y = data["POV NXT"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    model = RandomForestClassifier(n_estimators = 10000)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(accuracy_score(y_test, predictions))


if __name__ == "__main__":
    main()
