#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 08:35:58 2019

@author: admin2
"""

from arango import ArangoClient
import logging


# create logger with 'spam_application'
logger = logging.getLogger('arangoml_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('arangoml.log')
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

def create_db():
    client = ArangoClient(protocol='http', host='localhost', port=8529)

    # Connect to "_system" database as root user.
    # This returns an API wrapper for "_system" database.
    sys_db = client.db('_system', username='root', password='admin123')

    # Create a new database named "test" if it does not exist.
    if not sys_db.has_database('arangoml'):
        sys_db.create_database('arangoml')
        
    if not sys_db.has_user("arangoml"):
        sys_db.create_user(username = "arangoml", password = "arangoml")
    
    sys_db.update_permission(username = "arangoml", database = "arangoml", permission = "rw")

    # Connect to "test" database as root user.
    # This returns an API wrapper for "test" database.
    db = client.db('arangoml', username='arangoml', password='arangoml')
    

    
    return db

def create_enterprise_ml_graph(db):
    
    if not db.has_graph('enterprise_ml_graph'):
        emlg = db.create_graph('enterprise_ml_graph')
    else:
        emlg = db.graph('enterprise_ml_graph')
    
    
    if not emlg.has_vertex_collection('project'):
        emlg.create_vertex_collection('project')
    
    if not emlg.has_vertex_collection('pipeline'):
        emlg.create_vertex_collection('pipeline')
        
    if not emlg.has_vertex_collection('models'):
        emlg.create_vertex_collection('models')
    
    if not emlg.has_vertex_collection('datasets'):
        emlg.create_vertex_collection('datasets')
    
    if not emlg.has_vertex_collection('featuresets'):
        emlg.create_vertex_collection('featuresets')

    if not emlg.has_vertex_collection('modelparams'):
        emlg.create_vertex_collection('modelparams')

    if not emlg.has_vertex_collection('modelperf'):
         emlg.create_vertex_collection('modelperf')
    
    if not emlg.has_vertex_collection('run'):
         emlg.create_vertex_collection('run')
         
    if not emlg.has_edge_definition('project_pipeline'):
        emlg.create_edge_definition(edge_collection = "project_pipeline",\
                                                  from_vertex_collections=['project'],\
                                                  to_vertex_collections=['pipeline'] )
    if not emlg.has_edge_definition('pipeline_models'):
        emlg.create_edge_definition(edge_collection = "pipeline_models",\
                                                  from_vertex_collections=['pipeline'],\
                                                  to_vertex_collections=['models'] )
    if not emlg.has_edge_definition('run_models'):
        emlg.create_edge_definition(edge_collection = "run_models",\
                                                  from_vertex_collections=['run'],\
                                                  to_vertex_collections=['models'] )
    if not emlg.has_edge_definition('run_datasets'):
        emlg.create_edge_definition(edge_collection = "run_datasets",\
                                                  from_vertex_collections=['run'],\
                                                  to_vertex_collections=['datasets'] )
    if not emlg.has_edge_definition('run_modelparams'):
        emlg.create_edge_definition(edge_collection = "run_modelparams",\
                                                  from_vertex_collections=['run'],\
                                                  to_vertex_collections=['modelparams'] )
    if not emlg.has_edge_definition('run_modelperf'):
        emlg.create_edge_definition(edge_collection = "run_modelperf",\
                                                  from_vertex_collections=['run'],\
                                                  to_vertex_collections=['modelperf'] )
    if not emlg.has_edge_definition('run_featuresets'):
        emlg.create_edge_definition(edge_collection = "run_featuresets",\
                                                  from_vertex_collections=['run'],\
                                                  to_vertex_collections=['featuresets'] )
    
        

        
    return emlg
    

def get_enterprise_ml_graph():
    client = ArangoClient(protocol='http', host='localhost', port=8529)

    # Connect to "_system" database as root user.
    # This returns an API wrapper for "_system" database.
    sys_db = client.db('_system', username='root', password='admin123')
    
    if not sys_db.has_database('arangoml'):
        logger.info("Creating database and graph...")
        db = create_db()
        emlg = emlg = create_enterprise_ml_graph(db)
    else:
        db = client.db(name='arangoml', username='arangoml', password='arangoml')
        if db.has_graph('enterprise_ml_graph'):
            emlg = db.graph('enterprise_ml_graph')
        else:
            logger.info("Graph was not created, creating the graph")
            emlg = create_enterprise_ml_graph(db)
    
    return emlg


    
def delete_arangomldb():
    client = ArangoClient(protocol='http', host='localhost', port=8529)

    # Connect to "_system" database as root user.
    # This returns an API wrapper for "_system" database.
    sys_db = client.db('_system', username='root', password='admin123')

  
    if sys_db.has_database('arangoml'):
        sys_db.delete_database('arangoml')

    return

def register_project(p):
    emlg = get_enterprise_ml_graph()
    projects = emlg.vertex_collection("project")
    proj_reg = projects.insert(p)
    return proj_reg     

def register_pipeline(p):
    emlg = get_enterprise_ml_graph()
    pipeline = emlg.vertex_collection("pipeline")
    pipeline_reg = pipeline.insert(p)
    return pipeline_reg

def register_model(mi):
    emlg = get_enterprise_ml_graph()
    models = emlg.vertex_collection("models")
    model_reg = models.insert(mi)
    return model_reg

def register_dataset(ds_info):
    emlg = get_enterprise_ml_graph()
    ds = emlg.vertex_collection("datasets")
    ds_reg = ds.insert(ds_info)
    return ds_reg

def register_featureset(fs_info):
    emlg = get_enterprise_ml_graph()
    fs = emlg.vertex_collection("featuresets")
    fs_reg = fs.insert(fs_info)
    
    return fs_reg

def register_project_pipeline(proj_reg, pipeline_reg):
    emlg = get_enterprise_ml_graph()
    ppl = emlg.edge_collection("project_pipeline")
    proj_ppl = proj_reg["_key"] + "-" + pipeline_reg["_key"]
    if not ppl.has(proj_ppl):
        edge_ppl = {"_key": proj_ppl,\
                    "_from": "project/" + proj_reg["_key"],\
                    "_to": "pipeline/" + pipeline_reg["_key"]}
        proj_ppl_reg = ppl.insert(edge_ppl)
    return proj_ppl_reg

def get_tracking_info(pipeline_name):
    client = ArangoClient(protocol='http', host='localhost', port=8529)
    db = client.db(name='arangoml', username='arangoml', password='arangoml')
    # Execute the query
    cursor = db.aql.execute(
            'FOR doc IN pipeline FILTER doc.name == @value RETURN doc',
            bind_vars={'value': pipeline_name})
    ppl_keys = [doc for doc in cursor]
#    emlg = get_enterprise_ml_graph()
#    pipeline = emlg.vertex_collection("pipeline")
#    the_ppl = pipeline.get(ppl_keys[0])
    return ppl_keys[0]
    
    
def log_run(ri):
    #set_up()
    emlg = get_enterprise_ml_graph()
    rrid = ri["run_id"]
    mp = ri["model-params"]
    mp["_key"] = mp["run_id"]
    mperf = ri["model-perf"]
    mperf["_key"] = mperf["run_id"]

    
    run = emlg.vertex_collection("run")
    run_info = {"_key": rrid, \
                "featureset": ri["featureset"],\
                "dataset": ri["dataset"],\
                "timestamp": mperf["timestamp"]}
    print(run_info)
    run.insert(run_info)
    
    model_param = emlg.vertex_collection("modelparams")
    model_param.insert(mp)
  
    run_fs_edge = emlg.edge_collection("run_featuresets")
    run_fs_key = rrid + "-" +  ri["featureset"]
    
    if not run_fs_edge.has(run_fs_key):
        edge_run_fs = {"_key": run_fs_key,\
                    "_from": "run/" + rrid,\
                    "_to": "featuresets/" +  ri["featureset"]}
        
        run_fs_edge.insert(edge_run_fs)
    
 
    
    run_mp_edge = emlg.edge_collection("run_modelparams")
    run_mp_key = rrid + "-" + mp["run_id"]
    
    if not run_mp_edge.has(run_mp_key):
        edge_run_mp = {"_key": run_mp_key,\
                    "_from": "run/" + rrid,\
                    "_to": "modelparams/" + mp["run_id"]}
        
        run_mp_edge.insert(edge_run_mp)
    
    model_perf = emlg.vertex_collection("modelperf")
    model_perf.insert(mperf)
    
    run_model_perf_edge = emlg.edge_collection("run_modelperf")
    run_model_perf_key = rrid + "-" + mperf["run_id"]
    
    if not run_model_perf_edge.has(run_model_perf_key):
        edge_run_model_perf = {"_key": run_model_perf_key,\
                    "_from": "run/" + rrid,\
                    "_to": "modelperf/" + mperf["run_id"]}
        run_model_perf_edge.insert(edge_run_model_perf)
        
    run_dataset_edge = emlg.edge_collection("run_datasets")
    run_dataset_key = rrid + "-" + ri["dataset"]
    
    if not run_dataset_edge.has(run_dataset_key):
        edge_run_dataset = {"_key": run_dataset_key,\
                    "_from": "run/" + rrid,\
                    "_to": "datasets/" + ri["dataset"]}
        run_dataset_edge.insert(edge_run_dataset)
        

    return
    
    
    
    
    
        

    
    
    