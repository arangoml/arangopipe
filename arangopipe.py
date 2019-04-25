#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 08:35:58 2019

@author: admin2
"""

from arango import ArangoClient
import logging



# create logger with 'spam_application'
logger = logging.getLogger('arangopipe_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('arangopipe.log')
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

class ArangoPipe:
    
    """ An instance of ArangoPipe is meant to be used to log a run of a pipeline execution. To use it:
        (1) Create a ArangoPipe object
        (2) Register your dataset with ArangoPipe
        (3) Register your featureset with ArangoPipe
        (4) Register you model with ArangoPipe
"""
    def __init__(self):
        self.emlg = None
        self.init_graph()




    def lookup_pipeline(self, pipeline_name):
        """ Return a pipeline identifier given a name. This can be used to get the pipeline id that is used to log run information associated with execution of the pipeline. """
        client = ArangoClient(protocol='http', host='localhost', port=8529)
        db = client.db(name='arangopipe', username='arangopipe', password='arangopipe')
        # Execute the query
        cursor = db.aql.execute(
                'FOR doc IN pipeline FILTER doc.name == @value RETURN doc',
                bind_vars={'value': pipeline_name})
        ppl_keys = [doc for doc in cursor]
    
        return ppl_keys[0]
    


    def lookup_dataset(self, dataset_name):
            
        """ Return a dataset identifier given a name. This can be used to get the dataset id that is used to log run information associated with execution of the pipeline."""
        client = ArangoClient(protocol='http', host='localhost', port=8529)
        db = client.db(name='arangopipe', username='arangopipe', password='arangopipe')
        # Execute the query
        cursor = db.aql.execute(
                'FOR doc IN datasets FILTER doc.name == @value RETURN doc',
                bind_vars={'value': dataset_name})
        dataset_keys = [doc for doc in cursor]
    
        return dataset_keys[0]
    


    def lookup_featureset(self, feature_set_name):
                
        """ Return a featureset identifier given a name. This can be used to get the featureset id that is used to log run information associated with execution of the pipeline."""
        client = ArangoClient(protocol='http', host='localhost', port=8529)
        db = client.db(name='arangopipe', username='arangopipe', password='arangopipe')
        # Execute the query
        cursor = db.aql.execute(
                'FOR doc IN featuresets FILTER doc.name == @value RETURN doc',
                bind_vars={'value': feature_set_name})
        feature_set_keys = [doc for doc in cursor]
    
        return feature_set_keys[0]


    def lookup_model(self, model_name):
            
        """ Return a model identifier given a name. This can be used to get the model id that is used to log run information associated with execution of the pipeline."""
        client = ArangoClient(protocol='http', host='localhost', port=8529)
        db = client.db(name='arangopipe', username='arangopipe', password='arangopipe')
        # Execute the query
        cursor = db.aql.execute(
                'FOR doc IN featuresets FILTER doc.name == @value RETURN doc',
                bind_vars={'value': model_name})
        model_keys = [doc for doc in cursor]
    
        return model_keys[0]



    def init_graph(self):
        """ Initialize a graph when an instance of ArangoPipe is provisioned. """
        client = ArangoClient(protocol='http', host='localhost', port=8529)
    
        # Connect to "_system" database as root user.
        # This returns an API wrapper for "_system" database.
        sys_db = client.db('_system', username='root', password='admin123')
        
        if not sys_db.has_database('arangopipe'):
            logger.error("arangopipe database has not been created.")
            raise AttributeError("arangopipe database has not been created!")
        else:
            db = client.db(name='arangopipe', username='arangopipe', password='arangopipe')
            if db.has_graph('enterprise_ml_graph'):
                self.emlg = db.graph('enterprise_ml_graph')
            else:
                logger.error("ML tracking graph was not created. ")
                raise AttributeError("ML tracking graph has not been created")
        
        return
    

    
    
    def register_model(self, mi, user_id = "authorized_user"):
        """ Register a model. The operation requires specifying a user id. If the user id is permitted to register a model, then the registration proceeds, otherwise an unauthorized operation is indicated. """
        models = self.emlg.vertex_collection("models")
        model_reg = models.insert(mi)
        
        return model_reg

    def register_dataset(self, ds_info, user_id = "authorized_user"):
        """ Register a dataset. The operation requires specifying a user id. If the user id is permitted to register a dataset, then the registration proceeds, otherwise an unauthorized operation is indicated. """
        ds = self.emlg.vertex_collection("datasets")
        ds_reg = ds.insert(ds_info)
        return ds_reg

    
def register_featureset(self, fs_info, user_id = "authorized_user"):
    """ Register a featureset. The operation requires specifying a user id. If the user id is permitted to register a featureset, then the registration proceeds, otherwise an unauthorized operation is indicated. """
    fs = self.emlg.vertex_collection("featuresets")
    fs_reg = fs.insert(fs_info)
    
    return fs_reg

def update_featureset(self, fs_info, user_id = "authorized_user"):
    """ Update a featureset. The operation requires specifying a user id. If the user id is permitted to update a featureset, then the update proceeds, otherwise an unauthorized operation is indicated. """
    # Is this a replace or update of a field? An update implicitly assumes a data structure or schema.
    pass 
    
    return 

def update_dataset(self, ds_info, user_id = "authorized_user"):
    """ Update a featureset. The operation requires specifying a user id. If the user id is permitted to update a dataset, then the update proceeds, otherwise an unauthorized operation is indicated. """
    pass
    
    return

def update_model(self, ds_info, user_id = "authorized_user"):
    """ Update a model. The operation requires specifying a user id. If the user id is permitted to update a model, then the update proceeds, otherwise an unauthorized operation is indicated. """
    pass
    
    return  
    
    def log_run(self, ri):
    
        """ Log a run. Logging a run requires specifying a dataset, featureset and a model against which this run is recored. A run records model parameters and model performance. The run object is probably most useful for the analysis of model performance with respect to a featureset, model hyper-parameters and a dataset.""" 

        rrid = ri["run_id"]
        mp = ri["model-params"]
        mp["_key"] = mp["run_id"]
        mperf = ri["model-perf"]
        mperf["_key"] = mperf["run_id"]
    
        
        run = self.emlg.vertex_collection("run")
        run_info = {"_key": rrid, \
                    "featureset": ri["featureset"],\
                    "dataset": ri["dataset"],\
                    "timestamp": mperf["timestamp"]}
        print(run_info)
        run.insert(run_info)
        
        model_param = self.emlg.vertex_collection("modelparams")
        model_param.insert(mp)
      
        run_fs_edge = self.emlg.edge_collection("run_featuresets")
        run_fs_key = rrid + "-" +  ri["featureset"]
        
        if not run_fs_edge.has(run_fs_key):
            edge_run_fs = {"_key": run_fs_key,\
                        "_from": "run/" + rrid,\
                        "_to": "featuresets/" +  ri["featureset"]}
            
            run_fs_edge.insert(edge_run_fs)
        
     
        
        run_mp_edge = self.emlg.edge_collection("run_modelparams")
        run_mp_key = rrid + "-" + mp["run_id"]
        
        if not run_mp_edge.has(run_mp_key):
            edge_run_mp = {"_key": run_mp_key,\
                        "_from": "run/" + rrid,\
                        "_to": "modelparams/" + mp["run_id"]}
            
            run_mp_edge.insert(edge_run_mp)
        
        model_perf = self.emlg.vertex_collection("modelperf")
        model_perf.insert(mperf)
        
        run_model_perf_edge = self.emlg.edge_collection("run_modelperf")
        run_model_perf_key = rrid + "-" + mperf["run_id"]
        
        if not run_model_perf_edge.has(run_model_perf_key):
            edge_run_model_perf = {"_key": run_model_perf_key,\
                        "_from": "run/" + rrid,\
                        "_to": "modelperf/" + mperf["run_id"]}
            run_model_perf_edge.insert(edge_run_model_perf)
            
        run_dataset_edge = self.emlg.edge_collection("run_datasets")
        run_dataset_key = rrid + "-" + ri["dataset"]
        
        if not run_dataset_edge.has(run_dataset_key):
            edge_run_dataset = {"_key": run_dataset_key,\
                        "_from": "run/" + rrid,\
                        "_to": "datasets/" + ri["dataset"]}
            run_dataset_edge.insert(edge_run_dataset)
            

        return
    
    
    
    
    
        

    
    
    