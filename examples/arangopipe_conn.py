from arangopipe.arangopipe_storage.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.managed_service_conn_parameters import ManagedServiceConnParam
from arangopipe.arangopipe_storage.connection_manager import arango_pipe_connections


def conn_arangopipe():
  msc = ManagedServiceConnParam()
  conn_params = { msc.DB_SERVICE_HOST : "localhost", \
                  msc.DB_SERVICE_END_POINT : "createDB",\
                  msc.DB_SERVICE_NAME : "createDB",\
                  msc.DB_SERVICE_PORT : 8529,\
                  msc.DB_CONN_PROTOCOL : 'http'}
        
        
  with arango_pipe_connections(conn_params, False) as (ap_admin, ap):
      proj_info = {"name": "Context_Manager_Test"}
      proj_reg = ap_admin.register_project(proj_info)
      print("Done with context manager connection test!")
  return ap
  

      
    
