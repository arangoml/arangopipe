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
import yaml
import os
    
    
class TestAdminMSDB(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TestAdminMSDB, self).__init__(*args, **kwargs)
        self.test_cfg = self.get_test_config()
        self.mscp = ManagedServiceConnParam()
        
        return
    
    def setUp(self):
        
        #mshost: "5366b66b7d19.arangodb.cloud"
        self.delete_users()
        self.delete_arangopipe_db()
        conn_config = ArangoPipeConfig()
        
        self.test_cfg = self.get_test_config()
        
        conn_params = { self.mscp.DB_SERVICE_HOST : self.test_cfg['arangodb'][self.mscp.DB_SERVICE_HOST], \
                        self.mscp.DB_USER_NAME : self.test_cfg['arangodb'][self.mscp.DB_USER_NAME],\
                        self.mscp.DB_PASSWORD : self.test_cfg['arangodb'][self.mscp.DB_PASSWORD],\
                        self.mscp.DB_NAME : self.test_cfg['arangodb'][self.mscp.DB_NAME], \
                        self.mscp.DB_ROOT_USER : self.test_cfg['arangodb'][self.mscp.DB_ROOT_USER],\
                        self.mscp.DB_ROOT_USER_PASSWORD : self.test_cfg['arangodb'][self.mscp.DB_ROOT_USER_PASSWORD],\
                        self.mscp.DB_SERVICE_END_POINT : self.test_cfg['arangodb'][self.mscp.DB_SERVICE_END_POINT],\
                        self.mscp.DB_SERVICE_NAME : self.test_cfg['arangodb'][self.mscp.DB_SERVICE_NAME],\
                        self.mscp.DB_SERVICE_PORT : self.test_cfg['arangodb'][self.mscp.DB_SERVICE_PORT],\
                        self.mscp.DB_CONN_PROTOCOL : self.test_cfg['arangodb'][self.mscp.DB_CONN_PROTOCOL]}
        
        conn_config = conn_config.create_connection_config(conn_params)
        self.admin = ArangoPipeAdmin(reuse_connection = False,\
                                     config = conn_config, persist_conn= False)
        
        return
    
    def get_test_config(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                     "../test_config/test_datagen_config.yaml")
        with open(file_name, "r") as file_descriptor:
            test_cfg = yaml.load(file_descriptor, Loader=yaml.FullLoader)
        
        return test_cfg
    
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
            conn_params = { mscp.DB_SERVICE_HOST : self.test_cfg['arangodb'][self.mscp.DB_SERVICE_HOST], \
                        mscp.DB_SERVICE_END_POINT : self.test_cfg['arangodb'][self.mscp.DB_SERVICE_END_POINT],\
                        mscp.DB_SERVICE_NAME : self.test_cfg['arangodb'][self.mscp.DB_SERVICE_NAME],\
                        mscp.DB_SERVICE_PORT : self.test_cfg['arangodb'][self.mscp.DB_SERVICE_PORT],\
                        mscp.DB_CONN_PROTOCOL : self.test_cfg['arangodb'][self.mscp.DB_CONN_PROTOCOL]}
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
        host_connection = self.test_cfg['arangodb'][self.mscp.DB_CONN_PROTOCOL] + "://" + \
        self.test_cfg['arangodb'][self.mscp.DB_SERVICE_HOST] + ":" + \
        str(self.test_cfg['arangodb'][self.mscp.DB_SERVICE_PORT])
        try:
            root_user = self.test_cfg['arangodb'][self.mscp.DB_ROOT_USER]
            root_user_password = self.test_cfg['arangodb'][
                self.mscp.DB_ROOT_USER_PASSWORD]
        except KeyError as k:
            msg = "Root credentials are unvailable, try again " + \
                     "with a new connection and credentials for root provided"
            print(msg)
            print("Credential information that is missing : " +
                         k.args[0])
            raise Exception("Key error associated with missing " + k.args[0])
        
        client = ArangoClient(hosts= host_connection,\
                            http_client=CustomHTTPClient(username=root_user,\
                                                         password= root_user_password))
        sys_db = client.db('_system',\
                           username=self.test_cfg['arangodb'][self.mscp.DB_ROOT_USER],\
                           password=self.test_cfg['arangodb'][self.mscp.DB_ROOT_USER_PASSWORD])
        ul = sys_db.users()
        unl = [ tu['username'] for tu in ul]
        for u in unl:
            if not u in pl:
                sys_db.delete_user(u)
    
        return
    
    def delete_arangopipe_db(self):
        print("Deleting users before test !")

        host_connection = self.test_cfg['arangodb'][self.mscp.DB_CONN_PROTOCOL] + "://" + \
        self.test_cfg['arangodb'][self.mscp.DB_SERVICE_HOST] + ":" + \
        str(self.test_cfg['arangodb'][self.mscp.DB_SERVICE_PORT])
        try:
            root_user = self.test_cfg['arangodb'][self.mscp.DB_ROOT_USER]
            root_user_password = self.test_cfg['arangodb'][
                self.mscp.DB_ROOT_USER_PASSWORD]
        except KeyError as k:
            msg = "Root credentials are unvailable, try again " + \
                     "with a new connection and credentials for root provided"
            print(msg)
            print("Credential information that is missing : " +
                         k.args[0])
            raise Exception("Key error associated with missing " + k.args[0])
        client = ArangoClient(hosts= host_connection,\
                            http_client=CustomHTTPClient(username=root_user,\
                                                         password= root_user_password))
        sys_db = client.db('_system',\
                           username=self.test_cfg['arangodb'][self.mscp.DB_ROOT_USER],\
                           password=self.test_cfg['arangodb'][self.mscp.DB_ROOT_USER_PASSWORD] )
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
 
            

        
