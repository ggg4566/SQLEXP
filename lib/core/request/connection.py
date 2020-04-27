#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org

import sys
import traceback
import hackhttp
import urlparse
import time
import chardet
# from requests.adapters import HTTPAdapter
from lib.core.datatype import AttribDict
from lib.core.data import conf,logger
from lib.core.common import q_str_to_dict,dict_to_q_str,format_hex,format_unicode,url_encode,get_file_contents
# requests.adapters.DEFAULT_RETRIES = 5
fly_req = hackhttp.hackhttp()
# fly_req.mount('http://', HTTPAdapter(max_retries=3))
# fly_req.mount('https://', HTTPAdapter(max_retries=3))


class Request:
    def __init__(self, headers, proxies={},timeout=3,method = 'get'):
        if proxies:
            host,port =proxies.values()[0].split(":")
            proxies = (host,int(port))
        if conf.raw:
            self.raw_request =get_file_contents(conf.raw)
        self.headers = headers
        self.proxies = proxies
        self.timeout = timeout
        self.method = method
        self.elapsed_time = 0
        fly_req.headers = self.headers
        fly_req.proxies = self.proxies

    def set_headers(self,headers):
        self.headers = headers

    def set_proxies(self,porxies):
        self.proxies = porxies

    def set_timeout(self,timeout):
        self.timeout = timeout

    def set_method(self,method):
        self.method = method

    def get_method(self):
        return self.method

    def get_proxies(self):
        return self.proxies

    def generate_params(self,url,payload):
        params = ""
        data = conf.data
        inject_param = conf.p
        if data:
            data_dics = q_str_to_dict(data)
            if inject_param in data_dics.keys():
                value = data_dics.get(inject_param)
                value = value + payload
                data_dics[inject_param] = value
                data  = data_dics
            else:
                data = data_dics
        parse_res = urlparse.urlparse(url)
        query = parse_res.query
        params_dict = q_str_to_dict(query)
        if inject_param in params_dict.keys():
            value = params_dict.get(inject_param)
            value = value + payload
            params_dict[inject_param] = value
            query_str = dict_to_q_str(params_dict)
            li = list(parse_res)
            index = [i for i, x in enumerate(li) if x == parse_res.query][0]
            li[index] = query_str
            url =urlparse.urlunparse(tuple(li)) #(1,2)=> url_string
            url = urlparse.unquote(url)
        return url,params,data

    def get_elapsed_time(self):
        return self.elapsed_time

    def send_raw_request(self,url,data="",payload=""):
        try:
            raw_request = data.replace("$*$", payload)
            status_code, head, content, redirect, log = fly_req.http(url, raw=raw_request,timeout=self.timeout, header=self.headers,
                                                                    proxy=self.proxies)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            sys.exit(1)
        return status_code, head, content, redirect, log


    def connection(self,url,payload = ""):
        time.sleep(conf.delay_time)
        ret = AttribDict()
        ret.code = 0
        ret.text = ''
        ret.success = False
        if conf.raw:
            raw_data = self.raw_request
            start_time = time.time()
            status_code, head, content, redirect, log = self.send_raw_request(url,raw_data,payload)
            end_time = time.time()
            self.elapsed_time = end_time-start_time
            ret.code = status_code
            con = content
            con = format_unicode(con)
            ret.text = get_text_value(con)
            ret.success = True
        else:
            if self.method == 'get':
                payload = url_encode(payload)
                pass
            try:
                url, params, data = self.generate_params(url, payload)
                if data:
                    data = dict_to_q_str(data)
                if self.method == 'get':
                    start_time = time.time()
                    status_code, head, content, redirect, log= fly_req.http(url,timeout = self.timeout,header =self.headers,proxy=self.proxies)
                    end_time = time.time()
                    self.elapsed_time = end_time-start_time
                    ret.code = status_code
                    con  =content
                    con= format_unicode(con)
                    ret.text = get_text_value(con)
                    ret.success = True

                if self.method == 'post':
                    start_time = time.time()
                    status_code, head, content, redirect, log = fly_req.http(url+'?'+params,data=data, timeout=self.timeout,header =self.headers,proxy=self.proxies)
                    end_time = time.time()
                    self.elapsed_time = end_time-start_time
                    ret.code = status_code
                    con  =content
                    con= format_unicode(con)
                    ret.text = get_text_value(con)
                    ret.success = True
            except Exception as e:
                logger.warning(e.message)
                sys.exit(0)
        return ret


def get_text_value(text):
    if conf.order_sec:
        url = conf.order_sec
        res = fly_req.get(url)
        text = res.content
    return text


def get_headers():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
                'Connection': 'close'}
    if conf.cookie:
        headers['cookie'] = conf.cookie
    return headers


def smart_decoder(raw_content, default_encoding_list=("utf-8", "gb18030")):
    if isinstance(raw_content, unicode):
        return raw_content

    encoding = chardet.detect(raw_content).get("encoding", "utf-8")

    try:
        return raw_content.decode(encoding)
    except UnicodeEncodeError as e:
        for encoding in default_encoding_list:
            try:
                return raw_content.decode(encoding)
            except UnicodeEncodeError as e:
                pass
        raise e

try:
    req = Request(get_headers(),conf.proxies,conf.timeout,conf.method)
except Exception as e:
    logger.error(e.message)
    logger.error(traceback.format_exc())
