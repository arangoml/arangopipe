#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:17:50 2019

@author: admin2
"""
import os

import yaml

class ArangoPipeConfig:
    def __init__(self):
        self.cfg = self.read_data()
    
    def read_data(self):
        file_name = os.path.join(os.path.dirname(__file__), "arangopipe_config.yaml")
        with open(file_name, "r") as file_descriptor:
            cfg = yaml.load(file_descriptor, Loader=yaml.FullLoader)
        return cfg
    
    def set_cfg(self, new_cfg):
        self.cfg = new_cfg
        
    
    def get_cfg(self):
        return self.cfg
    
    def dump_data(self):
        file_name = os.path.join(os.path.dirname(__file__), "arangopipe_config.yaml")
        with open(file_name, "w") as file_descriptor:
            cfg = yaml.dump(self.cfg, file_descriptor)
        return cfg
    
    def set_dbconnection(self, hostname = "localhost", port = 8529,\
                         root_user = 'root', \
                         root_user_password = 'open sesame',\
                         arangopipe_dbname = "arangopipe"):
        self.cfg['arangodb']['root_user'] = root_user
        self.cfg['arangodb']['root_user_password'] = root_user_password
        self.cfg['arangodb']['host'] = hostname
        self.cfg['arangodb']['port'] = port
        self.cfg['arangodb']['arangopipe_dbname'] = arangopipe_dbname
        return
      
        
