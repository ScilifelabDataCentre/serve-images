import mlflow
import numpy as np
from sklearn.linear_model import LogisticRegression

mlflow.start_run()
X = np.array([-2, -1, 0, 1, 2, 1]).reshape(-1, 1)
y = np.array([0, 0, 1, 1, 1, 0])
lr = LogisticRegression()
lr.fit(X, y)

model_info = mlflow.sklearn.save_model(lr, "test_model")
mlflow.end_run()

sklearn_pyfunc = mlflow.pyfunc.load_model(model_uri=model_info.model_uri)

data = np.array([-4, 1, 0, 10, -2, 1]).reshape(-1, 1)

predictions = sklearn_pyfunc.predict(data)