#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 17:06:54 2019

@author: admin2
"""

from abc import ABC

class DatasetShiftDetector(ABC):
    
    def detect_dataset_shift(dataframe1, dataframe2):
        pass
    
    def detect_covariate_shift(dataframe1, dataframe2):
        pass