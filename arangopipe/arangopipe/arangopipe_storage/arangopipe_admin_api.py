#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:30:33 2019

@author: Rajiv Sambasivan
"""

from arango import ArangoClient, DatabaseListError
import logging
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.custom_http_client import CustomHTTPClient
from arangopipe.arangopipe_storage.managed_service_conn_parameters import ManagedServiceConnParam
import json
import requests
#import traceback
import sys
# create logger with 'spam_application'
logger = logging.getLogger('arangopipe_admin_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('arangopipeadmin.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class ArangoPipeAdmin:
    def __init__(self, reuse_connection=True, config=None, persist_conn=True):
        self.reuse_connection = reuse_connection
        self.db = None
        self.emlg = None
        self.config = None
        self.cfg = None
        self.mscp = ManagedServiceConnParam()
        self.use_supp_config_to_reconnect = False

        if reuse_connection:
            info_msg = "If a config is provided, it will be used for setting up the connection"
            if config is None:
                self.config = self.create_config()
                self.cfg = self.config.get_cfg()
                self.use_supp_config_to_reconnect = False
            else:
                self.config = config
                self.cfg = config.cfg
                self.use_supp_config_to_reconnect = True

            logger.info(info_msg)
        else:

            assert config is not None,\
                   "You must provide connection information for new connections"

            self.config = config
            self.cfg = config.cfg

        try:

            db_serv_host = self.cfg['arangodb'][self.mscp.DB_SERVICE_HOST]
            db_serv_port = self.cfg['arangodb'][self.mscp.DB_SERVICE_PORT]
            db_end_point = self.cfg['arangodb'][self.mscp.DB_SERVICE_END_POINT]
            db_serv_name = self.cfg['arangodb'][self.mscp.DB_SERVICE_NAME]

        except KeyError as k:
            logger.error("Connection information is missing : " + k.args[0])
            logger.error(
                "Please try again after providing the missing information !")
            raise Exception("Key error associated with missing " + k.args[0])

        # check if connection preferences are indicated
        if 'dbName' in self.cfg['arangodb']:
            logger.info("DB name for connection: " + \
                        str(self.cfg['arangodb'][self.mscp.DB_NAME]))
            db_dbName = self.cfg['arangodb'][self.mscp.DB_NAME]
        else:
            db_dbName = ''
        if 'username' in self.cfg['arangodb']:
            logger.info("user name for connection: " +\
                        str(self.cfg['arangodb'][self.mscp.DB_USER_NAME]))
            db_user_name = self.cfg['arangodb'][self.mscp.DB_USER_NAME]
        else:
            db_user_name = ''
        if 'password' in self.cfg['arangodb']:
            logger.info("A specific password was requested !")
            db_password = self.cfg['arangodb'][self.mscp.DB_PASSWORD]
        else:
            db_password = ''

        if self.mscp.DB_CONN_PROTOCOL in self.cfg['arangodb']:
            db_conn_protocol = self.cfg['arangodb'][self.mscp.DB_CONN_PROTOCOL]
        else:
            db_conn_protocol = "http"

        if self.mscp.DB_REPLICATION_FACTOR in self.cfg['arangodb']:
            db_replication_factor = self.cfg['arangodb'][
                self.mscp.DB_REPLICATION_FACTOR]
        else:
            db_replication_factor = None

        if self.mscp.DB_ROOT_USER in self.cfg['arangodb']:
            logger.info("A root user was specified, persisting...")

        if self.mscp.DB_ROOT_USER_PASSWORD in self.cfg['arangodb']:
            logger.info("A root user password was specified, persisting...")


        self.create_db(db_serv_host, db_serv_port,\
                       db_serv_name, db_end_point,\
                       db_dbName, db_user_name, db_password, db_conn_protocol)

        # If you could create a DB, proceed with provisioning the graph. Otherwise you
        # had an issue creating the database.
        if self.db is not None:
            self.create_enterprise_ml_graph(db_replication_factor)

            if persist_conn:
                self.config.dump_data()

        return

    def check_repeated_creation(self, api_data):
        if not api_data:
            repeated_connection = False
        else:
            try:
                user_name_equal = api_data[self.mscp.DB_USER_NAME] ==\
                self.cfg['arangodb'][self.mscp.DB_USER_NAME]
                password_equal =  api_data[self.mscp.DB_PASSWORD] ==\
                self.cfg['arangodb'][self.mscp.DB_PASSWORD]
                db_name_equal = api_data[self.mscp.DB_NAME] ==\
                self.cfg['arangodb'][self.mscp.DB_NAME]
                repeated_connection = user_name_equal or password_equal or db_name_equal
                if user_name_equal:
                    logger.info(
                        "Attempting to create a connection with an existing username"
                    )
                if db_name_equal:
                    logger.info(
                        "Attempting to create a connection with an existing db name"
                    )
            except KeyError:
                repeated_connection = False

        return repeated_connection

    def set_connection_params(self, config):
        self.cfg = config
        self.cfg.dump_data()
        return

    def create_config(self):
        apc = ArangoPipeConfig()
        return apc

    def get_config(self):
        return self.config

    def create_db(self, db_srv_host, db_srv_port, db_serv_name,\
                  db_end_point, db_dbName, db_user_name, db_password,\
                  db_conn_protocol):

        host_connection = db_conn_protocol + "://" + db_srv_host + ":" + str(
            db_srv_port)
        client = ArangoClient(hosts=host_connection)
        logger.debug("Connection reuse: " + str(self.reuse_connection))
        if not self.reuse_connection:
            API_ENDPOINT = host_connection + "/_db/_system/" + db_end_point + \
                            "/" + db_serv_name
            print("API endpoint: " + API_ENDPOINT)

            if db_dbName:
                logger.info("DB name preferrence: " + str(db_dbName))
            if db_user_name:
                logger.info("DB user name preferrence: " + str(db_user_name))
            if db_password:
                logger.info(
                    "Password preference for managed connection was indicated !"
                )

            api_data = {self.mscp.DB_NAME : db_dbName,\
                        self.mscp.DB_USER_NAME: db_user_name,\
                        self.mscp.DB_PASSWORD: db_password }
            logger.info("Requesting a managed service database...")

            r = requests.post(url=API_ENDPOINT, json=api_data, verify=False)

            if r.status_code == 409 or r.status_code == 400:
                logger.error(
                    "It appears that you are attempting to connecting using \
                             existing connection information. So either set reconnect = True when you create ArangoPipeAdmin or recreate a connection config and try again!"
                )
                return

            assert r.status_code == 200, \
            "Managed DB endpoint is unavailable !, reason: " + r.reason + " err code: " +\
            str(r.status_code)
            result = json.loads(r.text)
            logger.info("Managed service database was created !")
            ms_dbName = result['dbName']
            ms_user_name = result['username']
            ms_password = result['password']
            self.cfg['arangodb'][self.mscp.DB_NAME] = ms_dbName
            self.cfg['arangodb'][self.mscp.DB_USER_NAME] = ms_user_name
            self.cfg['arangodb'][self.mscp.DB_PASSWORD] = ms_password
            self.cfg['arangodb'][self.mscp.DB_SERVICE_HOST] = db_srv_host
            self.cfg['arangodb'][self.mscp.DB_SERVICE_NAME] = db_serv_name
            self.cfg['arangodb'][self.mscp.DB_SERVICE_END_POINT] = db_end_point
            self.cfg['arangodb'][self.mscp.DB_SERVICE_PORT] = db_srv_port
            self.cfg['arangodb'][self.mscp.DB_CONN_PROTOCOL] = db_conn_protocol

        else:
            if self.use_supp_config_to_reconnect:
                ms_dbName = self.cfg['arangodb'][self.mscp.DB_NAME]
                ms_user_name = self.cfg['arangodb'][self.mscp.DB_USER_NAME]
                ms_password = self.cfg['arangodb'][self.mscp.DB_PASSWORD]

            else:
                disk_cfg = ArangoPipeConfig()
                pcfg = disk_cfg.get_cfg()  # persisted config values
                ms_dbName = pcfg['arangodb'][self.mscp.DB_NAME]
                ms_user_name = pcfg['arangodb'][self.mscp.DB_USER_NAME]
                ms_password = pcfg['arangodb'][self.mscp.DB_PASSWORD]
                self.config = disk_cfg
                self.cfg = disk_cfg.cfg
        # Connect to arangopipe database as administrative user.
        #This returns an API wrapper for "test" database.
        print("Host Connection: " + str(host_connection))
        client = ArangoClient(hosts= host_connection,\
                              http_client=CustomHTTPClient(username = ms_user_name,\
                                                           password = ms_password))

        db = client.db(ms_dbName, ms_user_name, ms_password)
        self.db = db

        return

    def create_enterprise_ml_graph(self, db_replication_factor):

        cl = ['project', 'models', 'datasets', 'featuresets', 'modelparams', 'run',\
              'devperf', 'servingperf', 'deployment']

        if self.reuse_connection:
            self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])
            return

        if not self.db.has_graph(self.cfg['mlgraph']['graphname']):
            self.emlg = self.db.create_graph(self.cfg['mlgraph']['graphname'])
        else:
            self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])

        for col in cl:
            if not self.emlg.has_vertex_collection(col):
                self.db.create_collection(col, db_replication_factor)
                self.emlg.create_vertex_collection(col)


        from_list = ['project', 'models', 'run', 'run', 'run', 'run',\
                     'deployment', 'deployment', 'deployment', 'deployment',\
                     'featuresets']
        to_list = ['models', 'run', 'modelparams', 'datasets', 'devperf',\
                   'featuresets', 'servingperf', 'models', 'modelparams',\
                   'featuresets', 'datasets']
        edge_names = ['project_models', 'run_models', 'run_modelparams', 'run_datasets',\
                      'run_devperf', 'run_featuresets', 'deployment_servingperf', \
                      'deployment_model', 'deployment_modelparams', 'deployment_featureset',\
                       'featureset_dataset']
        for edge, fromv, tov in zip(edge_names, from_list, to_list):
            if not self.emlg.has_edge_definition(edge):
                self.db.create_collection(edge, edge = True,\
                                          replication_factor = db_replication_factor)
                self.emlg.create_edge_definition(edge_collection = edge,\
                                                      from_vertex_collections = [fromv],\
                                                      to_vertex_collections = [tov] )

        self.cfg['arangodb'][
            self.mscp.DB_REPLICATION_FACTOR] = db_replication_factor

        return

    def register_project(self, p):

        projects = self.emlg.vertex_collection("project")
        proj_reg = projects.insert(p)

        return proj_reg

    def delete_arangomldb(self):

        return

    def register_deployment(self, dep_tag):

        # Execute the query
        cursor = self.db.aql.execute(
            'FOR doc IN run FILTER doc.deployment_tag == @value RETURN doc',
            bind_vars={'value': dep_tag})
        run_docs = [doc for doc in cursor]
        the_run_doc = run_docs[0]
        # Get the model params for the run
        rmpe = self.emlg.edge_collection("run_modelparams")
        edge_dict = rmpe.edges(the_run_doc, direction="out")
        tmp_id = edge_dict["edges"][0]["_to"]
        mpc = self.emlg.edge_collection("modelparams")
        tagged_model_params = mpc.get(tmp_id)
        # Get the model for the run
        rme = self.emlg.edge_collection("run_models")
        edge_dict = rme.edges(the_run_doc, direction="in")
        tm_id = edge_dict["edges"][0]["_from"]
        mc = self.emlg.edge_collection("models")
        tagged_model = mc.get(tm_id)
        # Get the featureset for the run
        rfse = self.emlg.edge_collection("run_featuresets")
        edge_dict = rfse.edges(the_run_doc, direction="out")
        tfid = edge_dict["edges"][0]["_to"]
        tfc = self.emlg.edge_collection("featuresets")
        tagged_featureset = tfc.get(tfid)
        # Create a deployment artifact
        deployment = self.emlg.vertex_collection("deployment")
        deploy_info = {"tag": dep_tag}
        dep_reg = deployment.insert(deploy_info)
        #Link the deployment to the model parameters
        dep_model_params_edge = self.emlg.edge_collection(
            "deployment_modelparams")
        dep_model_params_key = dep_reg["_key"] + "-" + tagged_model_params[
            "_key"]
        the_dep_model_param_edge = { "_key": dep_model_params_key,\
                                "_from": dep_reg["_id"],\
                                "_to": tagged_model_params["_id"]}

        dep_mp_reg = dep_model_params_edge.insert(the_dep_model_param_edge)

        # Link the deployment to the featureset
        dep_featureset_edge = self.emlg.edge_collection(
            "deployment_featureset")
        dep_featureset_key = dep_reg["_key"] + "-" + tagged_featureset["_key"]
        the_dep_featureset_edge = { "_key": dep_featureset_key,\
                                "_from": dep_reg["_id"],\
                                "_to": tagged_featureset["_id"]}
        dep_fs_reg = dep_featureset_edge.insert(the_dep_featureset_edge)

        # Link the deployment to the model
        dep_model_edge = self.emlg.edge_collection("deployment_model")
        dep_featureset_key = dep_reg["_key"] + "-" + tagged_model["_key"]
        the_dep_model_edge = { "_key": dep_featureset_key,\
                                "_from": dep_reg["_id"],\
                                "_to": tagged_model["_id"]}

        dep_model_reg = dep_model_edge.insert(the_dep_model_edge)
        return dep_model_reg

    def add_vertex_to_arangopipe(self, vertex_to_create):
        rf = self.cfg['arangodb'][self.mscp.DB_REPLICATION_FACTOR]

        if not self.db.has_graph(self.cfg['mlgraph']['graphname']):
            self.emlg = self.db.create_graph(self.cfg['mlgraph']['graphname'])
        else:
            self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])

        #Check if vertex exists in the graph, if not create it
        if not self.emlg.has_vertex_collection(vertex_to_create):
            self.db.create_collection(vertex_to_create, rf)
            self.emlg.create_vertex_collection(vertex_to_create)
        else:
            logger.error("Vertex, " + vertex_to_create + " already exists!")

        return

    def remove_vertex_from_arangopipe(self, vertex_to_remove, purge=True):

        if not self.db.has_graph(self.cfg['mlgraph']['graphname']):
            self.emlg = self.db.create_graph(self.cfg['mlgraph']['graphname'])
        else:
            self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])

        #Check if vertex exists in the graph, if not create it
        if self.emlg.has_vertex_collection(vertex_to_remove):
            self.emlg.delete_vertex_collection(vertex_to_remove, purge)

            logger.info("Vertex collection " + vertex_to_remove +
                        " has been deleted!")
        else:
            logger.error("Vertex, " + vertex_to_remove + " does not exist!")

        return

    def add_edge_definition_to_arangopipe(self, edge_name, from_vertex_name,
                                          to_vertex_name):
        rf = self.cfg['arangodb'][self.mscp.DB_REPLICATION_FACTOR]

        if not self.db.has_graph(self.cfg['mlgraph']['graphname']):
            self.emlg = self.db.create_graph(self.cfg['mlgraph']['graphname'])
        else:
            self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])

        #Check if all data needed to create an edge exists, if so, create it

        if not self.emlg.has_vertex_collection(from_vertex_name):
            logger.error("Source vertex, " + from_vertex_name +\
                         " does not exist, aborting edge creation!")
            return
        elif not self.emlg.has_vertex_collection(to_vertex_name):
            logger.error("Destination vertex, " + to_vertex_name +\
                         " does not exist, aborting edge creation!")
            return

        else:
            if not self.emlg.has_edge_definition(edge_name):
                self.db.create_collection(edge_name, edge = True,\
                                          replication_factor = rf)
                self.emlg.create_edge_definition(edge_collection = edge_name,\
                                                 from_vertex_collections=[from_vertex_name],\
                                                 to_vertex_collections=[to_vertex_name] )
            else:
                logger.error("Edge, " + edge_name + " already exists!")

        return

    def remove_edge_definition_from_arangopipe(self, edge_name, purge=True):

        if not self.db.has_graph(self.cfg['mlgraph']['graphname']):
            self.emlg = self.db.create_graph(self.cfg['mlgraph']['graphname'])
        else:
            self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])

        if self.emlg.has_edge_definition(edge_name):
            self.emlg.delete_edge_definition(edge_name, purge)

        else:
            logger.error("Edge definition " + edge_name + " does not exist!")

        return

    def has_vertex(self, vertex_name):

        if not self.db.has_graph(self.cfg['mlgraph']['graphname']):
            self.emlg = self.db.create_graph(self.cfg['mlgraph']['graphname'])
        else:
            self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])

        result = self.emlg.has_vertex_collection(vertex_name)
        return result

    def has_edge(self, edge_name):

        if not self.db.has_graph(self.cfg['mlgraph']['graphname']):
            self.emlg = self.db.create_graph(self.cfg['mlgraph']['graphname'])
        else:
            self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])

        result = self.emlg.has_edge_definition(edge_name)

        return result

    def delete_all_databases(self,\
                             preserve = ['arangopipe', 'facebook_db', \
                                         'fb_node2vec_db', 'node2vecdb', '_system']):
        db_srv_host = self.cfg['arangodb'][self.mscp.DB_SERVICE_HOST]
        db_srv_port = self.cfg['arangodb'][self.mscp.DB_SERVICE_PORT]

        try:
            root_user = self.cfg['arangodb'][self.mscp.DB_ROOT_USER]
            root_user_password = self.cfg['arangodb'][
                self.mscp.DB_ROOT_USER_PASSWORD]
        except KeyError as k:
            msg = "Root credentials are unvailable, try again " + \
                     "with a new connection and credentials for root provided"
            logger.error(msg)
            logger.error("Credential information that is missing : " +
                         k.args[0])
            raise Exception("Key error associated with missing " + k.args[0])

        db_conn_protocol = self.cfg['arangodb'][self.mscp.DB_CONN_PROTOCOL]

        host_connection = db_conn_protocol + "://" + \
                db_srv_host + ":" + str(db_srv_port)
        if not root_user and not root_user_password:
            msg = "You will need to provide root credentials while connecting to perform" + \
                    " deletes of databases ! Please try again after doing so."
            logger.info(msg)
            return

        client = ArangoClient(hosts= host_connection,\
                              http_client=CustomHTTPClient(username=root_user,\
                                                           password = root_user_password))
        if not '_system' in preserve:
            preserve.append('_system')


        sys_db = client.db('_system',\
                                   username = root_user,\
                                   password = root_user_password)

        try:

            all_db = sys_db.databases()
            print("There were " + str(len(all_db) - 4) + " databases!")

            for the_db in all_db:
                if not the_db in preserve:
                    sys_db.delete_database(the_db)

        except DatabaseListError as err:
            logger.error(err)
            print("Error code: " + str(err.error_code) + " received !")
            print("Error Message: " + str(err.error_message))

        return

    def delete_database(self, db_to_delete):
        db_srv_host = self.cfg['arangodb'][self.mscp.DB_SERVICE_HOST]
        db_srv_port = self.cfg['arangodb'][self.mscp.DB_SERVICE_PORT]
        try:
            root_user = self.cfg['arangodb'][self.mscp.DB_ROOT_USER]
            root_user_password = self.cfg['arangodb'][
                self.mscp.DB_ROOT_USER_PASSWORD]
        except KeyError as k:
            msg = "Root credentials are unvailable, try again " + \
                     "with a new connection and credentials for root provided"
            logger.error(msg)
            logger.error("Credential information that is missing : " +
                         k.args[0])
            raise Exception("Key error associated with missing " + k.args[0])

        db_conn_protocol = self.cfg['arangodb'][self.mscp.DB_CONN_PROTOCOL]

        host_connection = db_conn_protocol + "://" + \
                db_srv_host + ":" + str(db_srv_port)
        if not root_user and not root_user_password:
            msg = "You will need to provide root credentials while connecting to perform" + \
                    " deletes of databases ! Please try again after doing so."
            logger.info(msg)
            return

        client = ArangoClient(hosts= host_connection,\
                              http_client=CustomHTTPClient(username=root_user,\
                                                           password = root_user_password))

        sys_db = client.db('_system',\
                               username = root_user,\
                               password = root_user_password)
        try:
            if sys_db.has_database(db_to_delete):
                sys_db.delete_database(db_to_delete)
            else:
                logger.error("The database, " + db_to_delete +
                             ", does not exist !")

        except DatabaseListError as err:
            logger.error(err)
            print("Error code: " + str(err.error_code) + " received !")
            print("Error Message: " + str(err.error_message))

        return
