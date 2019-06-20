# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

import os
import warnings


import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

import mlflow
import mlflow.sklearn
from arangopipe.arangopipe_api import ArangoPipe
import datetime


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2



if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)
    ap = ArangoPipe()
    # Read the wine-quality csv file (make sure you're running this from the root of MLflow!)
    wine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wine-quality.csv")
    data = pd.read_csv(wine_path)

    ds_reg = ap.lookup_dataset("wine dataset")
    fs_reg = ap.lookup_featureset("wine_no_transformations")
    
    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = 0.2
    l1_ratio = 0.1

    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)
        ruuid = mlflow.active_run().info.run_uuid
        model_reg = ap.lookup_model("elastic_net_wine_model")
        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        
        model_params = {"l1_ratio": l1_ratio, "alpha": alpha, "run_id": str(ruuid)}
        model_perf = {"rmse": rmse, "r2": r2, "mae": mae, "run_id": str(ruuid),\
                      "timestamp": str(datetime.datetime.now())}
        run_info = {"dataset" : ds_reg["_key"],\
                    "featureset": fs_reg["_key"],\
                    "model": model_reg["_key"],\
                    "run_id": ruuid,\
                    "model-params": model_params,\
                    "model-perf": model_perf,\
                    "pipeline" : "Wine-Regression-Pipeline",\
                    "project": "Wine-Quality-Assessment"}
      
        ap.log_run(run_info)
        mlflow.sklearn.log_model(lr, "model")
