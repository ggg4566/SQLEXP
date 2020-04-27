#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:flystart
# home:www.flystart.org


import logging
import sys
from lib.core.enums import CUSTOM_LOGGING


OUT_FILE = r"./output/files/log.txt"
logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")

LOGGER = logging.getLogger("SqlEXPLogger")

LOGGER_HANDLER = None
LOGGER_FILEHANDLER = logging.FileHandler(filename=OUT_FILE,encoding='utf-8')
try:
    from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler
    try:
        LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
        LOGGER_HANDLER.level_map[logging.getLevelName("*")] = (None, "cyan", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("+")] = (None, "green", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("-")] = (None, "red", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (None, "yellow", False)
    except Exception:
        LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

    
FORMATTER = logging.Formatter("\r[%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.addHandler(LOGGER_FILEHANDLER)
LOGGER.setLevel(CUSTOM_LOGGING.WARNING)


class FLY_LOGGER:
    @staticmethod
    def success(msg):
        return LOGGER.log(CUSTOM_LOGGING.SUCCESS, msg)

    @staticmethod
    def info(msg):
        return LOGGER.log(CUSTOM_LOGGING.SYSINFO, msg)

    @staticmethod
    def warning(msg):
        return LOGGER.log(CUSTOM_LOGGING.WARNING, msg)

    @staticmethod
    def error(msg):
        return LOGGER.log(CUSTOM_LOGGING.ERROR, msg)
