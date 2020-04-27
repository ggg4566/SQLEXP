#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org


import platform


def is_win():
    ret = False
    if platform.system()=='Windows':
        ret = True
    return ret