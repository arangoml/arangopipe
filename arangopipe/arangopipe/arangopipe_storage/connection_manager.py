#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 14:35:38 2020

@author: Rajiv Sambasivan
"""
from contextlib import contextmanager

from arangopipe.arangopipe_storage.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
from arangopipe.arangopipe_storage.managed_service_conn_parameters import (
    ManagedServiceConnParam,
)


@contextmanager
def arango_pipe_connections(conn_params, reuse_prev_connection=True):
    mdb_config = ArangoPipeConfig()
    mdb_config = mdb_config.create_connection_config(conn_params)
    admin = ArangoPipeAdmin(reuse_connection=reuse_prev_connection, config=mdb_config)
    ap_config = admin.get_config()
    ap = ArangoPipe(config=ap_config)
    yield admin, ap
