#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 17:16:53 2019

@author: Rajiv Sambasivan
"""
from arango import ArangoClient, DatabaseListError
import logging
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.custom_http_client import CustomHTTPClient
from arangopipe.arangopipe_storage.managed_service_conn_parameters import ManagedServiceConnParam
import json
import requests
import sys


def create_arangopipe_db(argv):
    
    assert len(argv) > 3 and len(argv) < 7, "Incorrect number of arguments provided to ms provisioning service"
    if len(argv) == 6:
        db_srv_port = argv[5]
    else:
        db_srv_port = 8529
    db_conn_protocol = argv[1]
    db_srv_host = argv[2]
    db_end_point = argv[3]
    db_serv_name = argv[4]
    mscp = ManagedServiceConnParam()
    for a in argv:
        print("argument: " + str(a))
    
    host_connection = db_conn_protocol + "://" + db_srv_host + ":" + str(db_srv_port)
    
    api_data = {mscp.DB_NAME : "arangopipe",\
                mscp.DB_USER_NAME: "arangopipe",\
                mscp.DB_PASSWORD: "localhost"}
    API_ENDPOINT = host_connection + "/_db/_system/" + db_end_point + \
                            "/" + db_serv_name
    r = requests.post(url=API_ENDPOINT, json=api_data, verify=False)
    print("Requesting a managed service database...")
    assert r.status_code == 200, \
        "Managed DB endpoint is unavailable !, reason: " + r.reason + " err code: " +\
        str(r.status_code)
    print("Provisioned arangopipe database on the managed database service")

        
    return
    
    
if __name__ == "__main__":
    create_arangopipe_db(sys.argv)