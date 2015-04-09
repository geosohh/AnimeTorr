# -*- coding: utf-8 -*-
"""
Manages the logging of errors and other messages from the application.

Based on: http://www.islascruz.org/html/index.php?blog/show/Python-Logging.html
Modified by Sohhla


This is part of the Christine project
Copyright (c) 2006-2007 Marco Antonio Islas Cruz

Christine is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Christine is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

@category  Pattern
@package   Singleton
@author    Miguel Vazquez Gocobachi <demrit@gnu.org>
@author    Marco Antonio Islas Cruz <markuz@islascruz.org>
@copyright 2007 Christine Development Group
@license   http://www.gnu.org/licenses/gpl.txt
@version   $Id$
"""


import sys
import traceback
import logging
import logging.handlers
import constant


# noinspection PyMethodParameters
# ^ because it's not my class.
class Singleton(object):
    """
    Manage instance of the given object

    Usage:
        Similar to java "implements"
        E.G.: class LoggerManager(Singleton): ......

    Copyright (c) 2006-2007 Marco Antonio Islas Cruz
    Modified by Sohhla
    """

    #
    # Manage instance
    #
    # @var object
    __Instance = None

    #
    # callback
    #
    def __new__(self, *args):
        if not self.__Instance:
            self.__Instance = super(Singleton, self).__new__(self, *args)
        else:
            self.__init__ = self.__do_nothing

        return self.__Instance

    # noinspection PyMethodMayBeStatic
    def __do_nothing(self, *args):
        """
        This method does nothing.

        It is used to override the __init__ method, so that no values may be
        re-declared after the first use of __init__ (When the instance was first created).
        """
        pass


class LoggerManager(Singleton):
    """
    Controls the log file: it's maximum size, number of backups, and access to write on the file.

    Copyright (c) 2006-2007 Marco Antonio Islas Cruz
    Modified by Sohhla
    """

    def __init__(self):
        self.loggers = {}
        self.LOGGING_HANDLER = logging.handlers.RotatingFileHandler(constant.LOG_PATH,maxBytes=1048576,backupCount=2)  # 1048576==1MB
        self.LOGGING_HANDLER.setFormatter(logging.Formatter("%(asctime)s ## %(name)-15s ## %(levelname)-10s ## %(message)s"))

    def get_logger(self, context):
        """
        :type context: str
        :param context:
            Represents from where the log message is coming from.
            Usually, it's the name of the class calling it.
            Examples: "Nyaa", "Anirena", "Downloader".

        :rtype: Logger
        :return:
            Object responsible for writting the log messages received from the given context.
        """
        if not context in self.loggers:
            self.loggers[context] = Logger(context, self.LOGGING_HANDLER)
        return self.loggers[context]


class Logger:
    """
    Custom Logger class.

    Copyright (c) 2006-2007 Marco Antonio Islas Cruz
    Modified by Sohhla
    """

    def __init__(self, name, logging_handler=None):
        self.__Logger = logging.getLogger(name)

        self.__Logger.addHandler(logging_handler)
        self.__Logger.setLevel(logging.DEBUG)

        self.debug = self.__Logger.debug
        self.info = self.__Logger.info
        self.warning = self.__Logger.warning
        self.error = self.__Logger.error
        self.critical = self.__Logger.critical

    @staticmethod
    def print_traceback(error,log_level):
        """
        Prints traceback to the log.

        :type error: Exception
        :param error: ...

        :type log_level: instancemethod
        :param log_level: method used to print the traceback (i.e. debug/info/etc.)
        """
        log_level("TRACEBACK:")
        for lines in traceback.format_tb(sys.exc_info()[2]):
            for line in lines.split('\n'):
                line = line.strip()
                if line!="":
                    log_level(line)
            log_level("")
        log_level("ERROR TYPE: %s" % type(error).__name__)
        log_level("ERROR: %s" % error.__doc__)
        log_level("MESSAGE: %s" % error.message)
