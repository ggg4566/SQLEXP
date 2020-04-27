#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org

from lib.parse.payload import SQL,BOUNDARY


class Databases:
    def __init__(self,tech):
        self.query = SQL.base_query
        if tech == "E":
            self.boundary = BOUNDARY.error
            self.ini_boundary = BOUNDARY.error
        if tech == "B":
            self.boundary = BOUNDARY.blind
            self.ini_boundary = BOUNDARY.blind
        if tech == "T":
            self.boundary = BOUNDARY.time
            self.ini_boundary = BOUNDARY.time
        if tech == "U":
            self.boundary = BOUNDARY.union
            self.ini_boundary = BOUNDARY.union
    def reset_query(self):
        self.query = SQL.base_query

    def reset_boundary(self):
        self.boundary = self.ini_boundary

    def get_dbs(self):
        return

    def set_tables(self):
        return

    def get_tables(self):
        return

    def set_columns(self):
        return

    def get_columns(self):
        return

    def get_current_user(self):
        return

    def set_current_db(self):
        return

    def get_current_db(self):
        return

    def set_query(self,query):
        self.query = query

    def get_query(self):
        return self.query

    def get_boundary(self):
        return self.boundary

    def set_boundary(self,boundary):
        self.boundary = boundary

