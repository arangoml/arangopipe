#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:17:50 2019

@author: Rajiv Sambasivan
"""
import os

import yaml
from arangopipe.arangopipe_storage.managed_service_conn_parameters import ManagedServiceConnParam


class ArangoPipeConfig:
    def __init__(self):
        self.cfg = None
        self.mscp = ManagedServiceConnParam()

    def read_data(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "arangopipe_config.yaml")
        with open(file_name, "r") as file_descriptor:
            cfg = yaml.load(file_descriptor, Loader=yaml.FullLoader)
        return cfg

    def set_cfg(self, new_cfg):
        self.cfg = new_cfg

    def get_cfg(self):
        if self.cfg is None:
            self.cfg = self.read_data()
        return self.cfg

    def dump_data(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "arangopipe_config.yaml")
        with open(file_name, "w") as file_descriptor:
            cfg = yaml.dump(self.cfg, file_descriptor)
        return cfg

    def create_connection_config(self, conn_params):
        self.cfg = {
            'arangodb': {},
            'mlgraph': {
                'graphname': 'enterprise_ml_graph'
            }
        }
        for key, value in conn_params.items():
            self.cfg['arangodb'][key] = value
        return self
