import uuid
import datetime

from arangopipe.arangopipe_storage.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.managed_service_conn_parameters import (
    ManagedServiceConnParam,
)


def create_arangopipe_connection():
    mdb_config = ArangoPipeConfig()
    msc = ManagedServiceConnParam()
    conn_params = {msc.DB_SERVICE_HOST: "arangoml.arangodb.cloud",
                   msc.DB_SERVICE_END_POINT: "createDB",
                   msc.DB_SERVICE_NAME: "createDB",
                   msc.DB_SERVICE_PORT: 8529,
                   msc.DB_CONN_PROTOCOL: 'https'}
    mdb_config = mdb_config.create_connection_config(conn_params)
    admin = ArangoPipeAdmin(config=mdb_config, reuse_connection=False)
    ap_config = admin.get_config()
    ap = ArangoPipe(config=ap_config)
    print(ap_config.get_cfg())
    return ap, admin


def bug():
    ap, admin = create_arangopipe_connection()
    project_name = "my_project"
    admin.register_project({"name": project_name})

    dataset_info = {
        "name": "IMDB Graph Dataset",
        "description": "This dataset contains movies and users along with the ratings that users have given them",
        "source": "IMDB",
    }
    dataset_reg = ap.register_dataset(dataset_info)

    featureset = {}
    featureset["name"] = "transformed_graph_data"

    feature_reg = ap.register_featureset(
        featureset, dataset_reg["_key"]
    )

    model_info = {
        "name": "GraphSAGE Model",
        "task": "Node Classification"
    }
    model_reg = ap.register_model(model_info, project=project_name)

    run_id = str(uuid.uuid4().int)
    model_params = {
        "run_id": run_id,
    }

    model_perf = {
        "run_id": run_id,
        "timestamp": str(datetime.datetime.now()),
    }

    run_info = {
        "dataset": dataset_reg["_key"],
        "featureset": feature_reg["_key"],
        "model": model_reg["_key"],
        "run_id": run_id,
        "custom_field": "this will not show up in the database",
        "model-params": model_params,
        "model-perf": model_perf,
        "tag": project_name,
        "project": project_name,
        "another_custom_field": "this is another custom field",
    }

    ap.log_run(run_info)


if __name__ == "__main__":
    bug()
