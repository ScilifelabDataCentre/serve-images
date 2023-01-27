import os
import mlflow
import numpy as np
from sklearn.linear_model import LogisticRegression


def create_test_model():
    with mlflow.start_run():
        X = np.array([-2, -1, 0, 1, 2, 1]).reshape(-1, 1)
        y = np.array([0, 0, 1, 1, 1, 0])
        lr = LogisticRegression()
        lr.fit(X, y)

        mlflow.sklearn.save_model(lr, os.path.join("tests", "test_model"))
