#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org
import sys
import re
from lib.core.data import conf,logger


def check_tech(tech):
    TECH_STR="EUBT"
    t = tech.upper()
    if t not in TECH_STR:
        logger.error("--tech param Error!!! value is one of {0}".format(list(TECH_STR)))
        sys.exit(1)
    return t

def parse_options(args):
    if not (args.url or args.parameter):
        logger.warning('Please input url and inject paramter!!!')
        sys.exit(1)
    if not (args.tech and args.dbms):
        logger.warning('Please set option --dbms,--tech')
        sys.exit(1)
    if args.db and (not (args.getTables or args.getColumns or args.dumpTable)):
        logger.warning('Dnt know what...Please options [--tables|--dump]')
        sys.exit(1)
    if args.db and args.tbl and (not (args.getColumns or args.dumpTable)):
        logger.warning('Dnt know what...Please options [--columns|--dump]')
        sys.exit(1)
    if args.db and args.tbl and args.col and not args.dumpTable:
        logger.warning('Dnt know what...Please options [--dump]')
        sys.exit(1)
    if (args.dumpTable or args.dumpTable) and (not args.db):
        logger.warning('Please input will dump db [-D test]')
        sys.exit(1)
    if args.dumpTable and args.col and (not args.tbl):
        logger.warning('Please input will dump table [-T test]')
        sys.exit(1)


def init_options(args):
    parse_options(args)
    conf.url = args.url
    conf.raw = args.raw_req
    conf.p = args.parameter
    conf.request_method = args.method
    conf.tech = check_tech(args.tech)
    conf.dbms = args.dbms
    conf.db = args.db
    conf.dbs = [c.strip() for c in args.db.split(',')] if args.db else args.db
    conf.table = [c.strip() for c in args.tbl.split(',')] if args.tbl else args.tbl
    conf.columns = [c.strip() for c in args.col.split(',')] if args.col else args.col
    conf.dumpTable = args.dumpTable
    conf.getDbs = args.getDbs
    conf.getTables = args.getTables
    conf.getColumns = args.getColumns
    conf.getCurrentDb = args.getCurrentDb
    conf.getCurrentUser = args.getCurrentUser
    conf.method = args.method
    conf.delay_time = args.delay_time
    conf.flag = args.flag
    conf.order_sec=args.order_sec
    conf.time_sec = args.time_sec
    conf.tamper = args.tamper
    conf.timeout = args.timeout
    conf.debug = args.debug
    p = args.proxy
    if p:
        pattern = "(http|socks)://([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,5}"
        match = re.findall(pattern,p)
        if match:
            conf.proxies = {match[0][0]:p.split('/')[-1]}
        else:
            logger.error("PROXY Format not corrent! Please input ex:[http://ip:port]")
            sys.exit(0)
    conf.data = args.data
    if args.cookie:
        conf.cookie = args.cookie
    return
