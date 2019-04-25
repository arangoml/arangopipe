#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 11:48:43 2019

@author: admin2
"""

from arangopipe_admin import ArangoPipeAdmin


def clean():
    admin = ArangoPipeAdmin()
    admin.delete_arangomldb()
    return

def provision_pipeline():
    proj_info = {"name": "Wine-Quality-Regression-Modelling"}
    pipeline_info = {"name": "Wine-Regression-Pipeline"}

    admin = ArangoPipeAdmin()
    proj_reg = admin.register_project(proj_info)
    pipeline_reg = admin.register_pipeline(pipeline_info)
    proj_ppl_reg = admin.register_project_pipeline (proj_reg, pipeline_reg)


    return 


    
    