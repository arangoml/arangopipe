#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 08:35:58 2019

@author: Rajiv Sambasivan
"""

from arango import ArangoClient, AQLQueryExecuteError
import logging
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.managed_service_conn_parameters import ManagedServiceConnParam

# create logger with 'spam_application'
logger = logging.getLogger('arangopipe_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('arangopipe.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class ArangoPipe:
    """ An instance of ArangoPipe is meant to be used to log a run of a pipeline execution. To use it:
        (1) Create a ArangoPipe object
        (2) Register your dataset with ArangoPipe
        (3) Register your featureset with ArangoPipe
        (4) Register you model with ArangoPipe
"""

    def __init__(self, config):
        self.cfg = config.get_cfg()
        self.emlg = None
        self.db = None
        self.mscp = ManagedServiceConnParam()
        self.init_graph()
        self.heart_beat()

    def heart_beat(self):
        try:
            self.lookup_dataset("heart beat check")
        except AQLQueryExecuteError as e:
            print("WARNING : " + str(e))
            logger.error(
                "Your database was perhaps deleted, try a new connection")
            # logger.error("Error: " + str(e))
            raise Exception("Your connection is stale, try a new connection!")

        return

    def get_config(self):
        apc = ArangoPipeConfig()
        return apc.get_cfg()

    def get_collection_from_id(self, id_str):
        sep = "/"
        tokens = id_str.split(sep)
        col_name = tokens[0]

        return col_name

    def is_valid_id_str(self, id_str):
        valid_id_str = False
        sep = "/"
        tokens = id_str.split(sep)

        valid_id_str = True if len(tokens) == 2 else False

        return valid_id_str

    def link_entities(self, src_id, dest_id):
        src_id_valid = self.is_valid_id_str(src_id)
        dest_id_valid = self.is_valid_id_str(dest_id)

        if not src_id_valid:
            logger.error("The source node key does appear to be valid")
            return
        if not dest_id_valid:
            logger.error("The destination key does not appear to be valid")
            return

        dest_entity_type = self.get_collection_from_id(dest_id)
        src_entity_type = self.get_collection_from_id(src_id)
        related_key = "related_" + dest_entity_type
        concat_key = 'doc.' + related_key
        aql_str = 'FOR doc in %s FILTER doc._id == @value UPDATE doc WITH {\
  %s: CONCAT_SEPARATOR(",", %s, @dest_entity) } IN %s' % (
            src_entity_type, related_key, concat_key, src_entity_type)

        cursor = self.db.aql.execute(aql_str,
                                     bind_vars={
                                         'value': src_id,
                                         'dest_entity': dest_id
                                     })

        return

    def lookup_entity_by_id(self, entity_id):
        entity_col = self.get_collection_from_id(entity_id)
        aql = 'FOR doc in %s FILTER doc._id == @value RETURN doc' % (
            entity_col)
        # Execute the query
        cursor = self.db.aql.execute(aql, bind_vars={'value': entity_id})
        asset_keys = [doc for doc in cursor]

        asset_info = None
        if len(asset_keys) == 0:
            logger.info("The asset by name: " + asset_name + \
                        " was not found in Arangopipe!")
        else:
            asset_info = asset_keys[0]

        return asset_info

    def lookup_entity(self, asset_name, asset_type):
        aql = 'FOR doc IN %s FILTER doc.name == @value RETURN doc' % (
            asset_type)
        # Execute the query
        cursor = self.db.aql.execute(aql, bind_vars={'value': asset_name})
        asset_keys = [doc for doc in cursor]

        asset_info = None
        if len(asset_keys) == 0:
            logger.info("The asset by name: " + asset_name + \
                        " was not found in Arangopipe!")
        else:
            asset_info = asset_keys[0]

        return asset_info

    def find_entity(self, attrib_name, attrib_value, asset_type):
        aql = 'FOR doc IN %s FILTER doc.%s == @value RETURN doc' % (
            asset_type, attrib_name)
        # Execute the query
        cursor = self.db.aql.execute(aql, bind_vars={'value': attrib_value})
        asset_keys = [doc for doc in cursor]

        asset_info = None
        if len(asset_keys) == 0:
            msg = "Asset %s with %s = %s was not found!" % (
                asset_type, attrib_name, attrib_value)
            logger.info(msg)
        else:
            asset_info = asset_keys

        return asset_info

    def lookup_dataset(self, dataset_name):
        """ Return a dataset identifier given a name. This can be used to get the dataset id that is used to log run information associated with execution of the pipeline."""

        dataset_info = self.lookup_entity(dataset_name, 'datasets')

        return dataset_info

    def lookup_featureset(self, feature_set_name):
        """ Return a featureset identifier given a name. This can be used to get the featureset id that is used to log run information associated with execution of the pipeline."""

        featureset_info = self.lookup_entity(feature_set_name, 'featuresets')

        return featureset_info

    def lookup_model(self, model_name):
        """ Return a model identifier given a name. This can be used to get the model id that is used to log run information associated with execution of the pipeline."""

        model_info = self.lookup_entity(model_name, 'models')

        return model_info

    def lookup_modelparams(self, tag_value):
        """ Return a model parameter result given a tag."""

        # Execute the query
        cursor = self.db.aql.execute('WITH modelparams\
                                     FOR r IN run\
                    FILTER r.tag == @value \
                        FOR mp IN 1..1 OUTBOUND r run_modelparams\
                            RETURN mp ',
                                     bind_vars={'value': tag_value})
        mp_info = None
        mp_keys = [doc for doc in cursor]
        if len(mp_keys) == 0:
            logger.info("The model params for tag: " + tag_value + \
                        " was not found in Arangopipe!")
        else:
            mp_info = mp_keys[0]
        return mp_info

    def lookup_modelperf(self, tag_value):
        """ Return a model dev performance given a tag."""

        # Execute the query
        cursor = self.db.aql.execute('WITH devperf\
                                     FOR r IN run\
                    FILTER r.tag == @value \
                        FOR dp IN 1..1 OUTBOUND r run_devperf\
                            RETURN dp ',
                                     bind_vars={'value': tag_value})
        mperf_info = None
        mperf_keys = [doc for doc in cursor]
        if len(mperf_keys) == 0:
            logger.info("The model performance for tag: " + tag_value + \
                        " was not found in Arangopipe!")
        else:
            mperf_info = mperf_keys[0]

        return mperf_info

    def init_graph(self):
        """ Initialize a graph when an instance of ArangoPipe is provisioned. """
        db_serv_host = self.cfg['arangodb']['DB_service_host']
        db_serv_port = self.cfg['arangodb']['DB_service_port']
        db_name = self.cfg['arangodb']['dbName']
        db_user_name = self.cfg['arangodb']['username']
        db_passwd = self.cfg['arangodb']['password']
        db_conn_protocol = self.cfg['arangodb'][self.mscp.DB_CONN_PROTOCOL]

        host_conn_str = db_conn_protocol + "://" + \
                        db_serv_host + ":" + str(db_serv_port)
        client = ArangoClient(hosts=host_conn_str)

        self.db = client.db(name=db_name, \
                            username=db_user_name, \
                            password=db_passwd, verify=True)

        self.emlg = self.db.graph(self.cfg['mlgraph']['graphname'])

        return

    def register_model(self, mi, user_id="authorized_user", project="Wine-Quality-Regression-Modelling"):
        """ Register a model. The operation requires specifying a user id. If the user id is permitted to register a
        model, then the registration proceeds, otherwise an unauthorized operation is indicated. """

        model_name = mi["name"]
        try:
            existing_model = self.lookup_model(model_name)
        except AQLQueryExecuteError as e:
            msg = "The model name %s is not taken" % (model_name)
            logger.info(msg)
        if existing_model is not None:
            msg = "It looks like the model name %s is already taken, try another name" % (
                model_name)
            logger.error(msg)
            return None
        models = self.emlg.vertex_collection("models")
        model_reg = models.insert(mi)

        # Execute the query
        cursor = self.db.aql.execute(
            'FOR doc IN project FILTER doc.name == @value RETURN doc',
            bind_vars={'value': project})
        project_keys = [doc for doc in cursor]
        the_project_info = project_keys[0]

        project_model_edge = self.emlg.edge_collection("project_models")
        project_model_key = the_project_info["_key"] + "-" + model_reg["_key"]

        a_project_model_edge = {"_key": project_model_key, \
                                "_from": "project/" + the_project_info["_key"], \
                                "_to": "models/" + model_reg["_key"]}
        pm_reg = project_model_edge.insert(a_project_model_edge)
        logger.info("Recording project model link " + str(pm_reg))

        return model_reg

    def register_dataset(self, ds_info, user_id="authorized_user"):
        """ Register a dataset. The operation requires specifying a user id. If the user id is permitted to register
        a dataset, then the registration proceeds, otherwise an unauthorized operation is indicated. """

        ds_name = ds_info["name"]
        try:
            existing_ds = self.lookup_dataset(ds_name)
        except AQLQueryExecuteError as e:
            msg = "The dataset name %s is not taken" % (ds_name)
            logger.info(msg)
        if existing_ds is not None:
            msg = "It looks like the dataset name %s is already taken, try another name" % (
                ds_name)
            logger.error(msg)
            return None
        ds = self.emlg.vertex_collection("datasets")
        ds_reg = ds.insert(ds_info)
        logger.info("Recording dataset dataset link " + str(ds_reg))

        return ds_reg

    def register_featureset(self, fs_info, dataset_id, user_id="authorized_user"):
        """ Register a featureset. ManagedServiceConnParamThe operation requires specifying a user id. If the user id
        is permitted to register a featureset, then the registration proceeds, otherwise an unauthorized operation is
        indicated. """
        fs_name = fs_info["name"]
        try:
            existing_fs = self.lookup_featureset(fs_name)
        except AQLQueryExecuteError as e:
            msg = "The featureset name %s is not taken" % (fs_name)
            logger.info(msg)
        if existing_fs is not None:
            msg = "It looks like the featureset name %s is already taken, try another name" % (
                fs_name)
            logger.error(msg)
            return None

        fs = self.emlg.vertex_collection("featuresets")
        fs_reg = fs.insert(fs_info)
        logger.info("Recording featureset " + str(fs_reg))
        featureset_dataset_edge = self.emlg.edge_collection(
            "featureset_dataset")
        featureset_dataset_key = fs_reg["_key"] + "-" + dataset_id

        a_featureset_dataset_edge = {"_key": featureset_dataset_key, \
                                     "_from": "featuresets/" + fs_reg["_key"], \
                                     "_to": "datasets/" + dataset_id}
        fsds_reg = featureset_dataset_edge.insert(a_featureset_dataset_edge)
        logger.info("Recording featureset dataset link " + str(fsds_reg))

        return fs_reg

    def log_run(self, ri):
        """ Log a run. Logging a run requires specifying a dataset, featureset and a model against which this run is
        recored. A run records model parameters and model performance. The run object is probably most useful for the
        analysis of model performance with respect to a featureset, model hyper-parameters and a dataset. """

        rrid = ri["run_id"]
        mp = ri["model-params"]
        mp["_key"] = mp["run_id"]
        mperf = ri["model-perf"]
        mperf["_key"] = mperf["run_id"]
        model_key = ri["model"]

        run_info_adds = {"_key": rrid, "timestamp": mperf["timestamp"]}
        default_params = ["dataset", "featureset", "model", "run_id", "model-params", "model-perf", "tag", "project",
                          "deployment_tag"]
        default_run_params = ["run_id", "deployment_tag"]

        for key in ri:
            if key in default_params:
                if key in default_run_params:
                    run_info_adds[key] = ri[key]
            else:
                run_info_adds[key] = ri[key]

        run = self.emlg.vertex_collection("run")
        # collection type
        logger.info("Run info " + str(run_info_adds))
        # logger
        run_reg = run.insert(run_info_adds)
        # insert dict into collection type
        logger.info("Recording run " + str(run_reg))
        # logger

        run_model_key = run_reg["_key"] + "-" + model_key
        # key gen
        a_run_model_edge = {"_key": run_model_key, "_from": "models/" + model_key, "_to": "run/" + rrid}
        # dict creation
        run_model_edge = self.emlg.edge_collection("run_models")
        # collection type
        rme_reg = run_model_edge.insert(a_run_model_edge)
        # insert dict into collection
        logger.info("Recording model run link " + str(rme_reg))
        # logger

        model_param = self.emlg.vertex_collection("modelparams")
        # get collection
        mp_reg = model_param.insert(mp)
        # insert dict into collection
        logger.info("Recording model params " + str(mp_reg))
        # logger

        run_fs_edge = self.emlg.edge_collection("run_featuresets")
        # get colletion
        run_fs_key = rrid + "-" + ri["featureset"]
        # gen key
        a_edge_run_fs = {"_key": run_fs_key, "_from": "run/" + rrid, "_to": "featuresets/" + ri["featureset"]}
        # dict gen
        rfse_reg = run_fs_edge.insert(a_edge_run_fs)
        # insert dict into collection
        logger.info("Recording run featureset link " + str(rfse_reg))
        # logger

        run_mp_edge = self.emlg.edge_collection("run_modelparams")
        # get collection
        run_mp_key = rrid + "-" + mp["run_id"]
        # key gen
        a_run_mp_edge = {"_key": run_mp_key, "_from": "run/" + rrid, "_to": "modelparams/" + mp_reg["_key"]}
        # dict creation
        rmp_reg = run_mp_edge.insert(a_run_mp_edge)
        # insert into collection
        logger.info("Recording run model params " + str(rmp_reg))
        # logger

        model_perf = self.emlg.vertex_collection("devperf")
        # get collection
        dp_reg = model_perf.insert(mperf)
        # insert into collection
        logger.info("Recording model dev performance  " + str(dp_reg))
        # logger

        run_devperf_edge = self.emlg.edge_collection("run_devperf")
        # get collection
        run_devperf_key = rrid + "-" + dp_reg["_key"]
        # key gen
        a_run_devperfedge = {"_key": run_devperf_key, "_from": "run/" + rrid, "_to": "devperf/" + dp_reg["_key"]}
        # dict gen
        rdp_reg = run_devperf_edge.insert(a_run_devperfedge)
        # insert into collection
        logger.info("Recording run dev perf link " + str(rdp_reg))
        # logger

        run_dataset_edge = self.emlg.edge_collection("run_datasets")
        # get collection
        run_dataset_key = rrid + "-" + ri["dataset"]
        # key gen
        a_run_dataset_edge = {"_key": run_dataset_key, "_from": "run/" + rrid, "_to": "datasets/" + ri["dataset"]}
        # dict gen
        rds_reg = run_dataset_edge.insert(a_run_dataset_edge)
        # insert into collection
        logger.info("Recording run dev perf link " + str(rds_reg))
        # logger
        return

    def log_serving_perf(self, sp, dep_tag, userid="authorized user"):
        """ Log serving performance against a deployed model. The user making the request needs to be authorized to log this performance update. A serving performance vertex is created and is linked with its deployment vertex"""
        servingperf = self.emlg.vertex_collection("servingperf")
        sp_reg = servingperf.insert(sp)

        # Execute the query
        cursor = self.db.aql.execute(
            'FOR doc IN deployment FILTER doc.tag == @value RETURN doc',
            bind_vars={'value': dep_tag})
        dep_docs = [doc for doc in cursor]
        the_dep_doc = dep_docs[0]
        # Link the service performance record with the deployment record
        dep_servingperf_edge = self.emlg.edge_collection(
            "deployment_servingperf")
        dep_servingperf_key = the_dep_doc["_key"] + "-" + sp_reg["_key"]
        the_dep_servingperf_edge = {"_key": dep_servingperf_key, \
                                    "_from": the_dep_doc["_id"], \
                                    "_to": sp_reg["_id"]}

        dep_servingperf_reg = dep_servingperf_edge.insert(
            the_dep_servingperf_edge)
        return dep_servingperf_reg

    def insert_into_vertex_type(self, vertex_type_name, document):
        vertex_info = None
        if self.emlg.has_vertex_collection(vertex_type_name):
            vc = self.emlg.vertex_collection(vertex_type_name)
            vertex_info = vc.insert(document)
        else:
            logger.error("Vertex, " + vertex_type_name +
                         " does not exist in Arangopipe!")

        return vertex_info

    def insert_into_edge_type(self,
                              edge_name,
                              from_vdoc,
                              to_vdoc,
                              document=None):
        edge_info = None
        if self.emlg.has_edge_collection(edge_name):
            try:
                ec = self.emlg.edge_collection(edge_name)
                edge_key = from_vdoc['_key'] + "-" + to_vdoc['_key']
                if document is not None:
                    document["_from"] = from_vdoc['_id']
                    document["_to"] = to_vdoc['_id']
                    document["_key"] = edge_key
                    edge_info = ec.insert(document)
                else:
                    document = {"_from": from_vdoc['_id'], \
                                "_to": to_vdoc['_id'], \
                                "_key": edge_key}
                    edge_info = ec.insert(document)
            except Exception as e:
                logger.error(e)
        else:
            logger.error("Edge, " + edge_name + " does not exist!")

        return edge_info
