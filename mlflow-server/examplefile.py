import mlflow
import os

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

if __name__ == "__main__":
    # Start an MLflow experiment
    mlflow.tracking.set_tracking_uri("http://<container_ip>:5000")
    mlflow.create_experiment("my_experiment")
    mlflow.start_run()

    # Load data and split it into training and test sets
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target)

    # Train a model
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    # Log the model
    mlflow.sklearn.log_model(clf, "model")

    # Log some metrics
    mlflow.log_metric("accuracy", clf.score(X_test, y_test))
    mlflow.log_metric("loss", 1 - clf.score(X_test, y_test))

    # Log some parameters
    mlflow.log_param("num_trees", clf.n_estimators)
    mlflow.log_param("max_depth", clf.max_depth)

    # End the MLflow run
    mlflow.end_run()
