from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import mlflow


def run_example(url, name):
    mlflow.tracking.set_tracking_uri(url)
    mlflow.set_experiment(name)

    mlflow.start_run()
    # Create some model
    clf = RandomForestClassifier()

    # Log the model
    mlflow.sklearn.log_model(clf, "model")

    # Log some metrics and params
    mlflow.log_metric("test_metric", 0.1)
    mlflow.log_param("test_param", 1.0)

    mlflow.end_run()
