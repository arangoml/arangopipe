#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 09:05:19 2019

@author: Rajiv Sambasivan
"""


class ManagedServiceConnParam:
    @property
    def DB_SERVICE_HOST(self):
        return "DB_service_host"

    @property
    def DB_SERVICE_END_POINT(self):
        return "DB_end_point"

    @property
    def DB_SERVICE_NAME(self):
        return "DB_service_name"

    @property
    def DB_SERVICE_PORT(self):
        return "DB_service_port"

    @property
    def DB_NAME(self):
        return "dbName"

    @property
    def DB_REPLICATION_FACTOR(self):
        return "arangodb_replication_factor"

    @property
    def DB_USER_NAME(self):
        return "username"

    @property
    def DB_PASSWORD(self):
        return "password"

    @property
    def DB_ROOT_USER(self):
        return "root_user"

    @property
    def DB_ROOT_USER_PASSWORD(self):
        return "root_user_password"

    @property
    def DB_CONN_PROTOCOL(self):
        return "conn_protocol"

    @property
    def DB_NOTIFICATION_EMAIL(self):
        return "email"
