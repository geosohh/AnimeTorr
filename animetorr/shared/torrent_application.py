# -*- coding: utf-8 -*-
"""
Functions to get the path to the application used to download torrents.
Only works on Windows, since it uses Windows Registry.
"""
__author__ = 'Sohhla'


import _winreg
import re
import os
import db


def default_application_fullpath():
    """
    :rtype: str
    :return: Full path to the default application used by Windows to open .torrent files.

    :exception WindowsError
        There's no default application.
    """
    hkey = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,".torrent")
    torrent_file_type,_ = _winreg.QueryValueEx(hkey,"")
    hkey = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,"%s\shell\open\command" % torrent_file_type)
    open_command,_ = _winreg.QueryValueEx(hkey,"")
    regex = re.search('"?(.+\.exe)', open_command)
    app_path = regex.group(1)
    return app_path


def default_application_filename():
    """
    :rtype str
    :return Only the executable filename (*.exe).

    :exception WindowsError
        There's no default application.
    """
    app_path = default_application_fullpath()
    path_separator = os.sep if os.sep in app_path else "/"
    app_exe = app_path[app_path.rfind(path_separator)+1:]
    return app_exe


def fullpath():
    """
    :rtype: str
    :return: Full path to the application chosen to open .torrent files (default one or that selected by the user).

    :exception WindowsError
        Either there's no default application, or the application manually selected has been deleted/moved.
    """
    config = db.DBManager().get_config()
    if config.use_default_app:
        app_path = default_application_fullpath()
    else:
        app_path = config.app_path
    if os.path.exists(app_path) and app_path.endswith(".exe"):
        return app_path
    else:
        raise WindowsError


def filename(path=None):
    """
    :type path: str or unicode
    :param path
        Path to an .exe file. If none is received, will call fullpath().

    :rtype str
    :return Only the executable filename (*.exe).

    :exception WindowsError
        Either there's no default application, or the application manually selected has been deleted/moved.
    """
    if path is None:
        app_path = fullpath()
    else:
        app_path = path
    path_separator = os.sep if os.sep in app_path else "/"
    app_exe = app_path[app_path.rfind(path_separator)+1:]
    return app_exe


def is_utorrent():
    """
    Checks if the currently selected application to download torrents is uTorrent or not.
    If it is, an additional parameter "/DIRECTORY" can be sent, allowing uTorrent to save the episode
    in a custom folder (e.g. each anime in a different folder).

    :rtype: bool
    :return: If the currently selected application to download torrents is uTorrent or not.
    """
    app_exe = filename()
    return app_exe.lower() == "utorrent.exe"