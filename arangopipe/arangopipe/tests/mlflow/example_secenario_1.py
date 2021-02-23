# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

import mlflow
import mlflow.sklearn
from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe
import datetime
from arangopipe.arangopipe_storage.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.managed_service_conn_parameters import ManagedServiceConnParam


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":

    proj_info = {"name": "Wine-Quality-Regression-Modelling"}
    conn_config = ArangoPipeConfig()
    msc = ManagedServiceConnParam()
    conn_params = { msc.DB_SERVICE_HOST : "localhost", \
                    msc.DB_SERVICE_END_POINT : "apmdb",\
                    msc.DB_SERVICE_NAME : "createDB",\
                    msc.DB_SERVICE_PORT : 8529,
                    msc.DB_CONN_PROTOCOL : 'http'}

    conn_config = conn_config.create_connection_config(conn_params)
    admin = ArangoPipeAdmin(reuse_connection=False, config=conn_config)
    proj_reg = admin.register_project(proj_info)

    warnings.filterwarnings("ignore")
    np.random.seed(40)
    ap_config = admin.get_config()
    ap = ArangoPipe(config=ap_config)

    # Read the wine-quality csv file (make sure you're running this from the root of MLflow!)
    wine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "wine-quality.csv")
    data = pd.read_csv(wine_path)
    ds_info = {"name" : "wine dataset",\
                   "description": "Wine quality ratings","source": "UCI ML Repository" }
    ds_reg = ap.register_dataset(ds_info)
    featureset = data.dtypes.to_dict()
    featureset = {k: str(featureset[k]) for k in featureset}
    featureset["name"] = "wine_no_transformations"
    fs_reg = ap.register_featureset(featureset, ds_reg["_key"])
    model_info = {
        "name": "elastic_net_wine_model",
        "type": "elastic net regression"
    }
    model_reg = ap.register_model(model_info,
                                  project="Wine-Quality-Regression-Modelling")

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)
        ruuid = mlflow.active_run().info.run_uuid
        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        model_params = {
            "l1_ratio": l1_ratio,
            "alpha": alpha,
            "run_id": str(ruuid)
        }
        model_perf = {"rmse": rmse, "r2": r2, "mae": mae, "run_id": str(ruuid),\
                      "timestamp": str(datetime.datetime.now())}
        run_info = {"dataset" : ds_reg["_key"],\
                    "featureset": fs_reg["_key"],\
                    "run_id": ruuid,\
                    "model": model_reg["_key"],\
                    "model-params": model_params,\
                    "model-perf": model_perf,\
                    "pipeline" : "Wine-Regression-Pipeline",\
                    "project": "Wine-Quality-Assessment"}

        ap.log_run(run_info)
        mlflow.sklearn.log_model(lr, "model")
