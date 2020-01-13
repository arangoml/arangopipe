#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:30:38 2019

@author: Rajiv Sambasivan
"""
import unittest
import sys
import traceback
from arangopipe.arangopipe_storage.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.custom_http_client import CustomHTTPClient
from arangopipe.arangopipe_storage.managed_service_conn_parameters import ManagedServiceConnParam
from arango import ArangoClient, DatabaseListError


class TestAdminMSDB(unittest.TestCase):
    def setUp(self):
        #mshost: "5366b66b7d19.arangodb.cloud"
        conn_config = ArangoPipeConfig()
        self.mscp = ManagedServiceConnParam()
        conn_params = { self.mscp.DB_SERVICE_HOST : "9abae0039203.arangodb.cloud", \
        self.mscp.DB_USER_NAME : "arangopipe",\
        self.mscp.DB_PASSWORD : "arangopipe",\
        self.mscp.DB_NAME : "arangopipe", \
        self.mscp.DB_ROOT_USER : "root",\
        self.mscp.DB_ROOT_USER_PASSWORD : "bM3IbqTurunvtrNngO83",\
        self.mscp.DB_SERVICE_END_POINT : "createDB",\
        self.mscp.DB_SERVICE_NAME : "createDB",\
        self.mscp.DB_SERVICE_PORT : 8529,\
        self.mscp.DB_CONN_PROTOCOL : 'https'}
        self.delete_users()
        self.delete_arangopipe_db()

        conn_config = conn_config.create_connection_config(conn_params)
        self.admin = ArangoPipeAdmin(reuse_connection = False, config = conn_config)

        return

    def test_delete_all_databases(self):
        err_raised = False

        try:
            self.admin.delete_all_databases()
        except :
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while registering dataset')
        self.assertFalse(err_raised)

        return

    def test_using_deleted_database(self):
        err_raised = False
        print("Running the test using a stale connection... ")
        self.delete_arangopipe_db()
        new_admin = ArangoPipeAdmin(reuse_connection = True)
        ap_config = new_admin.get_config()

        try:
            ap = ArangoPipe(config = ap_config)
        except Exception:
            print("Stale connection identified...")
            print("Using a new connection...")
            mscp = ManagedServiceConnParam()
            conn_config = ArangoPipeConfig()
            conn_params = { mscp.DB_SERVICE_HOST : "9abae0039203.arangodb.cloud", \
                        mscp.DB_SERVICE_END_POINT : "createDB",\
                        mscp.DB_SERVICE_NAME : "createDB",\
                        mscp.DB_SERVICE_PORT : 8529,\
                        mscp.DB_CONN_PROTOCOL : 'https',\
                        mscp.DB_ROOT_USER : 'root',
                        mscp.DB_ROOT_USER_PASSWORD: 'bM3IbqTurunvtrNngO83'}
            conn_config = conn_config.create_connection_config(conn_params)
            admin = ArangoPipeAdmin(reuse_connection = False, config = conn_config)
            ap_config = admin.get_config()
            ap = ArangoPipe(config = ap_config)

        print ("Using new connection to look up a non existent dataset...")
        ap.lookup_dataset("non existent dataset")
        self.assertFalse(err_raised)

        return




    def delete_users(self):

        print("Deleting users before test !")
        pl = ['_system', 'root', 'rajiv', 'node2vec_db_admin', 'susr']
        host_connection = "https://9abae0039203.arangodb.cloud:8529/"
        client = ArangoClient(hosts= host_connection,\
                            http_client=CustomHTTPClient('root', 'bM3IbqTurunvtrNngO83'))
        sys_db = client.db('_system',\
                           username="root",\
                           password="bM3IbqTurunvtrNngO83")
        ul = sys_db.users()
        unl = [ tu['username'] for tu in ul]
        for u in unl:
            if not u in pl:
                sys_db.delete_user(u)

        return

    def delete_arangopipe_db(self):
        print("Deleting users before test !")
        pl = ['_system', 'root', 'rajiv', 'node2vec_db_admin', 'susr']
        host_connection = "https://9abae0039203.arangodb.cloud:8529/"
        client = ArangoClient(hosts= host_connection,\
                            http_client=CustomHTTPClient('root', 'bM3IbqTurunvtrNngO83'))
        sys_db = client.db('_system',\
                           username="root",\
                           password="bM3IbqTurunvtrNngO83")
        try:
            if sys_db.has_database("arangopipe"):
                print("Before starting the test, cleaning up arangopipe instances...")
                sys_db.delete_database("arangopipe")
            else:
                print("Test Prep: The database arangopipe does not exist !")

        except DatabaseListError as err:
            print.error(err)
            print("Error code: " + str(err.error_code) + " received !")
            print("Error Message: " + str(err.error_message))


    def test_delete_database(self):
        err_raised = False

        try:
            self.admin.delete_database("arangopipe")
        except :
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while deleting database')
        self.assertFalse(err_raised)

        return





if __name__ == '__main__':
    unittest.main()
