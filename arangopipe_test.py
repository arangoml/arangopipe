#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 11:48:43 2019

@author: admin2
"""
import os
from arangopipe_admin import ArangoPipeAdmin
from arangopipe import ArangoPipe
import runpy
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

# convinience method to test both modes of pipeline execution
def test_exec_pipeline_modes():
    clean()
    test_provision_project()
    test_prvileged_ds_exec_mode()
    test_non_privileged_ds_exec_mode()
    return
    
 # This represents a data scientist with lower privileges - just set model hyper-parameters, executing a project.

def test_non_privileged_ds_exec_mode():
    os.chdir("/home/admin2/arangopipe/arangopipe_examples/sklearn_elasticnet_wine")
    ret = runpy.run_module("AP_Client_V1_Wine_Regression", run_name='__main__') 
    return
    
# This user can register datasets, featuresets and models
def test_prvileged_ds_exec_mode():
    os.chdir("/home/admin2/arangopipe/arangopipe_examples/sklearn_elasticnet_wine")
    # This represents a data scientist with privileges to register datasets, models and
    # feature sets executing a project
    ret1 = runpy.run_module("AP_Client_V2_Wine_Regression", run_name='__main__')
    return
# After a model has satisfactory performance, a DS can tag the model for deployment
def test_exec_tagging_model_for_deployment():
 
    os.chdir("/home/admin2/arangopipe/arangopipe_examples/sklearn_elasticnet_wine")
    # This represents a data scientist with privileges to register datasets, models and
    # feature sets executing a project
    ret1 = runpy.run_module("AP_Client_V3_Wine_Regression", run_name='__main__')

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
    
    

    
    