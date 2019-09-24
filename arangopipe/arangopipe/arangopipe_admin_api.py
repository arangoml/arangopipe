#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:30:33 2019

@author: admin2
"""

from arango import ArangoClient
import logging
from arangopipe.arangopipe_config import ArangoPipeConfig
from arangopipe.custom_http_client import CustomHTTPClient


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
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

class ArangoPipeAdmin:
    
    def __init__(self, user_name = "authorized_user", config = None, persist = False):
        self.user_name = user_name
        self.db = None

        self.emlg = None
        if config is None:
            self.cfg = self.get_config()
        else:
            self.cfg = config.cfg
            if persist:
                config.dump_data()
        self.create_db()
        self.create_enterprise_ml_graph()
    
    def set_connection_params(self, config):
        self.cfg = config
        self.cfg.dump_data()
        return


        
    def get_config(self):
        apc = ArangoPipeConfig()
        return apc.get_cfg()
        
         
    def create_db(self):
        client = ArangoClient(hosts=self.cfg['arangodb']['host'],\
                              http_client=CustomHTTPClient())

        # Connect to "_system" database as root user.
        # This returns an API wrapper for "_system" database.
        sys_db = client.db('_system',\
                           username=self.cfg['arangodb']['root_user'],
                           password=self.cfg['arangodb']['root_user_password'])

        # Create a new arangopipe database if it does not exist.
        if not sys_db.has_database(self.cfg['arangodb']['arangopipe_dbname']):
            sys_db.create_database(self.cfg['arangodb']['arangopipe_dbname'])
        
        if not sys_db.has_user(self.cfg['arangodb']['arangopipe_admin_username']):
            sys_db.create_user(username = self.cfg['arangodb']['arangopipe_admin_username'],\
                               password = self.cfg['arangodb']['arangopipe_admin_password'])
    
        sys_db.update_permission(username = self.cfg['arangodb']['arangopipe_admin_username'],\
                                 database = self.cfg['arangodb']['arangopipe_dbname'], permission = "rw")

        # Connect to arangopipe database as administrative user.
         #This returns an API wrapper for "test" database.
        db = client.db(self.cfg['arangodb']['arangopipe_dbname'],\
                       username=self.cfg['arangodb']['arangopipe_admin_username'],\
                       password=self.cfg['arangodb']['arangopipe_admin_password'])
        self.db = db
         
        return
    
    def create_enterprise_ml_graph(self):
    
        if not self.db.has_graph(self.cfg['mlgraph']['graphname']):
            self.emlg = self.db.create_graph(self.cfg['mlgraph']['graphname'])
        else:
            self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])
        
        
        if not self.emlg.has_vertex_collection('project'):
            self.emlg.create_vertex_collection('project')
        

            
        if not self.emlg.has_vertex_collection('models'):
            self.emlg.create_vertex_collection('models')
        
        if not self.emlg.has_vertex_collection('datasets'):
            self.emlg.create_vertex_collection('datasets')
        
        if not self.emlg.has_vertex_collection('featuresets'):
            self.emlg.create_vertex_collection('featuresets')
    
        if not self.emlg.has_vertex_collection('modelparams'):
            self.emlg.create_vertex_collection('modelparams')
    
        if not self.emlg.has_vertex_collection('run'):
             self.emlg.create_vertex_collection('run')
        
        if not self.emlg.has_vertex_collection('devperf'):
             self.emlg.create_vertex_collection('devperf')
                
        if not self.emlg.has_vertex_collection('servingperf'):
             self.emlg.create_vertex_collection('servingperf')
        
        if not self.emlg.has_vertex_collection('deployment'):
             self.emlg.create_vertex_collection('deployment')
        
        
        
        if not self.emlg.has_edge_definition('project_models'):
            self.emlg.create_edge_definition(edge_collection = "project_models",\
                                                      from_vertex_collections=['project'],\
                                                      to_vertex_collections=['models'] )  
        
        if not self.emlg.has_edge_definition('run_models'):
            self.emlg.create_edge_definition(edge_collection = "run_models",\
                                                      from_vertex_collections=['models'],\
                                                      to_vertex_collections=['run'] )     

        if not self.emlg.has_edge_definition('run_modelparams'):
            self.emlg.create_edge_definition(edge_collection = "run_modelparams",\
                                                      from_vertex_collections=['run'],\
                                                      to_vertex_collections=['modelparams'] )
        if not self.emlg.has_edge_definition('run_datasets'):
            self.emlg.create_edge_definition(edge_collection = "run_datasets",\
                                                      from_vertex_collections=['run'],\
                                                      to_vertex_collections=['datasets'] )

        if not self.emlg.has_edge_definition('run_devperf'):
            self.emlg.create_edge_definition(edge_collection = "run_devperf",\
                                                      from_vertex_collections=['run'],\
                                                      to_vertex_collections=['devperf'] )
        if not self.emlg.has_edge_definition('run_featuresets'):
            self.emlg.create_edge_definition(edge_collection = "run_featuresets",\
                                                      from_vertex_collections=['run'],\
                                                      to_vertex_collections=['featuresets'] )

        if not self.emlg.has_edge_definition('deployment_servingperf'):
            self.emlg.create_edge_definition(edge_collection = "deployment_servingperf",\
                                                      from_vertex_collections=['deployment'],\
                                                      to_vertex_collections=['servingperf'] )
        if not self.emlg.has_edge_definition('deployment_model'):
            self.emlg.create_edge_definition(edge_collection = "deployment_model",\
                                                      from_vertex_collections=['deployment'],\
                                                      to_vertex_collections=['models'] )
        if not self.emlg.has_edge_definition('deployment_modelparams'):
            self.emlg.create_edge_definition(edge_collection = "deployment_modelparams",\
                                                      from_vertex_collections=['deployment'],\
                                                      to_vertex_collections=['modelparams'] )
        if not self.emlg.has_edge_definition('deployment_featureset'):
            self.emlg.create_edge_definition(edge_collection = "deployment_featureset",\
                                                      from_vertex_collections=['deployment'],\
                                                      to_vertex_collections=['featuresets'] )
        if not self.emlg.has_edge_definition('featureset_dataset'):
            self.emlg.create_edge_definition(edge_collection = "featureset_dataset",\
                                                      from_vertex_collections=['featuresets'],\
                                                      to_vertex_collections=['datasets'] ) 
        return
    

    

    def register_project(self, p):
        
        projects = self.emlg.vertex_collection("project")
        proj_reg = projects.insert(p)
        
        return proj_reg
    

    
    def delete_arangomldb(self):

        client = ArangoClient(hosts=self.cfg['arangodb']['host'],\
                              http_client=CustomHTTPClient())

        sys_db = client.db('_system',\
                           username=self.cfg['arangodb']['root_user'],\
                           password=self.cfg['arangodb']['root_user_password'])

  
        if sys_db.has_database('arangopipe'):
            sys_db.delete_database('arangopipe')

        return
    
    def register_deployment(self, dep_tag):
        client = ArangoClient(hosts=self.cfg['arangodb']['host'],\
                              http_client=CustomHTTPClient())
        db = client.db(name =self.cfg['arangodb']['arangopipe_dbname'],\
                       username = self.cfg['arangodb']['arangopipe_admin_username'],\
                       password = self.cfg['arangodb']['arangopipe_admin_password'])
        # Execute the query
        cursor = db.aql.execute(
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
        dep_model_params_edge = self.emlg.edge_collection("deployment_modelparams")
        dep_model_params_key = dep_reg["_key"] + "-" + tagged_model_params["_key"]
        the_dep_model_param_edge = { "_key": dep_model_params_key,\
                                "_from": dep_reg["_id"],\
                                "_to": tagged_model_params["_id"]}
        
        dep_mp_reg = dep_model_params_edge.insert(the_dep_model_param_edge)
        
        # Link the deployment to the featureset
        dep_featureset_edge = self.emlg.edge_collection("deployment_featureset")
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
    
    

    

        
        
        
