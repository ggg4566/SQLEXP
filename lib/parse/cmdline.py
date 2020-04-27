#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org


import sys
import os
from lib.core.settings import IS_WIN
from lib.core.common import get_unicode
from lib.core.defaults import defaults
from optparse import OptionError
from optparse import OptionGroup
from optparse import OptionParser


def cmdline_parse(argv=None):
    if not argv:
        argv = sys.argv
    _ = get_unicode(os.path.basename(argv[0]), encoding=sys.stdin.encoding)
    usage = "%s%s [options]" % ("python " if not IS_WIN else "", \
            "\"%s\"" % _ if " " in _ else _)

    parser = OptionParser(usage=usage)
    parser.print_help()
    try:
        parser.add_option("-v","--version", dest="showVersion",
                          action="store_true",
                          help="Show program's version number and exit")
        target = OptionGroup(parser, "Target", "At least one of these "
                                               "options has to be provided to define the target(s)")
        target.add_option("-u", "--url", dest="url", help="Target URL (e.g. \"http://www.site.com/vuln.php?id=1\")")
        # Request options
        target.add_option("-r", "--raw", dest="raw_req", help="Raw request packet file.")
        # Request options
        request = OptionGroup(parser, "Request", "These options can be used "
                                                 "to specify how to connect to the target URL")
        request.add_option("--method", dest="method",default = "get",
                           help="Force usage of given HTTP method (e.g. GET|POST)")

        request.add_option("--data", dest="data",
                           help="Data string to be sent through POST")
        request.add_option("--cookie", dest="cookie",
                           help="HTTP Cookie header value")
        request.add_option("--proxy", dest="proxy",
                           help="Use a proxy to connect to the target URL,only can use http proxy:[http://127.0.0.1:8080]")
        request.add_option("--timeout", dest="timeout", type="float",default =defaults.timeout,
                           help="Seconds to wait before timeout connection ")
        request.add_option("--delay", dest="delay_time", type="float",default =defaults.delay_time,
                           help="dbms delay timeout ")
        # Injection options
        injection = OptionGroup(parser, "Injection", "These options can be "
                                "used to specify which parameters to test "
                                "for, provide custom injection payloads and "
                                "optional tampering scripts")
        injection.add_option("-p", dest="parameter",
                             help="Testable parameter(s)")
        injection.add_option("--dbms", dest="dbms",
                             help="Force back-end DBMS to this value")
        injection.add_option("--technique", dest="tech", default= defaults.tech,
                              help="SQL injection techniques to use "
                                   "(default \"%s\")" % defaults.tech)
        injection.add_option("--string",dest="flag",
                             help="String to match when query is evaluated to True")
        injection.add_option("--time-sec", dest="time_sec", type="int",default =defaults.timesec,
                           help="Seconds to wait before timeout connection ")
        injection.add_option("--order-sec",dest="order_sec",
                             help="Resulting page URL searched for second-order "
                                  "response")
        injection.add_option("--tamper",dest="tamper",
                             help="Use given script(s) for tampering injection data")
        injection.add_option("--current-user", dest="getCurrentUser",
                               action="store_true",
                               help="Retrieve DBMS current user")

        injection.add_option("--current-db", dest="getCurrentDb",
                               action="store_true",
                               help="Retrieve DBMS current database")
        injection.add_option("--dbs", dest="getDbs", action="store_true",
                               help="Enumerate DBMS databases")
        injection.add_option("--tables", dest="getTables", action="store_true",
                               help="Enumerate DBMS database tables")
        injection.add_option("--columns", dest="getColumns", action="store_true",
                               help="Enumerate DBMS database table columns")
        injection.add_option("--dump", dest="dumpTable", action="store_true",
                               help="Dump DBMS database table entries")
        injection.add_option("-D", dest="db",
                               help="DBMS database to enumerate")
        injection.add_option("-T", dest="tbl",
                               help="DBMS database table(s) to enumerate")
        injection.add_option("-C", dest="col",
                               help="DBMS database table column(s) to enumerate")


        misc = OptionGroup(parser, "Misc", "These options can be show some additional function.")
        misc.add_option('--debug', dest="debug", default=False, action='store_true',
                          help='show deubg payload.')
        parser.add_option_group(target)
        parser.add_option_group(request)
        parser.add_option_group(injection)
        parser.add_option_group(misc)
        _ = []
        for arg in argv:
            _.append(get_unicode(arg, encoding=sys.stdin.encoding))
        argv = _
        (args, _) = parser.parse_args(argv)
    except Exception, e:
        raise Exception
    return args