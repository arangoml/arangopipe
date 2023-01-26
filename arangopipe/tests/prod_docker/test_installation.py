import sys
import traceback

from arangopipe.arangopipe.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_storage.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.managed_service_conn_parameters import (
    ManagedServiceConnParam,
)


def verify_install():
    # mshost: "5366b66b7d19.arangodb.cloud"
    config = ArangoPipeConfig()
    msc = ManagedServiceConnParam()
    conn_params = {
        msc.DB_SERVICE_HOST: "d874fc3f1fa5.arangodb.cloud",
        msc.DB_SERVICE_END_POINT: "apmdb",
        msc.DB_SERVICE_NAME: "createDB",
        msc.DB_SERVICE_PORT: 8529,
        msc.DB_CONN_PROTOCOL: "https",
        msc.DB_NOTIFICATION_EMAIL: "somebody@some_company.com",
    }

    config = config.create_connection_config(conn_params)
    admin = ArangoPipeAdmin(reuse_connection=False, config=config)
    ap_config = admin.get_config()
    ap = ArangoPipe(config=ap_config)
    ap.lookup_dataset("non existent dataset")
    try:
        proj_info = {"name": "Wine-Quality-Regression-Modelling"}
        proj_reg = admin.register_project(proj_info)
    except:
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)

    print("Installation of Arangopipe API verified !")

    return
