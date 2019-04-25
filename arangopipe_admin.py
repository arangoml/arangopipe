#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:30:33 2019

@author: admin2
"""

from arango import ArangoClient
import logging



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
    
    def __init__(self, user_name = "authorized_user"):
        self.user_name = user_name
        self.db = None
        self.emlg = None
        self.create_db()
        self.create_enterprise_ml_graph()
         
    def create_db(self):
        client = ArangoClient(protocol='http', host='localhost', port=8529)

        # Connect to "_system" database as root user.
        # This returns an API wrapper for "_system" database.
        sys_db = client.db('_system', username='root', password='admin123')

        # Create a new database named "test" if it does not exist.
        if not sys_db.has_database('arangopipe'):
            sys_db.create_database('arangopipe')
        
        if not sys_db.has_user("arangopipe"):
            sys_db.create_user(username = "arangopipe", password = "arangopipe")
    
        sys_db.update_permission(username = "arangopipe",\
                                 database = "arangopipe", permission = "rw")

        # Connect to "test" database as root user.
         #This returns an API wrapper for "test" database.
        db = client.db('arangopipe', username='arangopipe', password='arangopipe')
        self.db = db
         
        return
    
    def create_enterprise_ml_graph(self):
    
        if not self.db.has_graph('enterprise_ml_graph'):
            self.emlg = self.db.create_graph('enterprise_ml_graph')
        else:
            self.emlg = self.db.graph('enterprise_ml_graph')
        
        
        if not self.emlg.has_vertex_collection('project'):
            self.emlg.create_vertex_collection('project')
        
        if not self.emlg.has_vertex_collection('pipeline'):
            self.emlg.create_vertex_collection('pipeline')
            
        if not self.emlg.has_vertex_collection('models'):
            self.emlg.create_vertex_collection('models')
        
        if not self.emlg.has_vertex_collection('datasets'):
            self.emlg.create_vertex_collection('datasets')
        
        if not self.emlg.has_vertex_collection('featuresets'):
            self.emlg.create_vertex_collection('featuresets')
    
        if not self.emlg.has_vertex_collection('modelparams'):
            self.emlg.create_vertex_collection('modelparams')
    
        if not self.emlg.has_vertex_collection('modelperf'):
             self.emlg.create_vertex_collection('modelperf')
        
        if not self.emlg.has_vertex_collection('run'):
             self.emlg.create_vertex_collection('run')
             
        if not self.emlg.has_edge_definition('project_pipeline'):
            self.emlg.create_edge_definition(edge_collection = "project_pipeline",\
                                                      from_vertex_collections=['project'],\
                                                      to_vertex_collections=['pipeline'] )
        if not self.emlg.has_edge_definition('pipeline_models'):
            self.emlg.create_edge_definition(edge_collection = "pipeline_models",\
                                                      from_vertex_collections=['pipeline'],\
                                                      to_vertex_collections=['models'] )
        if not self.emlg.has_edge_definition('run_models'):
            self.emlg.create_edge_definition(edge_collection = "run_models",\
                                                      from_vertex_collections=['run'],\
                                                      to_vertex_collections=['models'] )
        if not self.emlg.has_edge_definition('run_datasets'):
            self.emlg.create_edge_definition(edge_collection = "run_datasets",\
                                                      from_vertex_collections=['run'],\
                                                      to_vertex_collections=['datasets'] )
        if not self.emlg.has_edge_definition('run_modelparams'):
            self.emlg.create_edge_definition(edge_collection = "run_modelparams",\
                                                      from_vertex_collections=['run'],\
                                                      to_vertex_collections=['modelparams'] )
        if not self.emlg.has_edge_definition('run_modelperf'):
            self.emlg.create_edge_definition(edge_collection = "run_modelperf",\
                                                      from_vertex_collections=['run'],\
                                                      to_vertex_collections=['modelperf'] )
        if not self.emlg.has_edge_definition('run_featuresets'):
            self.emlg.create_edge_definition(edge_collection = "run_featuresets",\
                                                      from_vertex_collections=['run'],\
                                                      to_vertex_collections=['featuresets'] )
        return
    

    

    def register_project(self, p):
        
        projects = self.emlg.vertex_collection("project")
        proj_reg = projects.insert(p)
        
        return proj_reg
    
    def register_pipeline(self, p):
        pipeline = self.emlg.vertex_collection("pipeline")
        pipeline_reg = pipeline.insert(p)
        return pipeline_reg
    
    def register_project_pipeline(self, proj_reg, pipeline_reg):
        ppl = self.emlg.edge_collection("project_pipeline")
        proj_ppl = proj_reg["_key"] + "-" + pipeline_reg["_key"]
        if not ppl.has(proj_ppl):
            edge_ppl = {"_key": proj_ppl,\
                        "_from": "project/" + proj_reg["_key"],\
                        "_to": "pipeline/" + pipeline_reg["_key"]}
            proj_ppl_reg = ppl.insert(edge_ppl)
        return proj_ppl_reg
    
    def delete_arangomldb(self):
        client = ArangoClient(protocol='http', host='localhost', port=8529)

        # Connect to "_system" database as root user.
        # This returns an API wrapper for "_system" database.
        sys_db = client.db('_system', username='root', password='admin123')

  
        if sys_db.has_database('arangopipe'):
            sys_db.delete_database('arangopipe')

        return