#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org

import os
import subprocess

IS_WIN = subprocess.mswindows
VERSION = '1.0.0'
PROJECT = "flySQLEXP"
AUTHOR = 'flystart'
MAIL = 'root@flystart.org'
PLATFORM = os.name
LICENSE = 'GPLv2'
BANNER ="""

 ______   ______    __             (     )        
/_____/\ /_____/\  /_/\           ))\ ( /( `  )           
\::::_\/_\:::_ \ \ \:\ \         /((_))\())/(/(                     
 \:\/___/\\:\ \ \ \_\:\ \       (_)) ((_)\((_)_\                        
  \_::._\:\\:\ \ /_ \\:\ \____  / -_)\ \ /| '_ \) 
    /____\:\\:\_-  \ \\:\/___/\ \___|/_\_\| .__/  
    \_____\/ \___|\_\_/\_____\/           |_|       
                                                        
        Version %s by %s mail:%s                        
""" % (VERSION, AUTHOR, MAIL)

# Encoding used for Unicode data
UNICODE_ENCODING = "utf-8"
# String representation for NULL value
NULL = "NULL"
# Format used for representing invalid unicode characters
INVALID_UNICODE_CHAR_FORMAT = r"\x%02x"