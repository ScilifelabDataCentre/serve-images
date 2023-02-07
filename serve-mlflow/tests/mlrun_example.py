from sklearn.linear_model import LogisticRegression
import mlflow
import numpy as np
import sys


def run_example(experiment_name, model_name="test_model"):
    mlflow.set_experiment(experiment_name)

    X = np.array([-2, -1, 0, 1, 2, 1]).reshape(-1, 1)
    y = np.array([0, 0, 1, 1, 1, 0])

    mlflow.start_run()
    # Create some model
    clf = LogisticRegression()
    clf.fit(X, y)

    # Log the model
    mlflow.sklearn.log_model(clf, "model")

    # Log some metrics and params
    mlflow.log_metric("test_metric", 0.1)
    mlflow.log_param("test_param", 1.0)
    mlflow.sklearn.save_model(clf, model_name)

    mlflow.end_run()


if __name__ == "__main__":
    run_example(experiment_name=sys.argv[1], model_name=sys.argv[2])
