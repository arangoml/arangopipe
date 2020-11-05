#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 15:16:13 2019

@author: Rajiv Sambasivan
"""
import unittest
from arangopipe.arangopipe_storage.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
import datetime
from arangopipe.arangopipe_analytics.rf_dataset_shift_detector import RF_DatasetShiftDetector
import os
import pandas as pd
import sys
import traceback
from arangopipe.arangopipe_storage.managed_service_conn_parameters import ManagedServiceConnParam
import yaml
from arangopipe.arangopipe_storage.connection_manager import arango_pipe_connections

class TestArangopipe(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TestArangopipe, self).__init__(*args, **kwargs)
        self.test_cfg = self.get_test_config()
        
        return
    
    def setUp(self):
        #mshost: "5366b66b7d19.arangodb.cloud"
        config = ArangoPipeConfig()
        msc = ManagedServiceConnParam()
        conn_params = { msc.DB_SERVICE_HOST : self.test_cfg['arangodb'][msc.DB_SERVICE_HOST], \
                        msc.DB_SERVICE_END_POINT : self.test_cfg['arangodb'][msc.DB_SERVICE_END_POINT],\
                        msc.DB_SERVICE_NAME : self.test_cfg['arangodb'][msc.DB_SERVICE_NAME],\
                        msc.DB_SERVICE_PORT : self.test_cfg['arangodb'][msc.DB_SERVICE_PORT],\
                        msc.DB_CONN_PROTOCOL : self.test_cfg['arangodb'][msc.DB_CONN_PROTOCOL],\
                        msc.DB_NOTIFICATION_EMAIL : 'somebody@some_company.com'}
        
        config = config.create_connection_config(conn_params)
        self.config = config
        self.admin = ArangoPipeAdmin(reuse_connection = False,\
                                     config= self.config, persist_conn= False)
        ap_config = self.admin.get_config()
        self.ap = ArangoPipe(config = ap_config)
        self.provision_project()
        return
    
    def get_test_config(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                     "../test_config/test_datagen_config.yaml")
        with open(file_name, "r") as file_descriptor:
            test_cfg = yaml.load(file_descriptor, Loader=yaml.FullLoader)
        
        return test_cfg
    
    def provision_project(self):
        err_raised = False
        try:
            proj_info = {"name": "Wine-Quality-Regression-Modelling"}
            proj_reg = self.admin.register_project(proj_info)
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while provisioning project')

        #cls.assertFalse(err_raised, )
        return
    
    def register_dataset(self):
        ds_info = {"name": "wine_dataset",
                   "description": "Wine quality ratings",
                   "source": "UCI ML Repository"}
        ds_reg = self.ap.register_dataset(ds_info)
        return

    def lookup_dataset(self):
        ds_reg = self.ap.lookup_dataset("wine_dataset")
        return

    def lookup_featureset(self):
        fs_reg = self.ap.lookup_featureset("wine_no_transformations")
        return

    def register_model(self):

        model_info = {"name": "elastic_net_wine_model",
                      "type": "elastic net regression"}
        model_reg = self.ap.register_model(model_info)
        return
    
    def link_models(self):

        model_info1 = {"name": "elastic_net_wine_model1",
                      "type": "elastic net regression1"}
        model_reg1 = self.ap.register_model(model_info1)
        
        model_info2 = {"name": "elastic_net_wine_model2",
                      "type": "elastic net regression2"}
        model_reg2 = self.ap.register_model(model_info2)
        
        model_info3 = {"name": "elastic_net_wine_model3",
                      "type": "elastic net regression3"}
        model_reg3 = self.ap.register_model(model_info3)
        
        self.ap.link_entities(model_reg1['_id'], model_reg2['_id'])
        updated_model_info = self.ap.lookup_model(model_info1["name"])
        print("Updated model:")
        print(updated_model_info)
        print("Adding another model link")
        self.ap.link_entities(model_reg1['_id'], model_reg3['_id'])
        updated_model_info = self.ap.lookup_model(model_info1["name"])
        print("Updated model:")
        print(updated_model_info)
        added_str = updated_model_info['related_models']
        added_links = added_str.split(",")
        link_added = len(added_links) == 2
        self.assertTrue(link_added,
                            'Exception raised while linking models')
        
        
        return

    def lookup_model(self):

        model_reg = self.ap.lookup_model("elastic_net_wine_model")
        return

    def log_run(self):

        ds_reg = self.ap.lookup_dataset("wine_dataset")
        fs_reg = self.ap.lookup_featureset("wine_no_transformations")
        model_reg = self.ap.lookup_model("elastic_net_wine_model")
        model_params = {"l1_ratio": 0.1, "alpha": 0.2,
                        "run_id": "0ef73d9edf08487793c77a1742f4033e"}
        model_perf = {"rmse": 0.7836984021909766, "r2": 0.20673590971167466,
                      "mae": 0.6142020452688988, "run_id": "0ef73d9edf08487793c77a1742f4033e",
                      "timestamp": "2019-06-06 12:52:11.190048"}
        run_info = {"dataset": ds_reg["_key"],
                    "featureset": fs_reg["_key"],
                    "run_id": "0ef73d9edf08487793c77a1742f4033e",
                    "model": model_reg["_key"],
                    "model-params": model_params,
                    "model-perf": model_perf,
                    "pipeline": "Wine-Regression-Pipeline",
                    "project": "Wine-Quality-Assessment",
                    "deployment_tag": "Wine_Elastic_Net_Regression",
                    "tag": "wine regression model test 1"}
        self.ap.log_run(run_info)
        return

    def provision_deployment(self):

        ret = self.admin.register_deployment("Wine_Elastic_Net_Regression")

        return

    def register_featureset(self):

        fs_info = {"fixed acidity": "float64",
                   "volatile acidity": "float64",
                   "citric acid": "float64",
                   "residual sugar": "float64",
                   "chlorides": "float64",
                   "free sulfur dioxide": "float64",
                   "total sulfur dioxide": "float64",
                   "density": "float64",
                   "pH": "float64",
                   "sulphates": "float64",
                   "alcohol": "float64",
                   "quality": "int64",
                   "name": "wine_no_transformations"
                   }
        ds_reg = self.ap.lookup_dataset("wine_dataset")
        fs_reg = self.ap.register_featureset(fs_info, ds_reg["_key"])
        return

    def log_servingperf(self):
        to_date = datetime.datetime.now()
        from_date = to_date - datetime.timedelta(days=30)
        ex_servingperf = {"rmse": 0.822242, "r2": 0.12678, "mae": 0.62787,
                          "from_date": str(from_date), "to_date": str(to_date)}
        dep_tag = "Wine_Elastic_Net_Regression"
        user_id = "prvileged user"
        ret = self.ap.log_serving_perf(ex_servingperf, dep_tag, user_id)

        return

    def dataset_shift_positive(self):
        ds_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "cal_housing.csv")
        df = pd.read_csv(ds_path)
        req_cols = df.columns.tolist()
        df = df[req_cols]
        df1 = df.query("lat <= -119")
        df2 = df.query("lat > -119")
        rfd = RF_DatasetShiftDetector()
        score = rfd.detect_dataset_shift(df1, df2)
        print("Detaset shift score : ", score)

        return score

    def dataset_shift_negative(self):
        ds_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "cal_housing.csv")
        df = pd.read_csv(ds_path)
        req_cols = df.columns.tolist()
        df = df[req_cols]
        df1 = df.query("lat <= -119")
        df2 = df1.copy()
        rfd = RF_DatasetShiftDetector()
        score = rfd.detect_dataset_shift(df1, df2)
        print("Detaset shift score : ", score)

        return score

    def vertex_add_to_arangopipe(self):
        self.admin.add_vertex_to_arangopipe('test_vertex_1')

        return

    def test_arangopipe_vertex_add(self):
        self.vertex_add_to_arangopipe()
        self.assertTrue(self.admin.has_vertex('test_vertex_1'))

        return

    def vertex_remove_from_arangopipe(self):
        self.admin.add_vertex_to_arangopipe('test_vertex_t1')
        self.admin.remove_vertex_from_arangopipe('test_vertex_t1', purge=True)

        return

    def test_arangopipe_vertex_remove(self):
        self.vertex_remove_from_arangopipe()
        self.assertFalse(self.admin.has_vertex('test_vertex_t1'))

        return

    def test_register_dataset(self):
        err_raised = False
        try:
            self.register_dataset()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while registering dataset')
        self.assertFalse(err_raised)
        return
    def test_reregister_dataset(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_dataset()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while registering dataset')
        self.assertFalse(err_raised)
        return

    def test_lookup_dataset(self):
        err_raised = False
        try:
            self.register_dataset()
            self.lookup_dataset()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while looking up dataset')
        self.assertFalse(err_raised)
        return

    def test_register_featureset(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while registering featureset')
        self.assertFalse(err_raised)
        return
    
    def test_reregister_featureset(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
            self.register_featureset()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while registering featureset')
        self.assertFalse(err_raised)
        return

    def test_lookup_featureset(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
            self.lookup_featureset()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while registering featureset')
        self.assertFalse(err_raised)
        return

    def test_register_model(self):
        err_raised = False
        try:
            self.register_model()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while registering model')
        self.assertFalse(err_raised)
        return
    
    def test_reregister_model(self):
        err_raised = False
        try:
            self.register_model()
            self.register_model()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while registering model')
        self.assertFalse(err_raised)
        return

    def test_lookup_model(self):
        err_raised = False
        try:
            self.register_model()
            self.lookup_model()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while looking up model')
        self.assertFalse(err_raised)
        return

    def test_log_run(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
            self.register_model()
            self.log_run()
        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while logging performance')
        self.assertFalse(err_raised)
        return

    def test_link_models(self):
        err_raised = False
        try:
            self.link_models()
 

        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while provisioning deployment')
        self.assertFalse(err_raised)
        
    def test_provision_deployment(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
            self.register_model()
            self.log_run()
            self.provision_deployment()

        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while provisioning deployment')
        self.assertFalse(err_raised)
        return

    def test_log_serving_performance(self):
        err_raised = False
        try:
            self.register_dataset()
            self.register_featureset()
            self.register_model()
            self.log_run()
            self.provision_deployment()
            self.log_servingperf()

        except:
            err_raised = True
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            self.assertTrue(err_raised,
                            'Exception raised while logging serving performance')
        self.assertFalse(err_raised)
        return

    def test_dataset_shift_positive(self):

        score = self.dataset_shift_positive()

        self.assertTrue(score > 0.8)
        return

    def test_dataset_shift_negative(self):

        score = self.dataset_shift_negative()

        self.assertTrue(score < 0.6)
        return

    def add_edge_to_arangopipe(self):
        self.admin.add_vertex_to_arangopipe('test_vertex_s')
        self.admin.add_vertex_to_arangopipe('test_vertex_d')
        self.admin.add_edge_definition_to_arangopipe('test_edge_col', 'test_edge',
                                                     'test_vertex_s', 'test_vertex_d')
        return

    def test_arangopipe_edge_add(self):
        self.add_edge_to_arangopipe()
        self.assertTrue(self.admin.has_edge('test_edge_col'))

        return

    def remove_edge_from_arangopipe(self):
        self.admin.add_vertex_to_arangopipe('test_vertex_s1')
        self.admin.add_vertex_to_arangopipe('test_vertex_d1')
        self.admin.add_edge_definition_to_arangopipe('test_edge_col', 'test_edge_1',
                                                     'test_vertex_s1', 'test_vertex_d1')
        self.admin.remove_edge_definition_from_arangopipe(
            'test_edge_1', purge=True)

        return

    def test_arangopipe_edge_remove(self):
        self.remove_edge_from_arangopipe()
        self.assertFalse(self.admin.has_edge('test_edge_1'))

        return

    def add_vertex_node(self):
        ni = None
        self.admin.add_vertex_to_arangopipe('test_vertex_s2')
        sd = {'name': "sample doc"}
        ni = self.ap.insert_into_vertex_type('test_vertex_s2', sd)

        return ni

    def test_arangopipe_vertex_node_add(self):
        ni = self.add_vertex_node()
        self.assertIsNotNone(ni)
        return

    def add_edge_link(self):
        ei = None
        self.admin.add_vertex_to_arangopipe('test_vertex_s3')
        self.admin.add_vertex_to_arangopipe('test_vertex_s4')
        sd = {'name': "sample doc"}
        v1 = self.ap.insert_into_vertex_type('test_vertex_s3', sd)
        v2 = self.ap.insert_into_vertex_type('test_vertex_s4', sd)
        self.admin.add_edge_definition_to_arangopipe('test_edge_col', 'test_edge',
                                                     'test_vertex_s3', 'test_vertex_s4')
        ei = self.ap.insert_into_edge_type('test_edge_col', v1, v2)

        return ei

    def test_arangopipe_edge_link_add(self):
        ei = self.add_edge_link()
        self.assertIsNotNone(ei)
        return
    
    def test_export(self):
        file_path = '/tmp/arangopipe_config.yaml'
        self.config.export_cfg(file_path)
        file_exists = os.path.exists(file_path)
        self.assertTrue(file_exists)
        
        return
    
    def test_import(self):
        file_path = '/tmp/arangopipe_config.yaml'
        self.config.export_cfg(file_path)
        cc = self.config.create_config(file_path)
        self.assertTrue(len(cc) > 0)
        
        return
    
    def test_connection_manager(self):
        msc = ManagedServiceConnParam()
        conn_params = { msc.DB_SERVICE_HOST : "arangoml.arangodb.cloud", \
                        msc.DB_SERVICE_END_POINT : "createDB",\
                        msc.DB_SERVICE_NAME : "createDB",\
                        msc.DB_SERVICE_PORT : 8529,\
                        msc.DB_CONN_PROTOCOL : 'https'}
        
        
        with arango_pipe_connections(conn_params, False) as (ap_admin, ap):
             proj_info = {"name": "Python With Generator Admin test"}
             proj_reg = ap_admin.register_project(proj_info)
             print("Done with test!")
        
        return


if __name__ == '__main__':
    unittest.main()
