#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:17:50 2019

@author: Rajiv Sambasivan
"""
import os
from typing import Any, Dict, Optional, cast

import yaml

from arangopipe.arangopipe_storage.managed_service_conn_parameters import (
    ManagedServiceConnParam,
)

APConfigDict = Dict[str, Dict[str, Any]]
ConnectionConfig = Dict[str, Any]


class ArangoPipeConfig:
    def __init__(self) -> None:
        self.cfg: Optional[APConfigDict] = None
        self.mscp = ManagedServiceConnParam()

    def read_data(self) -> APConfigDict:
        file_name = os.path.join(os.path.dirname(__file__), "arangopipe_config.yaml")
        with open(file_name, "r") as file_descriptor:
            cfg = yaml.load(file_descriptor, Loader=yaml.FullLoader)
        return cast(APConfigDict, cfg)

    def set_cfg(self, new_cfg: APConfigDict) -> None:
        self.cfg = new_cfg

    def get_cfg(self) -> APConfigDict:
        if self.cfg is None:
            self.cfg = self.read_data()
        return self.cfg

    def export_cfg(self, file_path: str) -> Optional[APConfigDict]:
        try:
            with open(file_path, "w") as file_descriptor:
                cfg = yaml.dump(self.cfg, file_descriptor)
                return cfg
        except (IOError, EOFError) as e:
            print(
                "Error writing config file to specified location: {}".format(e.args[-1])
            )
            return None

    def create_config(self, file_path: str) -> ConnectionConfig:
        conn_config = {}
        try:
            with open(file_path, "r") as stream:
                cfg = yaml.safe_load(stream)
            for key, value in cfg["arangodb"].items():
                conn_config[key] = value
        except (yaml.YAMLError, IOError, EOFError) as exc:
            print(
                "Error reading the config file from the path specified {}".format(
                    exc.args[-1]
                )
            )

        return conn_config

    def dump_data(self) -> Optional[APConfigDict]:
        file_name = os.path.join(os.path.dirname(__file__), "arangopipe_config.yaml")
        with open(file_name, "w") as file_descriptor:
            cfg = yaml.dump(self.cfg, file_descriptor)
        return cfg

    def create_connection_config(self, conn_params: Dict[str, Any]):
        self.cfg = {"arangodb": {}, "mlgraph": {"graphname": "enterprise_ml_graph"}}
        for key, value in conn_params.items():
            self.cfg["arangodb"][key] = value
        return self
