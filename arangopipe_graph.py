#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:57:15 2019

@author: admin2
"""

from graphviz import Digraph

def create_arangopipe_schema():
    dot = Digraph(comment='Enterpise ML Model Tracker Generator')
    dot.node('A', 'Enterprise ML Tracker Graph')
    dot.node('B', 'Projects')
    dot.node('C', 'Model')
    dot.node('D', 'Run')
    dot.node('E', 'Dataset')
    dot.node('F', 'Model Parameters')
    dot.node('G', 'Dev Performance')
    dot.node('H', 'App. Admin')
    dot.node('I', "Feature Set")
    dot.node('J', 'Serving Performance')
    dot.node('K', 'Deployment')
    
    #dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'EG', 'EH'])
    dot.edge('A', 'B', label = "has many")
    dot.edge('B', 'C', label = "has many")
    dot.edge('C', 'D', label = "execution")
    dot.edge('C', 'E', label = "built with ")
    dot.edge('E', 'I', label = "transformed to")
    dot.edge('D', 'F', label = "produces ")
    dot.edge('D', 'G', label = "produces")
    dot.edge('H', 'A', label = "provisions")
    dot.edge('H', 'B', label = "creates")
    dot.edge('K', 'C', label = "tagged with")
    dot.edge('K', 'I', label = "tagged with")
    dot.edge('K', 'F', label = "tagged with")
    dot.edge('K', 'J', label = "produces")
    print(dot.source)
    dot.render('graph_schema/arangopipe_schema.gv', view=True)
    
    return    