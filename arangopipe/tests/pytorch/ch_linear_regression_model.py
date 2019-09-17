#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 09:16:24 2019

@author: Rajiv Sambasivan
"""

import torch


class CH_LinearRegression(torch.nn.Module):
    def __init__(self, inputSize, outputSize):
        super(CH_LinearRegression, self).__init__()
        self.linear = torch.nn.Linear(inputSize, outputSize)

    def forward(self, x):
        out = self.linear(x)
        return out

