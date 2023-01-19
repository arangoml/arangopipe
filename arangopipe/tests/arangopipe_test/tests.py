from arango import ArangoClient
from environment_settings import settings

from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe

# Initialize the client for ArangoDB.
client = ArangoClient(hosts=settings.TEST_HOST_NAME)
# Connect to "test" database as root user.
test_db = client.db(
    settings.TEST_DB_NAME,
    username=settings.TEST_USERNAME,
    password=settings.TEST_PASSWORD,
)

# Create ArangoPipe passing the test_db for database ops
ap = ArangoPipe(test_db, settings.TEST_GRAPH_NAME)


proj_info = {"name": "Housing_Price_Estimation_Project"}
proj_reg = ap.register_project(proj_info)
ds_info = {
    "name": "california-housing-dataset",
    "description": "This dataset lists median house prices in California. Various house features are provided",
    "source": "UCI ML Repository",
}
ds_reg = ap.register_dataset(ds_info)
features = {"featurea": [0, 1], "featureb": [0, 1]}
featureset = features
featureset = {k: str(featureset[k]) for k in featureset}
featureset["name"] = "log_transformed_median_house_value"
fs_reg = ap.register_featureset(featureset, ds_reg["_key"])
model_info = {
    "name": "Bias Variance Analysis of LASSO model",
    "task": "Model Validation",
}
model_reg = ap.register_model(model_info, project="Housing_Price_Estimation_Project")
import datetime
import uuid

ruuid = str(uuid.uuid4().int)
model_perf = {
    "model_bias": 100,
    "run_id": ruuid,
    "timestamp": str(datetime.datetime.now()),
}

mp = {
    "alpha": 0.001,
    "copy_X": True,
    "fit_intercept": True,
    "max_iter": 1000,
    "normalize": "deprecated",
    "positive": False,
    "precompute": False,
    "random_state": None,
    "selection": "cyclic",
    "tol": 0.0001,
    "warm_start": False,
}

model_params = {"run_id": ruuid, "model_params": mp}

run_info = {
    "dataset": ds_reg["_key"],
    "featureset": fs_reg["_key"],
    "run_id": ruuid,
    "model": model_reg["_key"],
    "model-params": model_params,
    "model-perf": model_perf,
    "tag": "Housing-Price-Hyperopt-Experiment",
    "project": "Housing Price Estimation Project",
}
ap.log_run(run_info)
