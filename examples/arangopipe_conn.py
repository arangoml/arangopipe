from arangopipe.arangopipe_storage.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.managed_service_conn_parameters import ManagedServiceConnParam
from arangopipe.arangopipe_storage.connection_manager import arango_pipe_connections


def conn_arangopipe(conn_params):
    valid_conn_info_provided = validate_conn_params(conn_params)
    conn_info = None
    
    if valid_conn_info_provided:
        with arango_pipe_connections(conn_params, False) as (ap_admin, ap):
            conn_info = {"ap_admin": ap_admin, "ap": ap}
            print("Obtained connection for R Arangopipe Connector!")
    else:
        print("Please try again after fixing connection information errors!")
        msg = "Incorrect connection info, Please try again after fixing connection information errors!"
        raise Exception(msg)
        
    return conn_info 

def validate_conn_params(conn_params):
    valid_conn_params = True
    msc = ManagedServiceConnParam()
    
    if not msc.DB_SERVICE_HOST in conn_params:
        print("Service host information not provided!, please provide")
        valid_conn_params = False
    
    if not msc.DB_SERVICE_END_POINT in conn_params:
        print("Service end point information not provided!, please provide")
        valid_conn_params = False
    
    if not msc.DB_SERVICE_NAME in conn_params:
        print("Service name information not provided!, please provide")
        valid_conn_params = False
    
    if not msc.DB_SERVICE_PORT in conn_params:
        print("Service port information not provided!, please provide")
        valid_conn_params = False
    
    if not msc.DB_CONN_PROTOCOL in conn_params:
        print("Service connection protocol information not provided!, please provide")
        valid_conn_params = False
    
    return valid_conn_params
    
    



      
    
