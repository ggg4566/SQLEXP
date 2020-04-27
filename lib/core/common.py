#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org


import re
import sys
import os
import string
import random
import binascii
import imp
from lib.core.data import *
from lib.core.log import LOGGER_HANDLER
from lib.core.settings import BANNER, IS_WIN, UNICODE_ENCODING, NULL, INVALID_UNICODE_CHAR_FORMAT
from thirdparty.termcolor.termcolor import colored
import urlparse,urllib
import chardet
from math import sqrt


def is_list_like(value):
    """
    Returns True if the given value is a list-like instance
    """
    return isinstance(value, (list, tuple, set))


def format_unicode(raw_content, default_encoding_list=("utf-8", "gb18030")):
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


def get_unicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if noneToNull and value is None:
        return NULL

    if is_list_like(value):
        value = list(get_unicode(_, encoding, noneToNull) for _ in value)
        return value

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        while True:
            try:
                return unicode(value, encoding or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except Exception:
                    value = value[:ex.start] + "".join(
                        INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances


def banner():
    """
    Function prints banner with its version
    """
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = re.sub("\033.+?m", "", _)
        data_to_stdout(_)


def singleTimeWarnMessage(message):  # Cross-linked function
    sys.stdout.write(message)
    sys.stdout.write("\n")
    sys.stdout.flush()


def stdoutencode(data):
    retVal = None
    try:
        data = data or ""

        # Reference: http://bugs.python.org/issue1602
        if IS_WIN:
            output = data.encode(sys.stdout.encoding, "replace")
            if '?' in output and '?' not in data:
                warnMsg = "cannot properly display Unicode characters "
                warnMsg += "inside Windows OS command prompt "
                warnMsg += "(http://bugs.python.org/issue1602). All "
                warnMsg += "unhandled occurances will result in "
                warnMsg += "replacement with '?' character. Please, find "
                warnMsg += "proper character representation inside "
                warnMsg += "corresponding output files. "
                singleTimeWarnMessage(warnMsg)
            retVal = output
        else:
            retVal = data.encode(sys.stdout.encoding)
    except Exception:
        retVal = data.encode(UNICODE_ENCODING) if isinstance(data, unicode) else data
    return retVal


def data_to_stdout(data, bold=False):
    """
    Writes text to the stdout (console) stream
    """
    conf.SCREEN_OUTPUT = True
    if conf.SCREEN_OUTPUT:

        if isinstance(data, unicode):
            message = stdoutencode(data)
        else:
            message = data
        sys.stdout.write(setColor(message, bold))
        try:
            sys.stdout.flush()
        except IOError:
            pass
    return


def put_file_contents(filename,contents):
    with open(filename,"ab+") as fin:
        fin.write(contents+'\n')


def get_file_contents(filename):
    contents=""
    with open(filename,"rb") as fin:
        contents=fin.read()
    return contents


def setColor(message, bold=False):
    retVal = message
    if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
        if bold:
            retVal = colored(message, color=None, on_color=None, attrs=("bold",))
    return retVal


def set_paths(root_path):
    paths.OUTPUT_PATH = os.path.join(root_path, "output")
    paths.DUMP_PATH = os.path.join(paths.OUTPUT_PATH,"dump")
    paths.FILES_PATH = os.path.join(paths.OUTPUT_PATH,"files")
    paths.TAMPER_PATH = os.path.join(root_path, "tamper")
    paths.DBS = os.path.join(root_path,"lib/core/dbs/{}".format(conf.dbms))
    if not os.path.exists(paths.OUTPUT_PATH):
        os.mkdir(paths.OUTPUT_PATH)
    if not os.path.exists(paths.DUMP_PATH):
        os.mkdir(paths.DUMP_PATH)
    if not os.path.exists(paths.FILES_PATH):
        os.mkdir(paths.FILES_PATH)


def we_are_frozen():
    """
    Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.
    Reference: http://www.py2exe.org/index.cgi/WhereAmI
    """

    return hasattr(sys, "frozen")


def format_data(data):
    return data


def tamper(boundary,query):
    if conf.tamper:
        tamper = conf.tamper
        fp, pathname, description = imp.find_module(tamper, [paths.TAMPER_PATH])
        module_obj = imp.load_module("_", fp, pathname, description)
        fun = getattr(module_obj, 'tamper')
        boundary,query = fun(boundary,query)
    return boundary,query
# example inpput "321"
# return 0x333231
def format_hex(str):
    return "0x"+binascii.b2a_hex(str)


def un_hex(str):
    """
    :param str: 0x7879
    :return: "xy"
    """
    return binascii.a2b_hex(str[2:])


def random_str(length=5, chars=string.ascii_letters + string.digits):
    return ''.join(random.sample(chars, length))


def match_data(text,token):
    res = ""
    try:
        pattern = "{pre}(.*){suf}".format(pre=token,suf=token)
        matcher = re.search(re.compile(pattern), text)
        res = matcher.group(1)
    except Exception, e:
        pass
    return res


def match_all_data(text,token):
    result = ""
    try:
        text = match_data(text,token)
        result = text.split(token)
    except Exception,e:
        pass
    return result


def find_success(flag,text):
    ret = False
    if flag in text:
        ret = True
    return ret


def dict_to_q_str(dict):  # input {'id':1,'name':'greent'} | output id=1&name=greent
    return urllib.urlencode(dict)


def q_str_to_dict(query_str): #input id=1&name=greent | output {'id':1,'name':'greent'}
    return dict((k, v if len(v) > 1 else v[0]) for k, v in urlparse.parse_qs(query_str).iteritems())


def stdev(values):
    """
    Computes standard deviation of a list of numbers.
    Reference: http://www.goldb.org/corestats.html

    >>> stdev([0.9, 0.9, 0.9, 1.0, 0.8, 0.9])
    0.06324555320336757
    """

    if not values or len(values) < 2:
        return None
    else:
        avg = average(values)
        _ = reduce(lambda x, y: x + pow((y or 0) - avg, 2), values, 0.0)
        return sqrt(_ / (len(values) - 1))

def average(values):
    """
    Computes the arithmetic mean of a list of numbers.

    >>> average([0.9, 0.9, 0.9, 1.0, 0.8, 0.9])
    0.9
    """

    return (sum(values) / len(values)) if values else None


def url_encode(param):
    """
    ?id=param
    >>> url_encode(parma)
    :param param:
    :return:
    """
    return urllib.quote(param)

