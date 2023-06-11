from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
from joblib import dump, load  # dump and load are imported for saving and loading the trained model


class Machine:
    def __init__(self, df: DataFrame):
        self.name = "Random Forest Classifier"
        target = df["Rarity"]
        features = df.drop(columns=["Rarity"])
        self.model = RandomForestClassifier()
        self.model.fit(features, target)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __call__(self, pred_basis: DataFrame):
        # predict_proba method is called on pred_basis
        # to get the predicted probabilities for each class.
        prediction, *_ = self.model.predict(pred_basis)
        probabilities, *_ = self.model.predict_proba(pred_basis)

        confidence = max(probabilities)
        # The maximum value of probabilities represents the highest confidence
        return prediction, confidence

    def save(self, filepath):
        #  The save method saves the trained model to a
        #  filepath using the dump function from joblib.
        dump(self, filepath)

    @staticmethod
    def open(filepath):
        # 'open' method loads a saved model from a specified
        # filepath using the load function from joblib.
        model = load(filepath)
        return model

    def info(self):
        return f"Base Model: {self.name}, <br>Timestamp: {self.timestamp} "


if __name__ == '__main__':
    from app.data import Database
    # import os
    # import pandas as pd
    db = Database('monster')
    print(db.count())
    # db.dataframe().to_csv(os.path.join("app", "monster.csv"))
    # print(os.path.join("app", "monster.csv"))
    df = db.dataframe().drop(columns=["Name", "Type", "Timestamp", "Damage"])
    pb = db.dataframe().drop(columns=["Rarity", "Name", "Type", "Timestamp", "Damage"])
    machine = Machine(df)
    print(machine(pred_basis=pb))

