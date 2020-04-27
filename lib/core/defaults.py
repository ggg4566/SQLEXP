#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org


from lib.core.datatype import AttribDict
from lib.core.data import conf
_defaults = {
   "csvDel":       ',',
   "verbose":      1,
   "delay_time":   0,
   "timeout":      7,
   "timesec":     5,
   "retries":      3,
   "dumpFormat":   "CSV",
   "tech":         "E",
}

config = {
            "url": "",
            "p":"id",
            "tech":'E',
            "dbms":'',
            "db":'',
            "dbs":[''],
            "table":[],
            "columns":[],
            "getCurrentUser": False,
            "getCurrentDb":False,
            "getDbs":False,
            "getTables":False,
            "getColumns":False,
            "dumpTable":False,
            "proxies":"",
            "method":"",
            "cookie":"",
            "timeout":7,
            "delay_time":0,
            "time_sec":5,
            "data":"",
            "tamper":"test",
            "flag":"",
            "order_sec":"",
            "out_log":"log.txt",
            "raw":""
        }
defaults = AttribDict(_defaults)
conf.update(config)
