#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 11:48:43 2019

@author: admin2
"""

from arangopipe.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_config import ArangoPipeConfig
import datetime

def clean():
    admin = ArangoPipeAdmin()
    admin.delete_arangomldb()
    return

# A user with privileges can register a project with Arangopipe
def test_provision_project():
    proj_info = {"name": "Wine-Quality-Regression-Modelling"}
    admin = ArangoPipeAdmin()
    proj_reg = admin.register_project(proj_info)
    return 

# convinience method to test arangopipe install
def run_tests():
    try:
        clean()
        test_provision_project()
        test_dataset_registration()
        test_dataset_lookup()
        test_featureset_registration()
        test_featureset_lookup()
        test_model_registration()
        test_model_lookup()
        test_set_db_connection()
        test_log_run()
        test_provision_deployment()
        test_log_servingperf()

    except:
        print ("Failures encountered, exceptions occured")
        raise
    print("Arangopipe test cases verified, tests successfull!")
    return
    
 # This represents a data scientist with lower privileges - just set model hyper-parameters, executing a project.


# This user can register datasets, featuresets and models
def test_dataset_registration():
    ap = ArangoPipe()
    ds_info = {"name" : "wine dataset",\
                   "description": "Wine quality ratings","source": "UCI ML Repository" }
    
    ds_reg = ap.register_dataset(ds_info)
    return

def test_dataset_lookup():
    ap = ArangoPipe()
    ds_reg = ap.lookup_dataset("wine dataset")
    return

def test_featureset_lookup():
    ap = ArangoPipe()
    fs_reg = ap.lookup_featureset("wine_no_transformations")
    return 

def test_model_lookup():
    ap = ArangoPipe()
    model_reg = ap.lookup_model("elastic_net_wine_model")
    return
    
def test_featureset_registration():
    ap = ArangoPipe()
    fs_info = {"fixed acidity": "float64",\
               "volatile acidity": "float64",\
               "citric acid": "float64",\
               "residual sugar": "float64",\
               "chlorides": "float64",\
               "free sulfur dioxide": "float64",\
               "total sulfur dioxide": "float64",\
               "density": "float64",\
               "pH": "float64",\
               "sulphates": "float64",\
               "alcohol": "float64",\
               "quality": "int64",\
               "name": "wine_no_transformations"
               }
    ds_reg = ap.lookup_dataset("wine dataset")
    fs_reg = ap.register_featureset(fs_info, ds_reg["_key"])
    return

def test_log_run():
     ap = ArangoPipe()
     ds_reg = ap.lookup_dataset("wine dataset")
     fs_reg = ap.lookup_featureset("wine_no_transformations")
     model_reg = ap.lookup_model("elastic_net_wine_model")
     model_params = { "l1_ratio": 0.1, "alpha": 0.2,\
                     "run_id": "0ef73d9edf08487793c77a1742f4033e"}
     model_perf = { "rmse": 0.7836984021909766, "r2": 0.20673590971167466,\
                    "mae": 0.6142020452688988, "run_id": "0ef73d9edf08487793c77a1742f4033e",\
                    "timestamp": "2019-06-06 12:52:11.190048"}
     run_info = {"dataset" : ds_reg["_key"],\
                    "featureset": fs_reg["_key"],\
                    "run_id": "0ef73d9edf08487793c77a1742f4033e",\
                    "model": model_reg["_key"],\
                    "model-params": model_params,\
                    "model-perf": model_perf,\
                    "pipeline" : "Wine-Regression-Pipeline",\
                    "project": "Wine-Quality-Assessment",\
                    "deployment_tag": "Wine_Elastic_Net_Regression",\
                    "tag": "wine regression model test 1"}
     ap.log_run(run_info)
     return
     
     
def test_model_registration():
    ap = ArangoPipe()
    model_info = {"name": "elastic_net_wine_model",  "type": "elastic net regression"}
    model_reg = ap.register_model(model_info)
    return
    

# A user with prvileges can register a tagged deployment with Arangopipe by simply providing the deployment tag
def test_provision_deployment():
    admin = ArangoPipeAdmin()
    ret = admin.register_deployment("Wine_Elastic_Net_Regression")
    
    return
# A user with prvileges can log serving performance with Arangopipe
def test_log_servingperf():
    to_date = datetime.datetime.now()
    from_date = to_date - datetime.timedelta(days = 30)
    ex_servingperf = {"rmse": 0.822242, "r2": 0.12678, "mae": 0.62787,\
                      "from_date": str(from_date), "to_date": str(to_date)}
    dep_tag = "Wine_Elastic_Net_Regression"
    user_id = "prvileged user"
    ap = ArangoPipe()
    ret = ap.log_serving_perf(ex_servingperf, dep_tag, user_id)
    return ret

def test_set_db_connection():
    apc = ArangoPipeConfig()
    apc.set_dbconnection()
    ap = ArangoPipe(config = apc, persist = False)
    model_reg = ap.lookup_model("elastic_net_wine_model")
    return


    
    

    
    