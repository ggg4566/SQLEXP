#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org
# python SQLEXP -u  "http://192.168.25.129/sqlinject/sqlinject.php?id=2" -p id --dump --dbms mysql -D test --tech E
# python SQLEXP -u  "http://192.168.25.129/sqlinject/update_text.php" -p username --current-user\
#  --dbms mysql --tech E --order-sec "http://192.168.25.129/sqlinject/query_users.php?id=1"
# --method post --data="username=5" -D insertdata --dump
# E:\PythonProject\flySQLEXP>python SQLEXP.py -u "http://web.jarvisoj.com:32787/login.php" --data="username=user&password=admin" -p username --tamper=tamper_blank --dbms=mysql --technique=B --string="密码错误" --method=post  --dbs
# python SQL-u  "http://192.168.153.129/sqlinject/sqlinject.php?" -p id --data="id=1" --string=wang --tech E --dbms mysql -D test --dump  --method=post
# python SQLEXP.py-u http://localhost/sqlinject/sqlinject.php?id=2  -r E:\PythonProject\flySQLEXP_v2\req.txt --dbms mysql --tech E  --current-user  --debug
import os
import traceback
import sys
import inspect
from lib.parse.cmdline import cmdline_parse
from lib.core.data import paths,logger, cmdLineOptions
from lib.core.option import init_options
from lib.core.settings import IS_WIN, UNICODE_ENCODING
from lib.core.common import set_paths,we_are_frozen,get_unicode,banner

from thirdparty.colorama.initialise import init as winowsColorInit
from lib.controller.hander import start

reload(sys)
sys.setdefaultencoding('utf8')


def module_path():
    """
    This will get us the program's directory, even if we are frozen
    using py2exe
    """
    try:
        _ = sys.executable if we_are_frozen() else __file__
    except NameError:
        _ = inspect.getsourcefile(module_path)

    return get_unicode(os.path.dirname(os.path.realpath(_)), encoding=sys.getfilesystemencoding() or UNICODE_ENCODING)


def main():
    banner()
    try:
        paths.ROOT_PATH = module_path()
        try:
            os.path.isdir(paths.ROOT_PATH)
        except UnicodeEncodeError:
            errMsg = "your system does not properly handle non-ASCII paths. "
            errMsg += "Please move the project root directory to another location"
            logger.error(errMsg)
            raise SystemExit
        cmdLineOptions.update(cmdline_parse().__dict__)
        init_options(cmdLineOptions)
        set_paths(paths.ROOT_PATH)
        if IS_WIN:
            winowsColorInit()
        start()
    except Exception,e:
        logger.error(e.message)
        logger.error(traceback.format_exc())
    except Exception:
        logger.error(traceback.format_exc())
        logger.warning('It seems like you reached a unhandled exception, please report it to author\'s mail:root@flystart.org')


if __name__ == "__main__":
    main()