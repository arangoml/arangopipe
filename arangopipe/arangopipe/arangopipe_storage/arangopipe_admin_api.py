#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:30:33 2019

@author: Rajiv Sambasivan
"""

import logging
from typing import Optional

import requests

from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.managed_service_conn_parameters import (
    ManagedServiceConnParam,
)

# import traceback
# create logger with 'spam_application'
logger = logging.getLogger("arangopipe_admin_logger")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler("arangopipeadmin.log")
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class ArangoPipeAdmin:
    def __init__(
        self,
        db,
        graph_name,
        replication_factor: Optional[int] = None,
        reuse_connection: bool = False,
        create_graph: bool = True,
    ):
        if db is None:
            logger.error("A database object is required to initialize ArangoPipeAdmin")
            raise Exception("arango_db object parameter is missing")
        else:
            self.db = db

        self.graph_name = graph_name
        self.db_replication_factor = replication_factor
        self.create_graph = create_graph
        self.reuse_connection = reuse_connection

        # Provision the graph
        if self.create_graph:
            self.create_enterprise_ml_graph(self.db_replication_factor)

        return

    # def check_repeated_creation(self, api_data):
    #     if not api_data:
    #         repeated_connection = False
    #     else:
    #         try:
    #             user_name_equal = (
    #                 api_data[self.mscp.DB_USER_NAME]
    #                 == self.cfg["arangodb"][self.mscp.DB_USER_NAME]
    #             )
    #             password_equal = (
    #                 api_data[self.mscp.DB_PASSWORD]
    #                 == self.cfg["arangodb"][self.mscp.DB_PASSWORD]
    #             )
    #             db_name_equal = (
    #                 api_data[self.mscp.DB_NAME]
    #                 == self.cfg["arangodb"][self.mscp.DB_NAME]
    #             )
    #             repeated_connection = user_name_equal or password_equal or db_name_equal
    #             if user_name_equal:
    #                 logger.info(
    #                     "Attempting to create a connection with an existing username"
    #                 )
    #             if db_name_equal:
    #                 logger.info(
    #                     "Attempting to create a connection with an existing db name"
    #                 )
    #         except KeyError:
    #             repeated_connection = False

    #     return repeated_connection

    # def set_connection_params(self, config):
    #     self.cfg = config
    #     self.cfg.dump_data()
    #     return

    # def create_config(self):
    #     apc = ArangoPipeConfig()
    #     return apc

    # def get_config(self):
    #     return self.config

    def create_enterprise_ml_graph(self, db_replication_factor):

        cl = [
            "project",
            "models",
            "datasets",
            "featuresets",
            "modelparams",
            "run",
            "devperf",
            "servingperf",
            "deployment",
        ]

        if self.reuse_connection:
            self.emlg = self.db.graph(self.graph_name)
            return

        if not self.db.has_graph(self.graph_name):
            self.emlg = self.db.create_graph(self.graph_name)
        else:
            self.emlg = self.db.graph(self.graph_name)

        for col in cl:
            if not self.emlg.has_vertex_collection(col):
                self.db.create_collection(col, db_replication_factor)
                self.emlg.create_vertex_collection(col)

        from_list = [
            "project",
            "models",
            "run",
            "run",
            "run",
            "run",
            "deployment",
            "deployment",
            "deployment",
            "deployment",
            "featuresets",
        ]
        to_list = [
            "models",
            "run",
            "modelparams",
            "datasets",
            "devperf",
            "featuresets",
            "servingperf",
            "models",
            "modelparams",
            "featuresets",
            "datasets",
        ]
        edge_names = [
            "project_models",
            "run_models",
            "run_modelparams",
            "run_datasets",
            "run_devperf",
            "run_featuresets",
            "deployment_servingperf",
            "deployment_model",
            "deployment_modelparams",
            "deployment_featureset",
            "featureset_dataset",
        ]
        for edge, fromv, tov in zip(edge_names, from_list, to_list):
            if not self.db.has_collection(edge):
                self.db.create_collection(
                    edge, edge=True, replication_factor=db_replication_factor
                )
            if not self.emlg.has_edge_definition(edge):
                self.emlg.create_edge_definition(
                    edge_collection=edge,
                    from_vertex_collections=[fromv],
                    to_vertex_collections=[tov],
                )

        return

    def register_project(self, p):

        projects = self.emlg.vertex_collection("project")
        proj_reg = projects.insert(p)

        return proj_reg

    def delete_arangomldb(self):

        return

    def register_deployment(self, dep_tag):

        # Execute the query
        cursor = self.db.aql.execute(
            "FOR doc IN run FILTER doc.deployment_tag == @value RETURN doc",
            bind_vars={"value": dep_tag},
        )
        run_docs = [doc for doc in cursor]
        the_run_doc = run_docs[0]
        # Get the model params for the run
        rmpe = self.emlg.edge_collection("run_modelparams")
        edge_dict = rmpe.edges(the_run_doc, direction="out")
        tmp_id = edge_dict["edges"][0]["_to"]
        mpc = self.emlg.edge_collection("modelparams")
        tagged_model_params = mpc.get(tmp_id)
        # Get the model for the run
        rme = self.emlg.edge_collection("run_models")
        edge_dict = rme.edges(the_run_doc, direction="in")
        tm_id = edge_dict["edges"][0]["_from"]
        mc = self.emlg.edge_collection("models")
        tagged_model = mc.get(tm_id)
        # Get the featureset for the run
        rfse = self.emlg.edge_collection("run_featuresets")
        edge_dict = rfse.edges(the_run_doc, direction="out")
        tfid = edge_dict["edges"][0]["_to"]
        tfc = self.emlg.edge_collection("featuresets")
        tagged_featureset = tfc.get(tfid)
        # Create a deployment artifact
        deployment = self.emlg.vertex_collection("deployment")
        deploy_info = {"tag": dep_tag}
        dep_reg = deployment.insert(deploy_info)
        # Link the deployment to the model parameters
        dep_model_params_edge = self.emlg.edge_collection("deployment_modelparams")
        dep_model_params_key = dep_reg["_key"] + "-" + tagged_model_params["_key"]
        the_dep_model_param_edge = {
            "_key": dep_model_params_key,
            "_from": dep_reg["_id"],
            "_to": tagged_model_params["_id"],
        }

        dep_model_params_edge.insert(the_dep_model_param_edge)

        # Link the deployment to the featureset
        dep_featureset_edge = self.emlg.edge_collection("deployment_featureset")
        dep_featureset_key = dep_reg["_key"] + "-" + tagged_featureset["_key"]
        the_dep_featureset_edge = {
            "_key": dep_featureset_key,
            "_from": dep_reg["_id"],
            "_to": tagged_featureset["_id"],
        }
        dep_featureset_edge.insert(the_dep_featureset_edge)

        # Link the deployment to the model
        dep_model_edge = self.emlg.edge_collection("deployment_model")
        dep_featureset_key = dep_reg["_key"] + "-" + tagged_model["_key"]
        the_dep_model_edge = {
            "_key": dep_featureset_key,
            "_from": dep_reg["_id"],
            "_to": tagged_model["_id"],
        }

        dep_model_reg = dep_model_edge.insert(the_dep_model_edge)
        return dep_model_reg

    def add_vertex_to_arangopipe(self, vertex_to_create):
        rf = self.db_replication_factor

        if not self.db.has_graph(self.graph_name):
            self.emlg = self.db.create_graph(self.graph_name)
        else:
            self.emlg = self.db.graph(self.graph_name)

        # Check if vertex exists in the graph, if not create it
        if not self.emlg.has_vertex_collection(vertex_to_create):
            self.db.create_collection(vertex_to_create, rf)
            self.emlg.create_vertex_collection(vertex_to_create)
        else:
            logger.error("Vertex, " + vertex_to_create + " already exists!")

        return

    def remove_vertex_from_arangopipe(self, vertex_to_remove, purge=True):

        if not self.db.has_graph(self.graph_name):
            self.emlg = self.db.create_graph(self.graph_name)
        else:
            self.emlg = self.db.graph(self.graph_name)

        # Check if vertex exists in the graph, if not create it
        if self.emlg.has_vertex_collection(vertex_to_remove):
            self.emlg.delete_vertex_collection(vertex_to_remove, purge)

            logger.info("Vertex collection " + vertex_to_remove + " has been deleted!")
        else:
            logger.error("Vertex, " + vertex_to_remove + " does not exist!")

        return

    def add_edge_definition_to_arangopipe(
        self, edge_col_name, edge_name, from_vertex_name, to_vertex_name
    ):
        rf = self.db_replication_factor

        if not self.db.has_graph(self.graph_name):
            self.emlg = self.db.create_graph(self.graph_name)
        else:
            self.emlg = self.db.graph(self.graph_name)

        # Check if all data needed to create an edge exists, if so, create it

        if not self.emlg.has_vertex_collection(from_vertex_name):
            logger.error(
                "Source vertex, "
                + from_vertex_name
                + " does not exist, aborting edge creation!"
            )
            return
        elif not self.emlg.has_vertex_collection(to_vertex_name):
            logger.error(
                "Destination vertex, "
                + to_vertex_name
                + " does not exist, aborting edge creation!"
            )
            return

        else:
            if not self.emlg.has_edge_definition(edge_name):
                if not self.emlg.has_edge_collection(edge_col_name):
                    self.db.create_collection(
                        edge_col_name, edge=True, replication_factor=rf
                    )

                self.emlg.create_edge_definition(
                    edge_collection=edge_col_name,
                    from_vertex_collections=[from_vertex_name],
                    to_vertex_collections=[to_vertex_name],
                )
            else:
                logger.error("Edge, " + edge_name + " already exists!")

        return

    def add_edges_to_arangopipe(self, edge_col_name, from_vertex_list, to_vertex_list):
        rf = self.db_replication_factor

        if not self.db.has_graph(self.graph_name):
            self.emlg = self.db.create_graph(self.graph_name)
        else:
            self.emlg = self.db.graph(self.graph_name)

        # Check if all data needed to create an edge exists, if so, create it

        if not self.emlg.has_edge_collection(edge_col_name):
            msg = "Edge collection %s did not exist, creating it!" % (edge_col_name)
            logger.info(msg)
            self.db.create_collection(edge_col_name, edge=True, replication_factor=rf)

        self.emlg.create_edge_definition(
            edge_collection=edge_col_name,
            from_vertex_collections=from_vertex_list,
            to_vertex_collections=to_vertex_list,
        )

        return

    def remove_edge_definition_from_arangopipe(self, edge_name, purge=True):

        if not self.db.has_graph(self.graph_name):
            self.emlg = self.db.create_graph(self.graph_name)
        else:
            self.emlg = self.db.graph(self.graph_name)

        if self.emlg.has_edge_definition(edge_name):
            self.emlg.delete_edge_definition(edge_name, purge)

        else:
            logger.error("Edge definition " + edge_name + " does not exist!")

        return

    def has_vertex(self, vertex_name):

        if not self.db.has_graph(self.graph_name):
            self.emlg = self.db.create_graph(self.graph_name)
        else:
            self.emlg = self.db.graph(self.graph_name)

        result = self.emlg.has_vertex_collection(vertex_name)
        return result

    def has_edge(self, edge_name):

        if not self.db.has_graph(self.graph_name):
            self.emlg = self.db.create_graph(self.graph_name)
        else:
            self.emlg = self.db.graph(self.graph_name)

        result = self.emlg.has_edge_definition(edge_name)

        return result
